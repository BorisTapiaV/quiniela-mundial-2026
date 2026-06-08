#!/usr/bin/env python
"""Generador del visor HTML estático (prototipo) — Mundial 2026.

Renderiza el pronóstico de un jugador: tablas de grupo + bracket completo,
con banderas oficiales de flagcdn. Salida: site/index.html (estático, Netlify-ready).
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'MF'

def load_pred():
    base = os.path.join(HERE, 'data/predicciones')
    gs = {}
    with open(os.path.join(base, f'{SLUG}.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            gs[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    ko = {}
    with open(os.path.join(base, f'{SLUG}_ko.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            ko[int(r['match_no'])] = r['ganador']
    esp = {}
    with open(os.path.join(base, f'{SLUG}_especiales.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            esp[r['clave']] = r['valor']
    return gs, ko, esp

def main():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    gs, ko, esp = load_pred()
    pb = engine.full_bracket(gs, ko, eq, fixture, terceros)
    ISO = {c: eq[c]['iso'] for c in eq}
    NM = {c: eq[c]['nombre_es'] for c in eq}

    def flag(code, big=False):
        w = 'w80' if big else 'w40'
        return f'<img class="flag{" big" if big else ""}" src="https://flagcdn.com/{w}/{ISO[code]}.png" alt="" loading="lazy">'

    def chip(code, win=False):
        cls = 'team win' if win else 'team'
        return f'<div class="{cls}">{flag(code)}<span>{NM[code]}</span></div>'

    def match_card(mn):
        a, b = pb['teams'][mn]
        w = pb['win'].get(mn)
        if a is None or b is None:
            return '<div class="match empty">—</div>'
        return f'<div class="match">{chip(a, w==a)}{chip(b, w==b)}</div>'

    ROUNDS = [('16avos', range(73, 89)), ('Octavos', range(89, 97)),
              ('Cuartos', range(97, 101)), ('Semis', (101, 102)), ('Final', (104,))]
    bracket_cols = ''
    for title, rng in ROUNDS:
        cards = ''.join(match_card(m) for m in rng)
        bracket_cols += f'<div class="round"><h3>{title}</h3>{cards}</div>'

    champ = esp.get('campeon')
    champ_html = (f'<div class="champ-card">{flag(champ, big=True)}'
                  f'<div class="champ-name">{NM[champ]}</div>'
                  f'<div class="champ-label">Campeón pronosticado</div></div>') if champ else ''
    tercero = pb['win'].get(103)
    tercero_html = f'<div class="bronze">🥉 3er puesto: {flag(tercero)} <b>{NM[tercero]}</b></div>' if tercero else ''

    # tablas de grupo
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

    html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Quiniela Mundial 2026 · Pronóstico de {SLUG}</title>
<style>
:root{{--bg:#0b1020;--card:#151c34;--card2:#1c2545;--line:#2a3358;--txt:#e8ecf7;--mut:#8d97bf;
--green:#16d97b;--gold:#ffd24a;--win:#1f8a55;}}
*{{box-sizing:border-box}}
body{{margin:0;background:linear-gradient(180deg,#0b1020,#0e1530);color:var(--txt);
font:15px/1.4 system-ui,'Segoe UI',Roboto,sans-serif}}
.wrap{{max-width:1280px;margin:0 auto;padding:24px}}
header{{text-align:center;padding:28px 0 8px}}
header .kick{{color:var(--gold);letter-spacing:.18em;font-size:12px;text-transform:uppercase}}
header h1{{margin:6px 0 2px;font-size:30px}}
header .sub{{color:var(--mut)}}
.champ{{display:flex;justify-content:center;margin:22px 0 8px}}
.champ-card{{background:linear-gradient(160deg,#2a2140,#3a2c1a);border:1px solid #4a3a20;
border-radius:18px;padding:18px 30px;text-align:center;box-shadow:0 10px 40px #0006}}
.champ-card .flag.big{{width:78px;border-radius:5px;box-shadow:0 4px 14px #0008}}
.champ-name{{font-size:24px;font-weight:700;margin-top:8px}}
.champ-label{{color:var(--gold);font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-top:2px}}
.bronze{{text-align:center;color:var(--mut);margin:6px 0 24px}}
.bronze .flag{{vertical-align:-3px}}
h2.sec{{font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut);
border-bottom:1px solid var(--line);padding-bottom:8px;margin:30px 0 16px}}
.bracket{{display:flex;gap:14px;overflow-x:auto;padding-bottom:10px}}
.round{{min-width:185px;flex:1}}
.round h3{{font-size:12px;text-transform:uppercase;letter-spacing:.1em;color:var(--mut);
text-align:center;margin:0 0 10px}}
.match{{background:var(--card);border:1px solid var(--line);border-radius:10px;
margin-bottom:10px;overflow:hidden}}
.match.empty{{color:var(--mut);text-align:center;padding:14px;background:transparent;border-style:dashed}}
.team{{display:flex;align-items:center;gap:8px;padding:7px 9px;font-size:13px}}
.team+.team{{border-top:1px solid var(--line)}}
.team.win{{background:var(--win);font-weight:700}}
.team span{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.flag{{width:26px;height:auto;border-radius:3px;box-shadow:0 1px 3px #0007;flex:0 0 auto}}
.groups{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}}
.gcard{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}}
.gcard h4{{margin:0 0 8px;font-size:13px;color:var(--gold)}}
.gcard table{{width:100%;border-collapse:collapse;font-size:12px}}
.gcard td,.gcard th{{padding:3px 4px;text-align:center;color:var(--txt)}}
.gcard th{{color:var(--mut);font-weight:500}}
.gcard td.p{{color:var(--mut);width:14px}}
.gcard td.t{{text-align:left;display:flex;align-items:center;gap:6px}}
.gcard td.t .flag{{width:20px}}
.gcard tr.q1 td.p{{color:var(--green);font-weight:700}}
.gcard tr.q3 td.p{{color:var(--gold);font-weight:700}}
footer{{text-align:center;color:var(--mut);font-size:12px;margin:30px 0 10px}}
footer .legend span{{margin:0 8px}}
.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;vertical-align:0}}
</style></head>
<body><div class="wrap">
<header>
  <div class="kick">Copa Mundial FIFA · Canadá · México · EE.UU.</div>
  <h1>Quiniela 2026</h1>
  <div class="sub">Pronóstico de <b>{SLUG}</b> · vista de solo lectura (prototipo)</div>
</header>

<div class="champ">{champ_html}</div>
{tercero_html}

<h2 class="sec">Cuadro de eliminatorias</h2>
<div class="bracket">{bracket_cols}</div>

<h2 class="sec">Fase de grupos (posiciones que implica su pronóstico)</h2>
<div class="groups">{groups_html}</div>

<footer>
  <div class="legend">
    <span><i class="dot" style="background:var(--green)"></i> 1º/2º clasifican</span>
    <span><i class="dot" style="background:var(--gold)"></i> 3º (mejores terceros)</span>
  </div>
  <div style="margin-top:8px">Banderas: flagcdn.com (dominio público) · generado por gen_site.py</div>
</footer>
</div></body></html>"""

    os.makedirs(os.path.join(HERE, 'site'), exist_ok=True)
    out = os.path.join(HERE, 'site', 'index.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print('site/index.html generado:', len(html), 'bytes ·', NM[champ], 'campeón')

if __name__ == '__main__':
    main()
