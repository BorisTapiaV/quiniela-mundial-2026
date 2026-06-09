#!/usr/bin/env python
"""Visor HTML — DEMO INTERMEDIO (torneo en curso) con 12 jugadores.

Estado simulado: la fase de grupos TERMINÓ y arrancan los 16avos. Puntúa solo lo
jugado (72 marcadores + clasificación a R32); las eliminatorias y los especiales
quedan pendientes. Muestra leaderboard parcial, próximos partidos, sub-campeonatos
de grupos, supervivencia de campeones y la carrera en marcha. Salida: site/index.html.

OJO: resultados SIMULADOS — solo para visualizar la UI mientras el torneo está vivo.
"""
import csv, os, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESES = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
def fmtdate(iso):
    y, m, d = iso.split('-'); return f'{int(d)} {MESES[int(m)]}'

STRENGTH = {'ARG':10,'FRA':10,'ESP':9,'BRA':9,'ENG':9,'POR':8,'GER':8,'NED':8,'BEL':7,
            'CRO':7,'URU':6,'COL':6,'MAR':6,'USA':5,'MEX':5,'SUI':5,'JPN':5,'SEN':5,'ECU':5,'NOR':5}
def sth(c): return STRENGTH.get(c, 3)

CUOTA = 10000                                              # cuota por jugador ($10.000)
NO_VALIDADO = {'Andrés Maldonado', 'Joaquín Riquelme'}     # demo: 2 jugadores sin validar
DIST = [0.50, 0.30, 0.20]                                  # reparto 1º / 2º / 3º
def clp(n): return '$' + format(int(n), ',d').replace(',', '.')

def sim_ko(r32, fixture, rng, accuracy=1.0):
    win, lose, out = {}, {}, {}
    ko = sorted([m for m in fixture if m['fase'] != 'grupos'], key=lambda m: m['match_no'])
    def slot(s): return win[int(s[1:])] if s.startswith('W') else lose[int(s[1:])]
    for m in ko:
        mn = m['match_no']
        A, B = r32[mn] if mn in r32 else (slot(m['local']), slot(m['visita']))
        pa = sth(A)/(sth(A)+sth(B)); pa = pa*accuracy + 0.5*(1-accuracy)
        w = A if rng.random() < pa else B
        win[mn] = w; lose[mn] = B if w == A else A; out[mn] = w
    return out

def noisy_group(real_group, rng, acc):
    return {mn: ((gl, gv) if rng.random() < acc else (rng.randint(0,3), rng.randint(0,3)))
            for mn, (gl, gv) in real_group.items()}

def load_mf():
    base = os.path.join(HERE, 'data/predicciones')
    gs = {int(r['match_no']): (int(r['gl']), int(r['gv']))
          for r in csv.DictReader(open(os.path.join(base, 'MF.csv'), encoding='utf-8'))}
    ko = {int(r['match_no']): r['ganador']
          for r in csv.DictReader(open(os.path.join(base, 'MF_ko.csv'), encoding='utf-8'))}
    return gs, ko, {'campeon': '', 'goleador': '', 'primer_eliminado': '', 'sorpresa': ''}

