#!/usr/bin/env python
"""Genera la PÁGINA INDIVIDUAL de cada jugador (confirmación pre-cierre).

Por cada predicción ingerida en data/predicciones/<slug>.* genera
`site/p/<slug-url>.html` con el pronóstico de ESE jugador (sus tablas de grupo +
su cuadro completo + campeón/especiales, banderas flagcdn) + un sello
"✓ recibido y registrado" y el aviso de que es su link privado hasta el cierre.

Visibilidad por tiempo (decisión Boris 2026-06-09): ANTES del 11-jun cada uno ve
solo SU página (link no listado, no se enlaza desde el sitio público). DESPUÉS del
cierre se abre la galería pública + leaderboard (otro generador).

Uso:
  python build/gen_jugador.py            # todos los jugadores (excluye La Casa)
  python build/gen_jugador.py MF         # solo ese slug
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(HERE, 'data', 'predicciones')
OUTDIR = os.path.join(HERE, 'site', 'p')
DENY = set()                        # La Casa (Boris Tapia V) pública. {'CASA'} para volver a ocultarla.
DEADLINE = '11-jun-2026'

CSS = """
:root{--bg:#0b1020;--card:#151c34;--card2:#1c2545;--line:#2a3358;--txt:#e8ecf7;--mut:#8d97bf;
--green:#16d97b;--gold:#ffd24a;--win:#1f8a55;}
*{box-sizing:border-box}
body{margin:0;background:linear-gradient(180deg,#0b1020,#0e1530);color:var(--txt);
font:15px/1.4 system-ui,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:1280px;margin:0 auto;padding:24px}
header{text-align:center;padding:28px 0 8px}
header .kick{color:var(--gold);letter-spacing:.18em;font-size:12px;text-transform:uppercase}
header h1{margin:6px 0 2px;font-size:30px}
header .sub{color:var(--mut)}
.recibido{max-width:760px;margin:14px auto 0;background:#10301c;border:1px solid #1f6b3f;
color:#a8f0c8;border-radius:12px;padding:12px 18px;text-align:center;font-size:14px}
.recibido b{color:#d6ffe7}
.recibido small{display:block;color:#6fbf93;margin-top:4px}
.apo-band{color:#ffd24a;font-style:italic;font-weight:700;font-size:19px;margin-top:6px}
.hooks{max-width:760px;margin:12px auto 0;background:#151c34;border:1px solid #2a3358;border-radius:12px;padding:11px 16px;color:#e8ecf7;font-size:14px}
nav{display:flex;gap:8px;justify-content:center;margin:10px 0}
nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:5px 14px;border:1px solid var(--line);border-radius:20px}
.champ{display:flex;justify-content:center;margin:22px 0 8px}
.champ-card{background:linear-gradient(160deg,#2a2140,#3a2c1a);border:1px solid #4a3a20;
border-radius:18px;padding:18px 30px;text-align:center;box-shadow:0 10px 40px #0006}
.champ-card .flag.big{width:78px;border-radius:5px;box-shadow:0 4px 14px #0008}
.champ-name{font-size:24px;font-weight:700;margin-top:8px}
.champ-label{color:var(--gold);font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-top:2px}
.bronze{text-align:center;color:var(--mut);margin:6px 0 24px}
.bronze .flag{vertical-align:-3px}
h2.sec{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);
border-bottom:1px solid var(--line);padding-bottom:8px;margin:30px 0 16px}
.bracket{display:flex;gap:14px;overflow-x:auto;padding-bottom:10px}
.round{min-width:185px;flex:1}
.round h3{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--mut);
text-align:center;margin:0 0 10px}
.match{background:var(--card);border:1px solid var(--line);border-radius:10px;margin-bottom:10px;overflow:hidden}
.match.empty{color:var(--mut);text-align:center;padding:14px;background:transparent;border-style:dashed}
.team{display:flex;align-items:center;gap:8px;padding:7px 9px;font-size:13px}
.team+.team{border-top:1px solid var(--line)}
.team.win{background:var(--win);font-weight:700}
.team span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.flag{width:26px;height:auto;border-radius:3px;box-shadow:0 1px 3px #0007;flex:0 0 auto}
.groups{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.gcard{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.gcard h4{margin:0 0 8px;font-size:13px;color:var(--gold)}
.gcard table{width:100%;border-collapse:collapse;font-size:12px}
.gcard td,.gcard th{padding:3px 4px;text-align:center;color:var(--txt)}
.gcard th{color:var(--mut);font-weight:500}
.gcard td.p{color:var(--mut);width:14px}
.gcard td.t{text-align:left;display:flex;align-items:center;gap:6px}
.gcard td.t .flag{width:20px}
.gcard tr.q1 td.p{color:var(--green);font-weight:700}
.gcard tr.q3 td.p{color:var(--gold);font-weight:700}
footer{text-align:center;color:var(--mut);font-size:12px;margin:30px 0 10px}
footer .legend span{margin:0 8px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;vertical-align:0}
"""


def slug_url(slug):
    return slug.lower().replace('_', '-')


def display_name(slug):
    return ' '.join(w.capitalize() for w in slug.replace('_', ' ').split())


def _load_apodos():
    p = os.path.join(HERE, 'data', 'apodos.csv'); d = {}
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('apodo'):
                d[r['slug']] = r['apodo'].strip()
    return d


def _load_results():
    rg, rk = {}, {}
    p = os.path.join(HERE, 'data', 'resultados.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('gl') not in (None, '') and r.get('gv') not in (None, ''):
                rg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    p = os.path.join(HERE, 'data', 'resultados_ko.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('ganador'):
                rk[int(r['match_no'])] = r['ganador'].strip().upper()
    return rg, rk


def _survivors(rg, rk, rv, eq, fixture, terceros):
    if len(rg) < 72:
        return set(eq)
    r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(rg, fixture), eq), fixture, terceros)
    qual = set()
    for a, b in r32.values():
        qual.update((a, b))
    los = set()
    for mn, w in rk.items():
        a, b = rv['teams'].get(mn, (None, None))
        if a and b:
            los.add(b if w == a else a)
    return qual - los


def load_pred(slug):
    gs, ko, esp = {}, {}, {}
    with open(os.path.join(PRED, f'{slug}.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            gs[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    with open(os.path.join(PRED, f'{slug}_ko.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['ganador']:
                ko[int(r['match_no'])] = r['ganador']
    with open(os.path.join(PRED, f'{slug}_especiales.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            esp[r['clave']] = r['valor']
    return gs, ko, esp


def render(slug, eq, fixture, terceros):
    gs, ko, esp = load_pred(slug)
    pb = engine.full_bracket(gs, ko, eq, fixture, terceros)
    ISO = {c: eq[c]['iso'] for c in eq}
    NM = {c: eq[c]['nombre_es'] for c in eq}
    name = esp.get('jugador') or display_name(slug)   # nombre real (con tildes) si la ingesta lo guardó

    def flag(code, big=False):
        if not code or code not in ISO:
            return ''
        w = 'w80' if big else 'w40'
        return f'<img class="flag{" big" if big else ""}" src="https://flagcdn.com/{w}/{ISO[code]}.png" alt="" loading="lazy">'

    def chip(code, win=False):
        cls = 'team win' if win else 'team'
        return f'<div class="{cls}">{flag(code)}<span>{NM.get(code, code)}</span></div>'

    def match_card(mn):
        a, b = pb['teams'][mn]
        w = pb['win'].get(mn)
        if a is None or b is None:
            return '<div class="match empty">—</div>'
        return f'<div class="match">{chip(a, w == a)}{chip(b, w == b)}</div>'

    ROUNDS = [('16avos', range(73, 89)), ('Octavos', range(89, 97)),
              ('Cuartos', range(97, 101)), ('Semis', (101, 102)), ('Final', (104,))]
    bracket_cols = ''
    for title, rng in ROUNDS:
        cards = ''.join(match_card(m) for m in rng)
        bracket_cols += f'<div class="round"><h3>{title}</h3>{cards}</div>'

    champ = esp.get('campeon')
    champ_html = (f'<div class="champ-card">{flag(champ, big=True)}'
                  f'<div class="champ-name">{NM.get(champ, champ)}</div>'
                  f'<div class="champ-label">Tu campeón</div></div>') if champ else ''
    tercero = pb['win'].get(103)
    tercero_html = f'<div class="bronze">🥉 3er puesto: {flag(tercero)} <b>{NM.get(tercero, tercero)}</b></div>' if tercero else ''
    ei = []
    if esp.get('goleador'):
        ei.append(f'⚽ Goleador: <b>{esp["goleador"]}</b>')
    if esp.get('primer_eliminado'):
        pe = esp['primer_eliminado']
        ei.append(f'💀 1º eliminado: {flag(pe)} <b>{NM.get(pe, pe)}</b>')
    if esp.get('sorpresa'):
        ei.append(f'🎁 Sorpresa: <b>{esp["sorpresa"]}</b>')
    esp_html = ('<div class="bronze">' + ' &nbsp;·&nbsp; '.join(ei) + '</div>') if ei else ''

    # ---- ganchos personales (research #1: identidad + obsesión) ----
    apodo = _load_apodos().get(slug, '')
    rg, rk = _load_results()
    hooks = []
    if champ:
        cm = [m for m in fixture if m['fase'] == 'grupos' and champ in (m['local'], m['visita'])]
        nx = next((m for m in cm if m['match_no'] not in rg), None)
        if nx:
            opp = nx['visita'] if nx['local'] == champ else nx['local']
            hooks.append(f'📅 {NM.get(champ, champ)} juega el {nx["fecha"][5:]} vs {NM.get(opp, opp)}')
    if rg or rk:
        rv = engine.full_bracket(rg, rk, eq, fixture, terceros)
        alive = champ in _survivors(rg, rk, rv, eq, fixture, terceros)
        hooks.append('🟢 tu campeón sigue vivo' if alive else '💀 tu campeón cayó')
        import snapshot
        players = snapshot.load_players()
        if len(players) > 1:
            st = snapshot.compute_standings(players, rg, rk, eq, fixture, terceros)
            me = next((r for r in st if r['slug'] == slug), None)
            if me:
                if me['pos'] <= 3:
                    hooks.append(f'🎯 Vas {me["pos"]}º de {len(st)} — en zona de premio 🏆')
                else:
                    gap = st[2]['total'] - me['total']
                    hooks.append(f'🎯 Vas {me["pos"]}º de {len(st)} — a {gap} pts del podio')
    apodo_html = f'<div class="apo-band">«{apodo}»</div>' if apodo else ''
    hooks_html = ('<div class="hooks">' + ' &nbsp;·&nbsp; '.join(hooks) + '</div>') if hooks else ''

    allst = engine.compute_all_standings(engine.group_results_by_group(gs, fixture), eq)
    groups_html = ''
    for g in 'ABCDEFGHIJKL':
        rows = ''
        for t in allst[g]:
            pos = t['pos']
            mark = 'q1' if pos <= 2 else ('q3' if pos == 3 else '')
            rows += (f'<tr class="{mark}"><td class="p">{pos}</td><td class="t">{flag(t["code"])}'
                     f'<span>{NM[t["code"]]}</span></td><td>{t["pts"]}</td>'
                     f'<td>{t["gd"]:+d}</td><td>{t["gf"]}</td></tr>')
        groups_html += (f'<div class="gcard"><h4>Grupo {g}</h4><table>'
                        f'<tr class="h"><th></th><th></th><th>Pts</th><th>DG</th><th>GF</th></tr>'
                        f'{rows}</table></div>')

    nfilled = len([1 for v in gs.values()])
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Tu pronóstico · {name} · Quiniela Mundial 2026</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <div class="kick">Copa Mundial FIFA · Canadá · México · EE.UU.</div>
  <h1>Tu Quiniela 2026</h1>
  <div class="sub">Pronóstico de <b>{name}</b></div>
  {apodo_html}
  <div class="recibido">✓ <b>Recibido y registrado</b> — {nfilled}/72 marcadores de grupo + tu cuadro completo.
    <small>Este es tu link privado. No lo compartas hasta el cierre ({DEADLINE}).</small></div>
  {hooks_html}
  <nav><a href="../calendario.html">Calendario del torneo</a></nav>
</header>

<div class="champ">{champ_html}</div>
{tercero_html}
{esp_html}

<h2 class="sec">Tu cuadro de eliminatorias</h2>
<div class="bracket">{bracket_cols}</div>

<h2 class="sec">Tu fase de grupos (posiciones que implican tus marcadores)</h2>
<div class="groups">{groups_html}</div>

<footer>
  <div class="legend">
    <span><i class="dot" style="background:var(--green)"></i> 1º/2º clasifican</span>
    <span><i class="dot" style="background:var(--gold)"></i> 3º (mejores terceros)</span>
  </div>
  <div style="margin-top:8px">Cuando cierre el plazo se publicará la tabla con todos los jugadores. ¡Suerte!</div>
</footer>
</div></body></html>"""
    return html, name, champ, NM


def discover_slugs():
    out = []
    for fn in sorted(os.listdir(PRED)):
        if fn.endswith('.csv') and not fn.endswith('_ko.csv') and not fn.endswith('_especiales.csv'):
            slug = fn[:-4]
            if slug in DENY:
                continue
            if all(os.path.exists(os.path.join(PRED, f'{slug}{suf}.csv')) for suf in ('_ko', '_especiales')):
                out.append(slug)
    return out


def main():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    slugs = sys.argv[1:] if len(sys.argv) > 1 else discover_slugs()
    if not slugs:
        print('No hay predicciones de jugadores en data/predicciones/ (excluyendo La Casa).')
        return
    os.makedirs(OUTDIR, exist_ok=True)
    links = []
    for slug in slugs:
        html, name, champ, NM = render(slug, eq, fixture, terceros)
        url = slug_url(slug)
        with open(os.path.join(OUTDIR, f'{url}.html'), 'w', encoding='utf-8') as f:
            f.write(html)
        champ_n = NM.get(champ, champ) if champ else '(sin campeón)'
        print(f'  ✓ {name:24} -> site/p/{url}.html   (campeón: {champ_n})')
        links.append((name, f'p/{url}.html'))

    # índice PRIVADO de links (no se despliega; ayuda a Boris a saber qué mandar)
    idx = os.path.join(HERE, 'private', 'links-jugadores.md')
    os.makedirs(os.path.dirname(idx), exist_ok=True)
    with open(idx, 'w', encoding='utf-8') as f:
        f.write('# Links privados por jugador (Quiniela Mundial 2026)\n\n')
        f.write('Reemplaza BASE por el dominio Netlify del sitio. Manda a cada uno SOLO su link.\n\n')
        for name, rel in links:
            f.write(f'- **{name}**: `BASE/{rel}`\n')
    print(f'\n{len(slugs)} página(s) generadas en site/p/ · índice privado: private/links-jugadores.md')


if __name__ == '__main__':
    main()
