#!/usr/bin/env python
"""Galería pública + leaderboard (post-cierre) — Mundial 2026.

Página pública que combina:
  · LEADERBOARD: ranking de todos los jugadores (motor vs data/resultados*.csv).
  · GALERÍA: grid con cada jugador -> link a su página individual site/p/<slug>.html.
  · Secciones ricas (carrera, evolución, sub-campeonatos, supervivencia, premios)
    que aparecen SOLO cuando ya hay resultados.

Estado dinámico: por comenzar / grupos en curso / grupos listos / KO en curso / cerrado.
Reusa los helpers del demo (gen_demo_site) sin reescribirlos.

Datos reales:
  data/predicciones/<slug>.csv (+_ko +_especiales)  — predicciones ingeridas (excluye CASA)
  data/resultados.csv            match_no,gl,gv      — grupos jugados (parcial)
  data/resultados_ko.csv         match_no,ganador    — llaves KO jugadas (parcial)
  data/resultados_especiales.csv clave,valor         — campeón/goleador/... conocidos
  data/validados.csv             slug (uno por línea)— quién validó (premio). Ausente=todos.

Uso:
  python build/gen_galeria.py            # datos reales -> site/index.html (portada)
  python build/gen_galeria.py --demo     # 10 jugadores sintéticos + resultado parcial (previsualizar)
"""
import csv, os, sys, random, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine
import gen_demo_site as demo            # helpers: sim_ko, noisy_group, load_mf, compute_evolution, evolution_svg, clp, fmtdate, HEAD, CUOTA, DIST
import snapshot                          # delta ▲▼ por jornada (vs último cierre)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(HERE, 'data', 'predicciones')
SITE = os.path.join(HERE, 'site')
SITE_URL = 'https://quiniela-mundial-2026-1780886848.netlify.app'
DENY = {'CASA'}
APODOS_DEMO = {'Manuel Fuentes': 'El Profe', 'Rodrigo Salazar': 'Rodo', 'Felipe Cárdenas': 'Pipe',
               'Cristóbal Reyes': 'Cris', 'Matías Ibáñez': 'Mati', 'Sebastián Vergara': 'Seba',
               'Diego Fuentealba': 'El Mago', 'Tomás Navarro': 'Tomi', 'Ignacio Bravo': 'Nacho',
               'Vicente Cáceres': 'Vicho'}


def slug_url(slug):
    return slug.lower().replace('_', '-')


def display_name(slug):
    return ' '.join(w.capitalize() for w in slug.replace('_', ' ').split())


def load_apodos():
    """data/apodos.csv (slug,apodo) opcional → dict. Gancho nominal (research #1: identidad)."""
    p = os.path.join(HERE, 'data', 'apodos.csv')
    d = {}
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('apodo'):
                d[r['slug']] = r['apodo'].strip()
    return d


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


def discover_slugs():
    out = []
    for fn in sorted(os.listdir(PRED)):
        if fn.endswith('.csv') and not fn.endswith('_ko.csv') and not fn.endswith('_especiales.csv'):
            slug = fn[:-4]
            if slug in DENY:
                continue
            if all(os.path.exists(os.path.join(PRED, f'{slug}{s}.csv')) for s in ('_ko', '_especiales')):
                out.append(slug)
    return out