def main():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    ISO = {c: eq[c]['iso'] for c in eq}; NM = {c: eq[c]['nombre_es'] for c in eq}
    fxno = {m['match_no']: m for m in fixture}

    # resultado real SIMULADO con cutoff = OCTAVOS jugados (cuartos por jugar)
    rng = random.Random(7)
    real_group = {m['match_no']: (rng.randint(0,3), rng.randint(0,3)) for m in fixture if m['fase'] == 'grupos'}
    real_r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(real_group, fixture), eq), fixture, terceros)
    real_ko_full = sim_ko(real_r32, fixture, rng, accuracy=0.80)
    real_ko = {mn: w for mn, w in real_ko_full.items() if mn <= 88}          # solo 16avos jugados
    real_view = engine.full_bracket(real_group, real_ko, eq, fixture, terceros)
    real_esp_view = {}                                                       # especiales pendientes
    alive_set = real_view['sets']['R16']                                     # 16 equipos que avanzaron a octavos

    NAMES = ['Manuel Fuentes','Rodrigo Salazar','Felipe Cárdenas','Cristóbal Reyes','Matías Ibáñez',
             'Sebastián Vergara','Diego Fuentealba','Tomás Navarro','Joaquín Riquelme','Ignacio Bravo',
             'Andrés Maldonado','Vicente Cáceres']
    ACC = [None, 0.85, 0.30, 0.62, 0.50, 0.70, 0.25, 0.45, 0.58, 0.40, 0.75, 0.55]
    players = []
    for i, name in enumerate(NAMES):
        prng = random.Random(100 + i)
        if ACC[i] is None:
            gs, ko, esp = load_mf()
        else:
            gs = noisy_group(real_group, prng, ACC[i])
            r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(gs, fixture), eq), fixture, terceros)
            ko = sim_ko(r32, fixture, prng, ACC[i] + 0.2)
            esp = {'campeon': engine.full_bracket(gs, ko, eq, fixture, terceros)['champion']}
        sc = engine.score_player(gs, ko, real_view, real_group, esp, real_esp_view, eq, fixture, terceros)
        h1x2 = sum(1 for mn, (rl, rv) in real_group.items() if engine._outcome(*gs[mn]) == engine._outcome(rl, rv))
        hx = sum(1 for mn, (rl, rv) in real_group.items() if gs[mn] == (rl, rv))
        champ = sc['bracket']['champion']
        players.append({'name': name, 'sc': sc, 'champ': champ, 'h1x2': h1x2, 'hx': hx,
                        'alive': champ in alive_set, 'gs': gs, 'ko': ko, 'esp': esp})
    players.sort(key=lambda p: -p['sc']['total'])
    ranks, miles = compute_evolution(players, real_group, real_ko_full, fixture, eq, terceros)
    render(players, real_view, fxno, NM, ISO, fmtdate, ranks, miles)


def compute_evolution(players, real_group, real_ko_full, fixture, eq, terceros):
    """Puntaje de cada jugador en hitos sucesivos del torneo → ranking por hito (bump chart)."""
    md = {m['match_no']: int(m['matchday']) for m in fixture if m['fase'] == 'grupos'}
    MILES = [('1ª fecha', 1, 0), ('2ª fecha', 2, 0), ('Fin grupos', 3, 0), ('16avos', 3, 88)]
    totals = {p['name']: [] for p in players}
    for _, gmd, komax in MILES:
        rg = {mn: r for mn, r in real_group.items() if md[mn] <= gmd}
        for p in players:
            if gmd < 3:                                  # grupos sin terminar → solo marcadores
                t = sum(engine.score_group_match(p['gs'][mn], rg[mn]) for mn in rg)
            else:
                rk = {mn: w for mn, w in real_ko_full.items() if mn <= komax}
                rv = engine.full_bracket(rg, rk, eq, fixture, terceros)
                t = engine.score_player(p['gs'], p['ko'], rv, rg, p['esp'], {}, eq, fixture, terceros)['total']
            totals[p['name']].append(t)
    ranks = {n: [] for n in totals}
    for i in range(len(MILES)):
        for r, n in enumerate(sorted(totals, key=lambda n: -totals[n][i]), 1):
            ranks[n].append(r)
    return ranks, [m[0] for m in MILES]


def evolution_svg(ranks, miles, order_final):
    W, H, ml, mr, mt, mb = 860, 340, 96, 96, 18, 28
    n = len(miles); N = len(order_final)
    xs = [ml + (W - ml - mr) * i / (n - 1) for i in range(n)]
    def y(rk): return mt + (H - mt - mb) * (rk - 1) / (N - 1)
    COL = ['#ffd24a', '#16d97b', '#5ab0ff', '#ff8aa0']
    s = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,sans-serif">']
    for rk in range(1, N + 1):
        s.append(f'<line x1="{ml}" y1="{y(rk):.0f}" x2="{W-mr}" y2="{y(rk):.0f}" stroke="#222a4a" stroke-width="1"/>')
        s.append(f'<text x="{ml-10}" y="{y(rk)+4:.0f}" fill="#8d97bf" font-size="11" text-anchor="end">{rk}º</text>')
    for i, lab in enumerate(miles):
        s.append(f'<text x="{xs[i]:.0f}" y="{H-8}" fill="#8d97bf" font-size="11" text-anchor="middle">{lab}</text>')
    for idx, name in enumerate(order_final):
        top = idx < 4
        col = COL[idx] if top else '#3c476f'
        pts = ' '.join(f'{xs[i]:.0f},{y(ranks[name][i]):.0f}' for i in range(n))
        s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{3 if top else 1.5}" '
                 f'stroke-linejoin="round" opacity="{1 if top else .55}"/>')
        for i in range(n):
            s.append(f'<circle cx="{xs[i]:.0f}" cy="{y(ranks[name][i]):.0f}" r="{3.5 if top else 2}" fill="{col}"/>')
        s.append(f'<text x="{W-mr+8}" y="{y(ranks[name][-1])+4:.0f}" fill="{col}" font-size="11" '
                 f'font-weight="{700 if top else 400}">{name.split()[-1]}</text>')
    s.append('</svg>')
    return ''.join(s)


