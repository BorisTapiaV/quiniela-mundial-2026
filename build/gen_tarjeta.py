#!/usr/bin/env python
"""Tarjeta diaria compartible para WhatsApp (recap de LIGA COMPLETA).

Decisión deep-research (2026-06-09): el contenido compartible debe cubrir a TODOS
los jugadores (no individual) para generar conversación y reenvío en el grupo
(Yahoo recap [VALIDADO]). La tarjeta junta las mecánicas validadas:
  · 👑 Rey de la jornada (Kicktipp)         · 📈/📉 delta de posiciones (Kicktipp)
  · 💀 supervivencia de campeones           · 🏆 líder actual
y lleva el LINK del sitio para re-entrada.

Genera una imagen PNG (HTML → render Edge headless) que el organizador manda al
grupo de WhatsApp manualmente (Opción A, $0, sin backend).

Uso:
  python build/gen_tarjeta.py --demo      # tarjeta de muestra (torneo simulado) -> render PNG
  python build/gen_tarjeta.py             # datos reales (predicciones + resultados)
"""
import csv, os, sys, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine
import gen_demo_site as demo

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(HERE, 'data', 'predicciones')
OUTDIR = os.path.join(HERE, 'tarjetas')
SITE_URL = '2026-mundial.netlify.app'
DENY = set()                        # La Casa (Boris Tapia V) pública, cuenta en el recap. {'CASA'} para ocultarla.


def display_name(slug):
    return ' '.join(w.capitalize() for w in slug.replace('_', ' ').split())


# ---------- scoring a un corte ----------
def score_at(players, rg_cut, rk_cut, eq, fixture, terceros):
    """Devuelve dict slug->total con resultados hasta el corte dado."""
    rv = engine.full_bracket(rg_cut, rk_cut, eq, fixture, terceros)
    out = {}
    for p in players:
        sc = engine.score_player(p['gs'], p['ko'], rv, rg_cut, p['esp'], {}, eq, fixture, terceros)
        out[p['slug']] = sc['total']
    return out, rv


def ranks_from(totals):
    order = sorted(totals, key=lambda s: -totals[s])
    return {slug: i + 1 for i, slug in enumerate(order)}


def build_state(players, rg_now, rk_now, prev_map, eq, fixture, terceros, NM, ISO, jornada_label):
    """prev_map = {slug: {'total':int,'pos':int}} del snapshot anterior (o {} si no hay)."""
    t_now, rv_now = score_at(players, rg_now, rk_now, eq, fixture, terceros)
    r_now = ranks_from(t_now)
    by = {p['slug']: p for p in players}
    rows = []
    for slug in sorted(t_now, key=lambda s: -t_now[s]):
        p = by[slug]
        pe = prev_map.get(slug)
        rows.append({
            'slug': slug, 'name': p['name'], 'champ': p['champ'],
            'total': t_now[slug],
            'round_pts': t_now[slug] - (pe['total'] if pe else 0),   # vs snapshot anterior (o todo si 1ª jornada)
            'delta': (pe['pos'] - r_now[slug]) if pe else None,       # + = subió · None = sin referencia
            'pos': r_now[slug],
        })
    # equipos aún vivos (no eliminados) para badge campeón
    surv = survivors(rg_now, rk_now, rv_now, eq, fixture, terceros)
    for r in rows:
        r['alive'] = r['champ'] in surv
    lider = rows[0]
    rey = max(rows, key=lambda r: r['round_pts'])
    movers = [r for r in rows if r['delta'] is not None]
    subio = max(movers, key=lambda r: r['delta']) if movers else None
    cayo = min(movers, key=lambda r: r['delta']) if movers else None
    muertos = [r for r in rows if not r['alive']]
    return {'rows': rows, 'lider': lider, 'rey': rey, 'subio': subio, 'cayo': cayo,
            'muertos': muertos, 'jornada': jornada_label, 'NM': NM, 'ISO': ISO}


def survivors(rg, rk, rv, eq, fixture, terceros):
    allt = set(eq)
    if len(rg) < 72:
        return allt
    r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(rg, fixture), eq), fixture, terceros)
    qual = set()
    for a, b in r32.values():
        qual.add(a); qual.add(b)
    losers = set()
    for mn, w in rk.items():
        a, b = rv['teams'].get(mn, (None, None))
        if a and b:
            losers.add(b if w == a else a)
    return qual - losers


# ---------- render ----------
def flag(code, ISO, w=40):
    return f'<img class="fl" src="https://flagcdn.com/w{w}/{ISO[code]}.png" alt="">' if code in ISO else ''


