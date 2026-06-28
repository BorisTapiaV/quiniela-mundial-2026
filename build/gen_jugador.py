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
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');
:root{--bg0:#070b18;--bg1:#0c1226;--card:#121a33;--card2:#18224a;--line:#26305a;--line2:#36427e;
--txt:#eef1fb;--mut:#949ec7;--mut2:#6b76a3;--green:#22e08c;--gold:#ffd35a;--gold2:#ffae3c;--win:#1c7d4e;--rad:16px;}
*{box-sizing:border-box}
body{margin:0;color:var(--txt);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;
font:15px/1.55 'Outfit',system-ui,'Segoe UI',Roboto,sans-serif;
background:
 radial-gradient(900px 480px at 50% -160px,rgba(255,178,60,.10),transparent 70%),
 radial-gradient(1100px 600px at 85% 8%,rgba(34,120,224,.10),transparent 65%),
 linear-gradient(180deg,#070b18,#0b1124 45%,#080d1e);
 background-attachment:fixed;min-height:100vh}
.wrap{max-width:1180px;margin:0 auto;padding:24px}
header{text-align:center;padding:26px 0 6px}
.brand-logo{width:60px;height:60px;border-radius:15px;object-fit:cover;display:block;margin:0 auto 10px;
border:1.5px solid var(--line2);box-shadow:0 8px 26px #0009,0 0 0 4px rgba(255,211,90,.05)}
.kick{color:var(--gold);letter-spacing:.22em;font-size:11px;font-weight:600;text-transform:uppercase}
header h1{margin:8px 0 2px;font-size:34px;font-weight:800;letter-spacing:-.01em;
background:linear-gradient(180deg,#fff,#b9c4ee);-webkit-background-clip:text;background-clip:text;color:transparent}
header .sub{color:var(--mut);font-size:15px}
header .sub b{color:var(--txt)}
.apo-band{color:var(--gold);font-style:italic;font-weight:700;font-size:18px;margin-top:6px}
.recibido{max-width:680px;margin:16px auto 0;background:linear-gradient(180deg,rgba(34,224,140,.10),rgba(34,224,140,.04));
border:1px solid rgba(34,224,140,.30);color:#bdf6d8;border-radius:13px;padding:11px 18px;font-size:13.5px}
.recibido b{color:#e2fff0}
.recibido small{display:block;color:#7fcaa3;margin-top:3px}
.hooks{max-width:680px;margin:12px auto 0;background:rgba(255,255,255,.035);border:1px solid var(--line);
border-radius:13px;padding:11px 16px;color:var(--txt);font-size:13.5px}
nav{display:flex;gap:9px;justify-content:center;margin:16px 0 4px;flex-wrap:wrap}
nav a{color:var(--mut);text-decoration:none;font-size:13px;font-weight:500;padding:7px 16px;
border:1px solid var(--line);border-radius:22px;transition:.15s}
nav a:hover{border-color:var(--line2);color:var(--txt);background:rgba(255,255,255,.03)}
nav a.back{color:var(--gold);border-color:rgba(255,211,90,.4)}
nav a.back:hover{background:rgba(255,211,90,.08)}

/* ---- Hero campeón ---- */
.hero{position:relative;display:flex;flex-direction:column;align-items:center;
margin:34px auto 8px;padding:30px 20px 26px;max-width:420px;
background:linear-gradient(165deg,rgba(58,44,26,.55),rgba(38,30,52,.45));
border:1px solid rgba(255,180,60,.28);border-radius:24px;
box-shadow:0 20px 60px -20px #000,inset 0 1px 0 rgba(255,255,255,.05);overflow:hidden}
.hero::before{content:"";position:absolute;top:-90px;left:50%;transform:translateX(-50%);
width:260px;height:260px;border-radius:50%;
background:radial-gradient(circle,rgba(255,200,80,.35),transparent 60%);pointer-events:none}
.hero .flag.big{width:96px;height:auto;border-radius:7px;position:relative;
box-shadow:0 10px 30px #000a,0 0 0 1px rgba(255,255,255,.12)}
.hero-name{font-size:30px;font-weight:800;margin-top:14px;letter-spacing:-.01em;position:relative}
.hero-label{position:relative;margin-top:6px;color:#0b0a06;background:linear-gradient(180deg,var(--gold),var(--gold2));
font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;padding:4px 14px;border-radius:20px;
box-shadow:0 4px 14px rgba(255,174,60,.35)}

/* ---- Tarjetas resumen ---- */
.summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:20px 0 6px}
.scard{background:linear-gradient(180deg,var(--card),rgba(18,26,51,.6));border:1px solid var(--line);
border-radius:var(--rad);padding:14px 16px;display:flex;flex-direction:column;gap:5px;transition:.15s}
.scard:hover{border-color:var(--line2);transform:translateY(-2px)}
.scard .k{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut2);font-weight:600;
display:flex;align-items:center;gap:6px}
.scard .v{font-size:16px;font-weight:700;display:flex;align-items:center;gap:8px}
.scard .v .flag{width:26px}

h2.sec{font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--mut);font-weight:600;
display:flex;align-items:center;gap:12px;margin:38px 0 18px}
h2.sec::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--line),transparent)}

/* ---- Bracket ---- */
.bracket{display:flex;gap:14px;overflow-x:auto;padding-bottom:12px}
.round{min-width:190px;flex:1}
.round h3{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--mut2);font-weight:600;
text-align:center;margin:0 0 12px}
.match{background:linear-gradient(180deg,var(--card),rgba(18,26,51,.55));border:1px solid var(--line);
border-radius:12px;margin-bottom:11px;overflow:hidden;box-shadow:0 4px 14px -8px #000}
.match.empty{color:var(--mut2);text-align:center;padding:15px;background:transparent;border-style:dashed;box-shadow:none}
.team{display:flex;align-items:center;gap:9px;padding:8px 11px;font-size:13px}
.team+.team{border-top:1px solid var(--line)}
.team.win{background:linear-gradient(90deg,rgba(28,125,78,.55),rgba(28,125,78,.18));font-weight:700}
.team.champ{background:linear-gradient(90deg,rgba(255,180,60,.28),rgba(255,180,60,.07));font-weight:700;color:#ffe7ad}
.team span{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.flag{width:27px;height:auto;border-radius:4px;box-shadow:0 1px 3px #0008;flex:0 0 auto}

/* ---- Grupos ---- */
.groups{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:13px}
.gcard{background:linear-gradient(180deg,var(--card),rgba(18,26,51,.55));border:1px solid var(--line);
border-radius:var(--rad);padding:13px 15px}
.gcard h4{margin:0 0 10px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--gold);font-weight:600}
.gcard table{width:100%;border-collapse:collapse;font-size:12.5px}
.gcard td,.gcard th{padding:5px 4px;text-align:center}
.gcard th{color:var(--mut2);font-weight:500;font-size:10.5px;text-transform:uppercase;letter-spacing:.05em}
.gcard tr+tr td{border-top:1px solid rgba(255,255,255,.04)}
.gcard td.p{color:var(--mut2);width:16px;font-weight:600}
.gcard td.t{text-align:left;display:flex;align-items:center;gap:7px}
.gcard td.t .flag{width:21px}
.gcard tr.q1{background:linear-gradient(90deg,rgba(34,224,140,.08),transparent)}
.gcard tr.q1 td.p{color:var(--green);font-weight:800}
.gcard tr.q3{background:linear-gradient(90deg,rgba(255,211,90,.07),transparent)}
.gcard tr.q3 td.p{color:var(--gold);font-weight:800}

h2.sec .note{font-weight:500;letter-spacing:0;text-transform:none;color:var(--mut2);font-size:12px}
/* ---- Aciertos fase de grupos ---- */
.hits{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}
.hcard{position:relative;background:linear-gradient(180deg,var(--card),rgba(18,26,51,.55));
border:1px solid var(--line);border-radius:var(--rad);padding:13px 14px 12px;overflow:hidden;transition:.15s}
.hcard.miss{opacity:.62}
.hcard.part{border-color:rgba(34,224,140,.32)}
.hcard.exact{border-color:rgba(255,180,60,.55);
background:linear-gradient(180deg,rgba(58,44,26,.55),rgba(28,22,12,.4));
box-shadow:0 10px 34px -16px rgba(255,174,60,.6),inset 0 1px 0 rgba(255,255,255,.05)}
.hcard.exact::before{content:"";position:absolute;top:-40px;right:-40px;width:120px;height:120px;border-radius:50%;
background:radial-gradient(circle,rgba(255,200,80,.22),transparent 65%);pointer-events:none}
.hbadge{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.04em;padding:3px 10px;border-radius:20px;margin-bottom:10px}
.hcard.exact .hbadge{color:#0b0a06;background:linear-gradient(180deg,var(--gold),var(--gold2));box-shadow:0 3px 12px rgba(255,174,60,.4)}
.hcard.part .hbadge{color:#bdf6d8;background:rgba(34,224,140,.16);border:1px solid rgba(34,224,140,.4)}
.hcard.miss .hbadge{color:var(--mut2);background:rgba(255,255,255,.05);border:1px solid var(--line)}
.hrow{display:flex;align-items:center;gap:9px;font-size:13.5px;padding:3px 0}
.hrow .flag{width:24px}
.hrow span{flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hrow b{font-variant-numeric:tabular-nums;font-size:15px}
.hcard.exact .hrow b{color:var(--gold)}
.hreal{margin-top:9px;padding-top:8px;border-top:1px solid rgba(255,255,255,.06);
font-size:11.5px;color:var(--mut2);letter-spacing:.02em}
.hreal b{color:var(--mut);font-variant-numeric:tabular-nums}
footer{text-align:center;color:var(--mut);font-size:12px;margin:40px 0 14px}
footer .legend span{margin:0 10px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;vertical-align:0}
.scrollhint{display:none;color:var(--mut2);font-size:11px;text-align:center;margin:-6px 0 8px}
@media(max-width:560px){
  .wrap{padding:14px}
  header{padding:18px 0 4px}
  header h1{font-size:26px}
  .hero{margin-top:24px;padding:24px 16px 22px}
  .hero .flag.big{width:80px}
  .hero-name{font-size:25px}
  .recibido,.hooks{padding:10px 13px;font-size:13px}
  .summary{grid-template-columns:1fr 1fr;gap:10px}
  .bracket{gap:10px}
  .round{min-width:154px}
  .groups{grid-template-columns:1fr}
  .scrollhint{display:block}
}
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

    champ = esp.get('campeon')

    def chip(code, win=False):
        if win and code and code == champ:
            cls = 'team champ'
        elif win:
            cls = 'team win'
        else:
            cls = 'team'
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

    # ---- Hero del campeón ----
    hero_html = (f'<div class="hero">{flag(champ, big=True)}'
                 f'<div class="hero-name">{NM.get(champ, champ)}</div>'
                 f'<div class="hero-label">★ Campeón pronosticado</div></div>') if champ else ''

    # ---- Tarjetas de resumen (subcampeón derivado del bracket + 3º + especiales) ----
    fa, fb = pb['teams'].get(104, (None, None))
    subcampeon = fb if champ == fa else (fa if champ == fb else None)   # el otro finalista
    tercero = pb['win'].get(103)
    cards = []
    if subcampeon:
        cards.append(('🥈', 'Subcampeón', f'{flag(subcampeon)}<span>{NM.get(subcampeon, subcampeon)}</span>'))
    if tercero:
        cards.append(('🥉', '3er puesto', f'{flag(tercero)}<span>{NM.get(tercero, tercero)}</span>'))
    if esp.get('goleador'):
        cards.append(('⚽', 'Goleador', f'<span>{esp["goleador"]}</span>'))
    summary_html = ''
    if cards:
        summary_html = '<div class="summary">' + ''.join(
            f'<div class="scard"><div class="k">{ico} {lbl}</div><div class="v">{val}</div></div>'
            for ico, lbl, val in cards) + '</div>'

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

    # ---- Aciertos en fase de grupos (partidos ya jugados) ----
    FX = {m['match_no']: m for m in fixture}
    hits, n_clav = [], 0
    for mn in sorted(rg):
        if mn > 72 or mn not in gs:
            continue
        m = FX.get(mn)
        if not m or m.get('fase') != 'grupos':
            continue
        (pl, pv), (rl, rv) = gs[mn], rg[mn]
        pts = engine.score_group_match((pl, pv), (rl, rv))
        if pts == 5:
            kind, badge = 'exact', '🎯 Clavado +5'; n_clav += 1
        elif pts == 3:
            kind, badge = 'part', '✓ Diferencia +3'
        elif pts == 2:
            kind, badge = 'part', '✓ Ganador +2'
        else:
            kind, badge = 'miss', '✗ +0'
        L, V = m['local'], m['visita']
        hits.append(
            f'<div class="hcard {kind}"><span class="hbadge">{badge}</span>'
            f'<div class="hrow">{flag(L)}<span>{NM.get(L, L)}</span><b>{pl}</b></div>'
            f'<div class="hrow">{flag(V)}<span>{NM.get(V, V)}</span><b>{pv}</b></div>'
            f'<div class="hreal">Resultado real: <b>{rl}-{rv}</b></div></div>')
    hits_html = ''
    if hits:
        note = f'{n_clav} clavado{"s" if n_clav != 1 else ""} de {len(hits)} jugado{"s" if len(hits) != 1 else ""}'
        hits_html = (f'<h2 class="sec">🎯 Tus aciertos en fase de grupos <span class="note">({note})</span></h2>'
                     f'<div class="hits">{"".join(hits)}</div>')

    nfilled = len([1 for v in gs.values()])
    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Tu pronóstico · {name} · Quiniela Mundial 2026</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <img class="brand-logo" src="../fisio-fc.png" alt="Fisioterapia & Futbolito FC">
  <div class="kick">Copa Mundial FIFA 2026 · Canadá · México · EE.UU.</div>
  <h1>Tu Quiniela 2026</h1>
  <div class="sub">Pronóstico de <b>{name}</b></div>
  {apodo_html}
  <div class="recibido">✓ <b>Recibido y registrado</b> — {nfilled}/72 marcadores de grupo + tu cuadro.
    <small>Pronóstico sellado. ¡Suerte!</small></div>
  {hooks_html}
  <nav><a class="back" href="../index.html">← Tabla de posiciones</a><a href="../calendario.html">Calendario</a></nav>
</header>

{hero_html}
{summary_html}

<h2 class="sec">Tu cuadro de eliminatorias</h2>
<div class="scrollhint">→ desliza para ver todas las rondas</div>
<div class="bracket">{bracket_cols}</div>

{hits_html}

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