def render(players, real_view, fxno, NM, ISO, fmtdate, ranks, miles):
    def flag(c, w=40): return f'<img class="flag" src="https://flagcdn.com/w{w}/{ISO[c]}.png" alt="">'
    maxtot = max(p['sc']['total'] for p in players) or 1
    evo = evolution_svg(ranks, miles, [p['name'] for p in players])
    rey_grupos = max(players, key=lambda p: p['sc']['grupo'])
    rey_1x2 = max(players, key=lambda p: p['h1x2'])
    rey_exacto = max(players, key=lambda p: p['hx'])
    profeta = max(players, key=lambda p: p['sc']['avance'])

    lb = ''
    for i, p in enumerate(players, 1):
        sc = p['sc']; val = p['name'] not in NO_VALIDADO
        badge = '<span class="b dead">💀 su campeón cayó</span>' if not p['alive'] else '<span class="b alive">🟢 sigue vivo</span>'
        medal = ['🥇','🥈','🥉'][i-1] if i <= 3 else f'{i}'
        tick = '<span class="vtick" title="validado">✓</span>' if val else '<span class="vpend" title="sin validar">○</span>'
        lb += (f'<tr class="{"" if val else "unval"}"><td class="rk">{medal}</td>'
               f'<td class="nm">{p["name"]} {tick}</td>'
               f'<td class="cp">{flag(p["champ"])}<span>{NM[p["champ"]]}</span></td>'
               f'<td>{sc["grupo"]}</td><td>{sc["avance"]}</td><td class="tot">{sc["total"]}</td>'
               f'<td>{badge}</td></tr>')

    # panel de premios
    nval = sum(1 for p in players if p['name'] not in NO_VALIDADO)
    pool = nval * CUOTA; prizes = [round(pool * f) for f in DIST]
    prem = ''
    for i, p in enumerate(players[:3]):
        val = p['name'] not in NO_VALIDADO
        med = ['🥇','🥈','🥉'][i]
        st = '<span class="pg">✓ en juego</span>' if val else '<span class="pn">sin validar · no lo cobra</span>'
        prem += (f'<div class="prow{"" if val else " unval"}"><div class="pm">{med} {p["name"]}</div>'
                 f'<div class="pa">{clp(prizes[i])}</div>{st}</div>')

    race = ''
    for p in players:
        g = p['sc']['grupo']; k = p['sc']['avance']; t = g + k
        race += (f'<div class="rrow"><div class="rn">{p["name"]}</div><div class="bar">'
                 f'<div class="seg g" style="width:{100*g/maxtot:.1f}%">{g}</div>'
                 f'<div class="seg k" style="width:{100*k/maxtot:.1f}%">{k or ""}</div></div>'
                 f'<div class="rt">{t}</div></div>')

    # próximos partidos = octavos de final (los 16 equipos ya están definidos)
    prox = ''
    for mn in range(89, 97):
        m = fxno[mn]; a, b = real_view['teams'][mn]
        prox += (f'<div class="px"><div class="pxd">{fmtdate(m["fecha"])} · {m["hora_chile"]}</div>'
                 f'<div class="pxm">{flag(a)}<b>{NM[a]}</b><span class="vs">vs</span>{flag(b)}<b>{NM[b]}</b></div>'
                 f'<div class="pxs">{m["sede"]}</div></div>')

    champ_grid = ''
    for p in sorted(players, key=lambda p: p['name']):
        st = 'dead' if not p['alive'] else 'alive'
        champ_grid += (f'<div class="cg {st}">{flag(p["champ"],80)}<div class="cgn">{p["name"]}</div>'
                       f'<div class="cgc">{"💀 eliminado" if not p["alive"] else "🟢 en carrera"} · {NM[p["champ"]]}</div></div>')

    html = HEAD.replace('{TITLE}', 'En curso · 12 jugadores') + f"""
<header><div class="kick">Copa Mundial FIFA · Canadá · México · EE.UU.</div>
<h1>Quiniela 2026</h1>
<nav><a class="on" href="index.html">Posiciones</a><a href="calendario.html">Calendario</a></nav>
<div class="demo">⚠ DEMO — torneo EN CURSO (resultados simulados)</div></header>

<div class="state">⚽ <b>16avos disputados</b> · 88/104 partidos jugados · quedan 16 equipos ·
arrancan los <b>Octavos de Final</b> · 🏆 campeón aún por definir</div>

<h2 class="sec">🏁 Tabla de posiciones <span class="note">(en curso — grupos + bracket hasta cuartos)</span></h2>
<table class="lead"><tr><th>#</th><th>Jugador</th><th>Su campeón</th><th>Grupos</th><th>KO</th><th>Total</th><th>Estado</th></tr>{lb}</table>

<h2 class="sec">💰 Premios <span class="note">(entregar la planilla basta para jugar; el premio es solo para quien valida)</span></h2>
<div class="pot">Pozo actual <b>{clp(pool)}</b> · {nval}/12 validados · cuota {clp(CUOTA)}<span class="potnote">reparto 🥇 50% · 🥈 30% · 🥉 20%</span></div>
<div class="prizes">{prem}</div>
<div class="potfoot">El que no valida igual aparece y ve <b>lo que dejaría de ganar</b> — pero no lo cobra.</div>

<h2 class="sec">📈 Evolución del ranking <span class="note">(posición por hito — cada cruce de líneas es un adelantamiento; ⭐ se llena fecha a fecha)</span></h2>
<div class="evo">{evo}</div>

<h2 class="sec">📊 La carrera <span class="note">(de dónde salió el puntaje · verde = grupos · dorado = eliminatorias)</span></h2>
<div class="race">{race}</div>

<h2 class="sec">📅 Próximos partidos · Octavos de Final</h2>
<div class="prox">{prox}</div>

<h2 class="sec">🏅 Sub-campeonatos y récords</h2>
<div class="subs">
<div class="subc"><div class="t">👑 Rey de la fase de grupos</div><div class="w">{rey_grupos['name']}</div><div class="x">{rey_grupos['sc']['grupo']} pts</div></div>
<div class="subc"><div class="t">🔮 El Profeta (bracket)</div><div class="w">{profeta['name']}</div><div class="x">{profeta['sc']['avance']} pts de avance</div></div>
<div class="subc"><div class="t">🎯 Rey del 1X2</div><div class="w">{rey_1x2['name']}</div><div class="x">{rey_1x2['h1x2']} resultados</div></div>
<div class="subc"><div class="t">🎯 Rey del marcador exacto</div><div class="w">{rey_exacto['name']}</div><div class="x">{rey_exacto['hx']} clavados</div></div>
</div>

<h2 class="sec">💀 Supervivencia de campeones <span class="note">(¿tu campeón sigue en carrera?)</span></h2>
<div class="cgrid">{champ_grid}</div>

<footer>Banderas: flagcdn.com · datos de demostración · gen_demo_site.py</footer>
</div></body></html>"""
    os.makedirs(os.path.join(HERE, 'site'), exist_ok=True)
    with open(os.path.join(HERE, 'site', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('site/index.html (intermedio) generado:', len(html), 'bytes')
    print('Líder:', players[0]['name'], players[0]['sc']['total'],
          '· campeones caídos:', sum(1 for p in players if not p['alive']), '/12')


HEAD = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Quiniela Mundial 2026 · {TITLE}</title>
<style>
:root{--bg:#0b1020;--card:#151c34;--line:#2a3358;--txt:#e8ecf7;--mut:#8d97bf;--green:#16d97b;--gold:#ffd24a;}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(180deg,#0b1020,#0e1530);color:var(--txt);font:15px/1.45 system-ui,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:24px}
header{text-align:center;padding:24px 0 6px}.kick{color:var(--gold);letter-spacing:.18em;font-size:12px;text-transform:uppercase}
h1{margin:6px 0 4px;font-size:30px}
nav{display:flex;gap:8px;justify-content:center;margin:8px 0}
nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:5px 14px;border:1px solid var(--line);border-radius:20px}
nav a.on{color:#06210f;background:var(--gold);border-color:var(--gold);font-weight:700}
.demo{display:inline-block;margin-top:10px;background:#3a2c1a;border:1px solid #5a431f;color:var(--gold);font-size:12px;padding:5px 12px;border-radius:20px}
.state{text-align:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;margin:16px 0;color:var(--txt);font-size:14px}
h2.sec{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);border-bottom:1px solid var(--line);padding-bottom:8px;margin:32px 0 14px}
h2.sec .note{text-transform:none;letter-spacing:0;font-size:12px;color:var(--mut);font-weight:400}
table.lead{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden}
.lead th,.lead td{padding:9px 10px;text-align:center;border-bottom:1px solid var(--line);font-size:13px}
.lead th{color:var(--mut);font-weight:600;font-size:11px;text-transform:uppercase}
.lead td.nm{text-align:left;font-weight:600}.lead td.rk{font-size:16px;width:34px}
.lead td.cp{text-align:left}.lead td.cp .flag{width:22px;border-radius:3px;vertical-align:-4px;margin-right:6px}
.lead td.tot{font-weight:800;color:var(--gold);font-size:15px}.lead tr:nth-child(1) td{background:#1b2547}
.b{font-size:11px;padding:2px 8px;border-radius:20px;white-space:nowrap}
.b.dead{background:#3a1620;color:#ff8aa0}.b.alive{background:#10301f;color:var(--green)}
.flag{box-shadow:0 1px 3px #0007}
.race{display:flex;flex-direction:column;gap:7px}
.rrow{display:grid;grid-template-columns:130px 1fr 46px;align-items:center;gap:10px}
.rn{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bar{display:flex;height:24px;border-radius:6px;overflow:hidden;background:#0d1430}
.seg{display:flex;align-items:center;justify-content:flex-end;padding:0 6px;font-size:11px;font-weight:700;color:#06210f;min-width:0;overflow:hidden}
.seg.g{background:var(--green)}.seg.k{background:var(--gold)}
.rt{text-align:right;font-weight:800;color:var(--gold)}
.evo svg{display:block;width:100%;height:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px}
.lead tr.unval{opacity:.5}.vtick{color:var(--green);font-weight:700;margin-left:4px}.vpend{color:var(--mut);margin-left:4px}
.pot{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center}
.pot b{color:var(--gold);font-size:19px}.potnote{display:block;color:var(--mut);font-size:12px;margin-top:4px}
.prizes{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px}
.prow{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center}
.prow.unval{opacity:.5;border-style:dashed}.pm{font-weight:600;font-size:13px}
.pa{font-size:22px;font-weight:800;color:var(--gold);margin:6px 0}.pg{color:var(--green);font-size:12px}.pn{color:#ff8aa0;font-size:12px}
.potfoot{text-align:center;color:var(--mut);font-size:12px;margin-top:8px}
@media(max-width:600px){.prizes{grid-template-columns:1fr}}
.prox{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.px{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.pxd{color:var(--gold);font-size:12px}.pxs{color:var(--mut);font-size:11px;margin-top:4px}
.pxm{display:flex;align-items:center;gap:6px;margin:5px 0;font-size:13px}
.pxm .flag{width:22px;border-radius:3px}.pxm .vs{color:var(--mut);margin:0 2px}
.subs{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.subc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.subc .t{font-size:12px;color:var(--mut)}.subc .w{font-size:18px;font-weight:700;margin-top:4px}.subc .x{color:var(--gold);font-size:13px}
.cgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.cg{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;text-align:center}
.cg.dead{opacity:.5}.cg .flag{width:54px;border-radius:4px}.cgn{font-weight:600;font-size:13px;margin-top:6px}
.cgc{color:var(--mut);font-size:12px;margin-top:2px}
footer{text-align:center;color:var(--mut);font-size:12px;margin:34px 0 10px}
</style></head><body><div class="wrap">"""

if __name__ == '__main__':
    main()