_LOGO_CACHE = None
def logo_data_uri():
    """Escudo 'Fisioterapia & Futbolito FC' embebido en base64 (self-contained:
    la tarjeta se renderiza vía file:// y se comparte como PNG, sin depender de rutas)."""
    global _LOGO_CACHE
    if _LOGO_CACHE is None:
        import base64
        p = os.path.join(HERE, 'site', 'fisio-fc.png')
        if os.path.exists(p):
            with open(p, 'rb') as f:
                _LOGO_CACHE = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
        else:
            _LOGO_CACHE = ''
    return _LOGO_CACHE


def render(st, fecha_label):
    NM, ISO = st['NM'], st['ISO']
    lider, rey, subio, cayo = st['lider'], st['rey'], st['subio'], st['cayo']

    def arrow(d):
        if d is None:
            return '<span class="eq">—</span>'
        if d > 0:
            return f'<span class="up">▲{d}</span>'
        if d < 0:
            return f'<span class="dn">▼{abs(d)}</span>'
        return '<span class="eq">=</span>'

    # tiles de movimiento (pueden no existir si es la 1ª jornada / sin snapshot previo)
    subio_name = subio['name'].split()[0] if subio else '—'
    subio_x = f"▲{subio['delta']}" if (subio and subio['delta'] > 0) else '—'
    cayo_name = cayo['name'].split()[0] if cayo else '—'
    cayo_x = f"▼{abs(cayo['delta'])}" if (cayo and cayo['delta'] < 0) else '—'

    # mini-tabla: top 5 + el último (cubrir liga completa, incl. el del fondo)
    rows = st['rows']
    shown = rows[:5]
    tail = None
    if len(rows) > 6:
        tail = rows[-1]
    elif len(rows) == 6:
        shown = rows
    trs = ''
    for r in shown:
        medal = ['🥇', '🥈', '🥉'][r['pos'] - 1] if r['pos'] <= 3 else str(r['pos'])
        dead = ' dead' if not r['alive'] else ''
        trs += (f'<tr class="{dead.strip()}"><td class="rk">{medal}</td>'
                f'<td class="nm">{flag(r["champ"], ISO, 20)}{r["name"]}</td>'
                f'<td class="tot">{r["total"]}</td><td class="dl">{arrow(r["delta"])}</td></tr>')
    if tail:
        trs += ('<tr class="tailgap"><td colspan="4">· · ·</td></tr>'
                f'<tr class="tail"><td class="rk">{tail["pos"]}</td>'
                f'<td class="nm">{flag(tail["champ"], ISO, 20)}{tail["name"]}</td>'
                f'<td class="tot">{tail["total"]}</td><td class="dl">{arrow(tail["delta"])}</td></tr>')

    muertos = st['muertos']
    muertos_html = ''
    if muertos:
        nombres = ', '.join(m['name'].split()[0] for m in muertos[:4])
        extra = f' +{len(muertos) - 4}' if len(muertos) > 4 else ''
        muertos_html = f'<div class="muertos">💀 Campeón caído: <b>{nombres}{extra}</b></div>'

    html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