def load_results():
    """Lee resultados reales (parciales). Devuelve (real_group, real_ko, real_esp)."""
    rg, rk, re_ = {}, {}, {}
    p = os.path.join(HERE, 'data', 'resultados.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('gl') not in (None, '') and r.get('gv') not in (None, ''):
                    rg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    p = os.path.join(HERE, 'data', 'resultados_ko.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('ganador'):
                    rk[int(r['match_no'])] = r['ganador']
    p = os.path.join(HERE, 'data', 'resultados_especiales.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('valor'):
                    re_[r['clave']] = r['valor']
    return rg, rk, re_


def survivors_set(real_group, real_ko, real_view, eq, fixture, terceros):
    """Equipos aún NO eliminados (para el badge 'sigue vivo')."""
    allteams = set(eq)
    if len(real_group) < 72:
        return allteams                              # grupos no terminados -> nadie eliminado
    r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(real_group, fixture), eq), fixture, terceros)
    qualified = set()
    for a, b in r32.values():
        qualified.add(a); qualified.add(b)
    losers = set()
    for mn, w in real_ko.items():
        a, b = real_view['teams'].get(mn, (None, None))
        if a and b:
            losers.add(b if w == a else a)
    return qualified - losers


def build_players(slugs, real_view, real_group, real_esp, eq, fixture, terceros, survivors, validated):
    apodos = load_apodos()
    players = []
    for slug in slugs:
        gs, ko, esp = load_pred(slug)
        sc = engine.score_player(gs, ko, real_view, real_group, esp, real_esp, eq, fixture, terceros)
        champ = sc['bracket']['champion']
        h1x2 = sum(1 for mn, (rl, rv) in real_group.items()
                   if mn in gs and engine._outcome(*gs[mn]) == engine._outcome(rl, rv))
        hx = sum(1 for mn, (rl, rv) in real_group.items() if gs.get(mn) == (rl, rv))
        players.append({'slug': slug, 'name': esp.get('jugador') or display_name(slug), 'url': f'p/{slug_url(slug)}.html',
                        'apodo': apodos.get(slug, ''),
                        'sc': sc, 'champ': champ, 'h1x2': h1x2, 'hx': hx,
                        'gs': gs, 'ko': ko, 'esp': esp,
                        'alive': champ in survivors, 'validated': (validated is None or slug in validated)})
    players.sort(key=lambda p: (-p['sc']['total'], -p['hx'], p['slug']))
    # delta ▲▼ vs el último snapshot de jornada (data/historico/)
    prev = snapshot.read_last()
    for i, p in enumerate(players, 1):
        pe = prev.get(p['slug'])
        p['delta'] = (pe['pos'] - i) if pe else None
    return players


def state_line(real_group, real_ko, real_view, NM):
    ng, nk = len(real_group), len(real_ko)
    champ = real_view['win'].get(104)
    if ng == 0:
        return False, '🗓️ El torneo aún no comienza — los pronósticos están <b>sellados</b>. La tabla se moverá con cada resultado.'
    if ng < 72:
        return True, f'⚽ <b>Fase de grupos en curso</b> · {ng}/72 partidos jugados'
    if nk == 0:
        return True, '✅ <b>Fase de grupos terminada</b> · arrancan las eliminatorias'
    if not champ:
        return True, f'⚔️ <b>Eliminatorias en curso</b> · {nk}/32 llaves resueltas'
    return True, f'🏆 <b>Torneo cerrado</b> · campeón <b>{NM.get(champ, champ)}</b>'


def render(players, has_results, state, real_view, fxno, NM, ISO, ranks, miles, is_demo):
    def flag(c, w=40):
        return f'<img class="flag" src="https://flagcdn.com/w{w}/{ISO[c]}.png" alt="">' if c in ISO else ''

    def apo(p):
        return f'<span class="apo">«{p["apodo"]}»</span>' if p.get('apodo') else ''

    # ---- galería (siempre) ----
    gallery = ''
    for p in sorted(players, key=lambda p: p['name']):
        ch = f'{flag(p["champ"], 60)}<div class="ggc">🏆 {NM.get(p["champ"], p["champ"])}</div>' if p['champ'] else '<div class="ggc">—</div>'
        gallery += (f'<a class="gg" href="{p["url"]}">{ch}'
                    f'<div class="ggn">{p["name"]}</div>{apo(p)}'
                    f'<div class="ggl">ver mi pronóstico →</div></a>')

    # ---- leaderboard (siempre; 0 si no hay resultados) ----
    show_delta = any(p.get('delta') is not None for p in players)

    def darrow(d):
        if d is None:
            return '<span class="eq">—</span>'
        if d > 0:
            return f'<span class="up">▲{d}</span>'
        if d < 0:
            return f'<span class="dn">▼{abs(d)}</span>'
        return '<span class="eq">=</span>'

    lb = ''
    for i, p in enumerate(players, 1):
        sc = p['sc']
        medal = ['🥇', '🥈', '🥉'][i - 1] if i <= 3 else f'{i}'
        tick = '<span class="vtick" title="validado">✓</span>' if p['validated'] else '<span class="vpend" title="sin validar">○</span>'
        if has_results:
            badge = '<span class="b dead">💀 su campeón cayó</span>' if not p['alive'] else '<span class="b alive">🟢 vivo</span>'
        else:
            badge = '<span class="b seal">🔒 sellado</span>'
        ch = f'{flag(p["champ"], 40)}<span>{NM.get(p["champ"], p["champ"])}</span>' if p['champ'] else '—'
        dcell = f'<td class="dl">{darrow(p.get("delta"))}</td>' if show_delta else ''
        lb += (f'<tr class="{"" if p["validated"] else "unval"}"><td class="rk">{medal}</td>'
               f'<td class="nm"><a href="{p["url"]}">{p["name"]}</a> {tick}{apo(p)}</td>'
               f'<td class="cp">{ch}</td>'
               f'<td>{sc["grupo"]}</td><td>{sc["avance"]}</td><td class="tot">{sc["total"]}</td>'
               f'{dcell}<td>{badge}</td></tr>')

    # ---- premios (pozo siempre; asignación al top-3 solo con resultados) ----
    nval = sum(1 for p in players if p['validated'])
    pool = nval * demo.CUOTA
    prizes = [round(pool * f) for f in demo.DIST]
    pot = (f'<div class="pot">Pozo actual <b>{demo.clp(pool)}</b> · {nval}/{len(players)} validados · '
           f'cuota {demo.clp(demo.CUOTA)}<span class="potnote">reparto 🥇 50% · 🥈 30% · 🥉 20%</span></div>')
    if has_results:
        prows = ''
        for i, p in enumerate(players[:3]):
            med = ['🥇', '🥈', '🥉'][i]
            st = '<span class="pg">✓ en juego</span>' if p['validated'] else '<span class="pn">sin validar · no lo cobra</span>'
            prows += (f'<div class="prow{"" if p["validated"] else " unval"}"><div class="pm">{med} {p["name"]}</div>'
                      f'<div class="pa">{demo.clp(prizes[i])}</div>{st}</div>')
        premios = (f'<h2 class="sec">💰 Premios</h2>{pot}<div class="prizes">{prows}</div>'
                   '<div class="potfoot">El que no valida igual aparece y ve <b>lo que dejaría de ganar</b> — pero no lo cobra.</div>')
    else:
        premios = (f'<h2 class="sec">💰 Premios <span class="note">(el pozo crece con cada jugador que valida)</span></h2>{pot}'
                   '<div class="potfoot">Entregar la planilla basta para jugar; el premio es solo para quien valida. '
                   'Al cerrar el torneo, aquí se reparte el pozo entre el top 3.</div>')

    rich = ''
    if has_results:
        maxtot = max((p['sc']['total'] for p in players), default=1) or 1
        # carrera
        race = ''
        for p in players:
            g, k = p['sc']['grupo'], p['sc']['avance']
            race += (f'<div class="rrow"><div class="rn">{p["name"]}</div><div class="bar">'
                     f'<div class="seg g" style="width:{100*g/maxtot:.1f}%">{g or ""}</div>'
                     f'<div class="seg k" style="width:{100*k/maxtot:.1f}%">{k or ""}</div></div>'
                     f'<div class="rt">{g+k}</div></div>')
        # sub-campeonatos
        rg_ = max(players, key=lambda p: p['sc']['grupo'])
        pf = max(players, key=lambda p: p['sc']['avance'])
        r1 = max(players, key=lambda p: p['h1x2'])
        rx = max(players, key=lambda p: p['hx'])
        # supervivencia
        cg = ''
        for p in sorted(players, key=lambda p: p['name']):
            st = 'dead' if not p['alive'] else 'alive'
            cg += (f'<div class="cg {st}">{flag(p["champ"], 80)}<div class="cgn">{p["name"]}</div>'
                   f'<div class="cgc">{"💀 eliminado" if not p["alive"] else "🟢 en carrera"} · {NM.get(p["champ"], p["champ"])}</div></div>')
        # Liga de Consolación (ESPN ladder): los de fuera del podio compiten aparte
        cons_html = ''
        if len(players) > 3:
            crows = ''
            for j, p in enumerate(players[3:], 1):
                med = '🏅' if j == 1 else str(j + 3)
                deadc = '' if p['alive'] else 'dead'
                crows += (f'<tr class="{deadc}"><td class="rk">{med}</td>'
                          f'<td class="nm">{flag(p["champ"], 22)}<span>{p["name"]}</span>{apo(p)}</td>'
                          f'<td class="tot">{p["sc"]["total"]}</td></tr>')
            cons_html = (
                '<h2 class="sec">🪜 Liga de Consolación '
                '<span class="note">(el campeonato de los que hoy están fuera del podio — aquí hasta el último pelea su propia corona)</span></h2>'
                f'<table class="lead cons"><tr><th>#</th><th>Jugador</th><th>Total</th></tr>{crows}</table>')
        evo = demo.evolution_svg(ranks, miles, [p['name'] for p in players]) if ranks else ''
        evo_sec = f'<h2 class="sec">📈 Evolución del ranking</h2><div class="evo">{evo}</div>' if evo else ''
        rich = f"""
<h2 class="sec">📊 La carrera <span class="note">(verde = grupos · dorado = eliminatorias)</span></h2>
<div class="race">{race}</div>
{evo_sec}
<h2 class="sec">🏅 Sub-campeonatos</h2>
<div class="subs">
<div class="subc"><div class="t">👑 Rey de la fase de grupos</div><div class="w">{rg_['name']}</div><div class="x">{rg_['sc']['grupo']} pts</div></div>
<div class="subc"><div class="t">🔮 El Profeta (bracket)</div><div class="w">{pf['name']}</div><div class="x">{pf['sc']['avance']} pts de avance</div></div>
<div class="subc"><div class="t">🎯 Rey del 1X2</div><div class="w">{r1['name']}</div><div class="x">{r1['h1x2']} resultados</div></div>
<div class="subc"><div class="t">🎯 Rey del marcador exacto</div><div class="w">{rx['name']}</div><div class="x">{rx['hx']} clavados</div></div>
</div>
<h2 class="sec">💀 Supervivencia de campeones</h2>
<div class="cgrid">{cg}</div>
{cons_html}"""

    demobanner = '<div class="demo">⚠ VISTA DEMO — jugadores y resultados de muestra</div>' if is_demo else ''
    lead_note = '' if has_results else '<div class="note2">La tabla está en cero hasta que arranque el torneo. Mientras, cada jugador ya puede ver su pronóstico en la galería ↓</div>'

    # Open Graph (preview del link al pegarlo en WhatsApp) + botón Compartir al grupo
    og = (f'<meta property="og:title" content="Quiniela Mundial 2026">'
          f'<meta property="og:description" content="Mira cómo va la tabla — ¿sigues vivo?">'
          f'<meta property="og:image" content="{SITE_URL}/og.png">'
          f'<meta property="og:url" content="{SITE_URL}/"><meta property="og:type" content="website">'
          f'<meta name="twitter:card" content="summary_large_image">')
    share_text = urllib.parse.quote(f'📊 Quiniela Mundial 2026 — mira cómo va la tabla 👀\n{SITE_URL}/')
    share_href = f'https://wa.me/?text={share_text}'

    head = demo.HEAD.replace('{TITLE}', 'Pronósticos y tabla').replace('</head>', og + '</head>')
    html = head + EXTRA_CSS + f"""
<header><div class="kick">Copa Mundial FIFA · Canadá · México · EE.UU.</div>
<h1>Quiniela 2026</h1>
<nav><a class="on" href="index.html">Posiciones</a><a href="calendario.html">Calendario</a></nav>
<a class="share" href="{share_href}" target="_blank" rel="noopener">📲 Compartir al grupo</a>
{demobanner}</header>

<div class="state">{state}</div>

<h2 class="sec">🏁 Tabla de posiciones</h2>
{lead_note}
<table class="lead"><tr><th>#</th><th>Jugador</th><th>Su campeón</th><th>Grupos</th><th>KO</th><th>Total</th>{'<th title="cambio desde la jornada anterior">±</th>' if show_delta else ''}<th>Estado</th></tr>{lb}</table>

{premios}

<h2 class="sec">🖼️ Galería de pronósticos <span class="note">(click en un jugador para ver su cuadro completo)</span></h2>
<div class="ggrid">{gallery}</div>
{rich}
<footer>Banderas: flagcdn.com (dominio público) · gen_galeria.py{' · datos de muestra' if is_demo else ''}</footer>
</div></body></html>"""

    os.makedirs(SITE, exist_ok=True)
    out = os.path.join(SITE, 'index.html')           # la galería + leaderboard ES la portada
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    return out


EXTRA_CSS = """<style>
.share{display:inline-block;margin:12px auto 0;background:#25d366;color:#06210f;font-weight:800;
font-size:14px;text-decoration:none;padding:9px 20px;border-radius:24px;box-shadow:0 4px 14px #25d36644}
.share:hover{background:#1ebe5a}
header{display:flex;flex-direction:column;align-items:center}
.note2{text-align:center;color:var(--mut);font-size:13px;margin:-6px 0 12px}
.b.seal{background:#23284a;color:var(--mut)}
.lead td.nm a{color:var(--txt);text-decoration:none;border-bottom:1px dotted var(--line)}
.lead td.nm a:hover{color:var(--gold)}
.lead td.dl{text-align:center;width:56px;font-weight:700}
.up{color:#16d97b}.dn{color:#ff8aa0}.eq{color:#5a648c}
.lead.cons td.tot{color:#b9c2e8}
.apo{color:#ffd24a;font-size:12px;font-weight:600;font-style:italic;margin-left:6px}
.gg .apo{display:block;margin:2px 0 0}
.ggrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.gg{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 12px;text-align:center;text-decoration:none;color:var(--txt);transition:.15s}
.gg:hover{border-color:var(--gold);transform:translateY(-2px)}
.gg .flag{width:50px;border-radius:5px;box-shadow:0 3px 10px #0007}
.ggc{color:var(--gold);font-size:12px;margin-top:8px}
.ggn{font-weight:700;font-size:15px;margin-top:6px}
.ggl{color:var(--mut);font-size:12px;margin-top:6px}
</style>"""


# -------------------- modos --------------------
def run_real():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    ISO = {c: eq[c]['iso'] for c in eq}; NM = {c: eq[c]['nombre_es'] for c in eq}
    fxno = {m['match_no']: m for m in fixture}
    slugs = discover_slugs()
    if not slugs:
        print('No hay predicciones de jugadores ingeridas (excluyendo La Casa). Ingiere plantillas con ingest_plantilla.py primero.')
        return
    rg, rk, re_ = load_results()
    real_view = engine.full_bracket(rg, rk, eq, fixture, terceros)
    surv = survivors_set(rg, rk, real_view, eq, fixture, terceros)
    vfile = os.path.join(HERE, 'data', 'validados.csv')
    validated = None
    if os.path.exists(vfile):
        validated = {line.strip() for line in open(vfile, encoding='utf-8') if line.strip()}
    players = build_players(slugs, real_view, rg, re_, eq, fixture, terceros, surv, validated)
    has, state = state_line(rg, rk, real_view, NM)
    ranks = miles = None
    if has and len(rg) > 0:
        ranks, miles = demo.compute_evolution(players, rg, rk, fixture, eq, terceros)
    out = render(players, has, state, real_view, fxno, NM, ISO, ranks, miles, is_demo=False)
    print(f'{out} generado · {len(players)} jugadores · estado: {"con resultados" if has else "pre-torneo"}')


def run_demo():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    ISO = {c: eq[c]['iso'] for c in eq}; NM = {c: eq[c]['nombre_es'] for c in eq}
    fxno = {m['match_no']: m for m in fixture}
    rng = random.Random(7)
    rg = {m['match_no']: (rng.randint(0, 3), rng.randint(0, 3)) for m in fixture if m['fase'] == 'grupos'}
    r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(rg, fixture), eq), fixture, terceros)
    rk_full = demo.sim_ko(r32, fixture, rng, accuracy=0.80)
    rk = {mn: w for mn, w in rk_full.items() if mn <= 96}      # 16avos+octavos jugados
    real_view = engine.full_bracket(rg, rk, eq, fixture, terceros)
    surv = survivors_set(rg, rk, real_view, eq, fixture, terceros)
    NAMES = ['Manuel Fuentes', 'Rodrigo Salazar', 'Felipe Cárdenas', 'Cristóbal Reyes', 'Matías Ibáñez',
             'Sebastián Vergara', 'Diego Fuentealba', 'Tomás Navarro', 'Ignacio Bravo', 'Vicente Cáceres']
    ACC = [None, 0.85, 0.30, 0.62, 0.50, 0.70, 0.25, 0.45, 0.40, 0.55]
    unval = {'Diego Fuentealba', 'Vicente Cáceres'}
    players = []
    for i, name in enumerate(NAMES):
        prng = random.Random(100 + i)
        if ACC[i] is None:
            gs, ko, esp = demo.load_mf()
        else:
            gs = demo.noisy_group(rg, prng, ACC[i])
            r = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(gs, fixture), eq), fixture, terceros)
            ko = demo.sim_ko(r, fixture, prng, ACC[i] + 0.2)
            esp = {'campeon': engine.full_bracket(gs, ko, eq, fixture, terceros)['champion']}
        sc = engine.score_player(gs, ko, real_view, rg, esp, {}, eq, fixture, terceros)
        champ = sc['bracket']['champion']
        h1x2 = sum(1 for mn, (rl, rv) in rg.items() if engine._outcome(*gs[mn]) == engine._outcome(rl, rv))
        hx = sum(1 for mn, (rl, rv) in rg.items() if gs[mn] == (rl, rv))
        slug = name.upper().replace(' ', '_')
        players.append({'slug': slug, 'name': name, 'url': f'p/{slug_url(slug)}.html', 'sc': sc,
                        'apodo': APODOS_DEMO.get(name, ''),
                        'champ': champ, 'h1x2': h1x2, 'hx': hx, 'gs': gs, 'ko': ko, 'esp': esp,
                        'alive': champ in surv, 'validated': name not in unval})
    players.sort(key=lambda p: (-p['sc']['total'], -p['hx'], p['slug']))
    # delta ▲▼ demo: comparar contra el corte previo (16avos jugados, <=88)
    rk_prev = {mn: w for mn, w in rk_full.items() if mn <= 88}
    rv_prev = engine.full_bracket(rg, rk_prev, eq, fixture, terceros)
    ptot = {p['slug']: engine.score_player(p['gs'], p['ko'], rv_prev, rg, p['esp'], {}, eq, fixture, terceros)['total'] for p in players}
    porder = sorted(ptot, key=lambda s: -ptot[s]); ppos = {s: i + 1 for i, s in enumerate(porder)}
    for i, p in enumerate(players, 1):
        p['delta'] = ppos[p['slug']] - i
    ranks, miles = demo.compute_evolution(players, rg, rk_full, fixture, eq, terceros)
    has, state = state_line(rg, rk, real_view, NM)
    out = render(players, has, state, real_view, fxno, NM, ISO, ranks, miles, is_demo=True)
    print(f'{out} (DEMO) generado · {len(players)} jugadores · líder {players[0]["name"]} {players[0]["sc"]["total"]}')


if __name__ == '__main__':
    if '--demo' in sys.argv:
        run_demo()
    else:
        run_real()