*{{margin:0;box-sizing:border-box}}
html,body{{width:1000px;background:#0b1020;font:16px system-ui,'Segoe UI',Roboto,sans-serif}}
.card{{width:1000px;background:linear-gradient(170deg,#0b1020,#101a3a 60%,#0e1530);
color:#e8ecf7;padding:44px 48px 36px}}
.brand{{display:flex;align-items:center;justify-content:center;gap:15px;margin-bottom:10px}}
.brand img{{width:66px;height:66px;object-fit:contain;border-radius:12px;
box-shadow:0 4px 14px #0007;background:#0e1530;padding:3px}}
.brand .bn{{font-size:25px;font-weight:800;color:#e8ecf7;letter-spacing:.01em;line-height:1.05;text-align:left}}
.brand .bn small{{display:block;font-size:13px;font-weight:600;color:#8d97bf;letter-spacing:.02em;margin-top:3px}}
.kick{{color:#ffd24a;letter-spacing:.22em;font-size:18px;text-transform:uppercase;text-align:center}}
.h1{{font-size:46px;font-weight:800;text-align:center;margin:6px 0 2px}}
.jor{{text-align:center;color:#8d97bf;font-size:22px;margin-bottom:26px}}
.lider{{display:flex;align-items:center;gap:20px;background:linear-gradient(150deg,#2a2140,#3a2c1a);
border:1px solid #4a3a20;border-radius:20px;padding:22px 28px;margin-bottom:22px}}
.lider .fl{{width:74px;border-radius:6px;box-shadow:0 4px 14px #0009}}
.lider .lbl{{color:#ffd24a;font-size:16px;letter-spacing:.12em;text-transform:uppercase}}
.lider .who{{font-size:34px;font-weight:800;line-height:1.1}}
.lider .pts{{margin-left:auto;text-align:right}}
.lider .pts b{{font-size:44px;color:#ffd24a}}
.lider .pts span{{display:block;color:#8d97bf;font-size:15px}}
.tiles{{display:flex;gap:16px;margin-bottom:20px}}
.tile{{flex:1;background:#151c34;border:1px solid #2a3358;border-radius:16px;padding:16px 18px;text-align:center}}
.tile .t{{font-size:15px;color:#8d97bf}}
.tile .w{{font-size:25px;font-weight:800;margin:4px 0;line-height:1.1}}
.tile .x{{font-size:15px;color:#16d97b}}
.tile.dn .x{{color:#ff8aa0}}
.muertos{{text-align:center;background:#2a1620;border:1px solid #5a2030;color:#ff8aa0;
border-radius:14px;padding:12px;margin-bottom:20px;font-size:19px}}
table{{width:100%;border-collapse:collapse;font-size:21px}}
td{{padding:11px 10px;border-bottom:1px solid #222c52}}
.rk{{width:54px;text-align:center;font-size:23px}}
.nm{{font-weight:700}}
.nm .fl{{width:26px;border-radius:4px;vertical-align:-5px;margin-right:11px;box-shadow:0 1px 3px #0008}}
.tot{{text-align:right;font-weight:800;color:#ffd24a;width:90px}}
.dl{{text-align:right;width:90px;font-weight:700}}
.up{{color:#16d97b}}.dn{{color:#ff8aa0}}.eq{{color:#5a648c}}
tr.dead .nm{{opacity:.6}}
tr.tailgap td{{text-align:center;color:#3a4470;border:none;padding:2px;letter-spacing:.4em}}
tr.tail td{{background:#161d3a}}
.foot{{display:flex;align-items:center;justify-content:space-between;margin-top:26px;
padding-top:18px;border-top:1px solid #2a3358}}
.foot .cta{{font-size:22px;font-weight:700}}
.foot .url{{color:#ffd24a;font-size:20px;font-weight:800}}
.foot .date{{color:#5a648c;font-size:15px}}
</style></head><body>
<div class="card">
  {f'<div class="brand"><img src="{logo_data_uri()}" alt=""><div class="bn">Fisioterapia &amp; Futbolito FC<small>⚽ el fútbol lo ponemos nosotros, la fisioterapia la pone la edad</small></div></div>' if logo_data_uri() else ''}
  <div class="kick">Quiniela Mundial 2026</div>
  <div class="h1">📊 Cómo va la cosa</div>
  <div class="jor">{st['jornada']}</div>

  <div class="lider">
    {flag(lider['champ'], ISO, 80)}
    <div><div class="lbl">🏆 Puntero</div><div class="who">{lider['name']}</div></div>
    <div class="pts"><b>{lider['total']}</b><span>puntos</span></div>
  </div>

  <div class="tiles">
    <div class="tile"><div class="t">👑 Rey de la jornada</div><div class="w">{rey['name'].split()[0]}</div><div class="x">+{rey['round_pts']} pts</div></div>
    <div class="tile"><div class="t">📈 Trepó</div><div class="w">{subio_name}</div><div class="x">{subio_x}</div></div>
    <div class="tile dn"><div class="t">📉 Se hundió</div><div class="w">{cayo_name}</div><div class="x">{cayo_x}</div></div>
  </div>

  {muertos_html}

  <table>{trs}</table>

  <div class="foot">
    <div><div class="cta">¿Sigues vivo? 👀</div><div class="date">{fecha_label}</div></div>
    <div class="url">{SITE_URL}</div>
  </div>
</div></body></html>"""
    return html


def render_png(html, slug='tarjeta-dia'):
    os.makedirs(OUTDIR, exist_ok=True)
    htmlpath = os.path.join(OUTDIR, f'{slug}.html')
    pngpath = os.path.join(OUTDIR, f'{slug}.png')
    with open(htmlpath, 'w', encoding='utf-8') as f:
        f.write(html)
    edges = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
             r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']
    edge = next((e for e in edges if os.path.exists(e)), None)
    if not edge:
        print(f'HTML generado: {htmlpath} (Edge no encontrado — abre y exporta la imagen a mano)')
        return htmlpath
    url = 'file:///' + htmlpath.replace('\\', '/')
    subprocess.run([edge, '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--window-size=1000,1115', '--virtual-time-budget=9000',
                    f'--screenshot={pngpath}', url], check=False)
    print(f'✓ Tarjeta lista: {pngpath}\n  Mándala al grupo de WhatsApp. Lleva el link {SITE_URL}.')
    return pngpath


# ---------- modos ----------
def run_demo():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    NM = {c: eq[c]['nombre_es'] for c in eq}; ISO = {c: eq[c]['iso'] for c in eq}
    rng = random.Random(7)
    rg = {m['match_no']: (rng.randint(0, 3), rng.randint(0, 3)) for m in fixture if m['fase'] == 'grupos'}
    r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(rg, fixture), eq), fixture, terceros)
    rk_full = demo.sim_ko(r32, fixture, rng, accuracy=0.80)
    # corte actual = octavos jugados (<=96), corte previo = 16avos (<=88)
    rk_now = {mn: w for mn, w in rk_full.items() if mn <= 96}
    rk_prev = {mn: w for mn, w in rk_full.items() if mn <= 88}
    NAMES = ['Manuel Fuentes', 'Rodrigo Salazar', 'Felipe Cárdenas', 'Cristóbal Reyes', 'Matías Ibáñez',
             'Sebastián Vergara', 'Diego Fuentealba', 'Tomás Navarro', 'Ignacio Bravo', 'Vicente Cáceres']
    ACC = [None, 0.85, 0.30, 0.62, 0.50, 0.70, 0.25, 0.45, 0.40, 0.55]
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
        players.append({'slug': name.upper().replace(' ', '_'), 'name': name, 'gs': gs, 'ko': ko, 'esp': esp,
                        'champ': engine.full_bracket(gs, ko, eq, fixture, terceros)['champion']})
    t_prev, _ = score_at(players, rg, rk_prev, eq, fixture, terceros)
    r_prev = ranks_from(t_prev)
    prev_map = {s: {'total': t_prev[s], 'pos': r_prev[s]} for s in t_prev}
    st = build_state(players, rg, rk_now, prev_map, eq, fixture, terceros, NM, ISO, 'Tras los Octavos de Final')
    render_png(render(st, 'Vista de muestra'))


def load_pred(slug):
    gs, ko, esp = {}, {}, {}
    for r in csv.DictReader(open(os.path.join(PRED, f'{slug}.csv'), encoding='utf-8')):
        gs[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    for r in csv.DictReader(open(os.path.join(PRED, f'{slug}_ko.csv'), encoding='utf-8')):
        if r['ganador']:
            ko[int(r['match_no'])] = r['ganador']
    for r in csv.DictReader(open(os.path.join(PRED, f'{slug}_especiales.csv'), encoding='utf-8')):
        esp[r['clave']] = r['valor']
    return gs, ko, esp


def run_real():
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    NM = {c: eq[c]['nombre_es'] for c in eq}; ISO = {c: eq[c]['iso'] for c in eq}
    slugs = [fn[:-4] for fn in sorted(os.listdir(PRED))
             if fn.endswith('.csv') and not fn.endswith('_ko.csv') and not fn.endswith('_especiales.csv')
             and fn[:-4] not in DENY] if os.path.isdir(PRED) else []
    if not slugs:
        print('No hay predicciones de jugadores. Ingiere plantillas primero.'); return
    players = []
    for slug in slugs:
        gs, ko, esp = load_pred(slug)
        players.append({'slug': slug, 'name': esp.get('jugador') or display_name(slug),
                        'gs': gs, 'ko': ko, 'esp': esp,
                        'champ': engine.full_bracket(gs, ko, eq, fixture, terceros)['champion']})
    # resultados reales (parciales) + snapshot previo opcional (data/historico/prev.*)
    def load_res(suffix=''):
        rg, rk = {}, {}
        p = os.path.join(HERE, 'data', f'resultados{suffix}.csv')
        if os.path.exists(p):
            for r in csv.DictReader(open(p, encoding='utf-8')):
                if r.get('gl') not in (None, '') and r.get('gv') not in (None, ''):
                    rg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
        p = os.path.join(HERE, 'data', f'resultados_ko{suffix}.csv')
        if os.path.exists(p):
            for r in csv.DictReader(open(p, encoding='utf-8')):
                if r.get('ganador'):
                    rk[int(r['match_no'])] = r['ganador']
        return rg, rk
    rg_now, rk_now = load_res('')
    import snapshot
    prev_map = snapshot.read_last()          # delta vs el último cierre de jornada
    st = build_state(players, rg_now, rk_now, prev_map, eq, fixture, terceros, NM, ISO,
                     'Estado actual' if rg_now else 'El torneo aún no comienza')
    render_png(render(st, 'hoy'))


if __name__ == '__main__':
    if '--demo' in sys.argv:
        run_demo()
    else:
        run_real()
