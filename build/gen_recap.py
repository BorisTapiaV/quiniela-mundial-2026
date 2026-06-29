#!/usr/bin/env python
"""Generador de la tarjeta de recap diario (pronósticos para WhatsApp).

Uso:
    python build/gen_recap.py 2026-06-29            # tarjeta real de esa fecha
    python build/gen_recap.py 2026-07-03 --prueba   # tarjeta marcada como PRUEBA

- Grupos: muestra el marcador + ganador de cada jugador.
- KO: muestra el equipo que el cuadro de cada jugador hace avanzar más lejos en
  ese cruce (regla consistente con el puntaje por equipos-que-avanzan).
- Banderas embebidas en base64 (self-contained, sin imágenes externas → el
  screenshot nunca sale con banderas rotas).
Salida: recap/predicciones-<fecha>.html  (o ...-PRUEBA-<fecha>.html con --prueba)
"""
import sys, csv, os, datetime, struct, json, unicodedata, urllib.request, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E


def norm(s):
    """minúsculas sin acentos, para casar nombres (Mbappé == Mbappe)."""
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower().strip()
    return ' '.join(s.split())

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, 'data')
PRED = os.path.join(DATA, 'predicciones')
RECAP = os.path.join(HERE, 'recap')

PLAYERS = ['CASA', 'PAULO_SALAS', 'CARLOS_SALGADO', 'ANDRES_ACOSTA', 'JORGE_VASQUEZ']
PNAME = {'CASA': 'Boris · La Casa', 'PAULO_SALAS': 'Paulo Salas',
         'CARLOS_SALGADO': 'Carlos Salgado', 'ANDRES_ACOSTA': 'Andrés Acosta',
         'JORGE_VASQUEZ': 'Jorge Vásquez'}
DIAS = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
MESES = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
FASE_LBL = {'R32': '16avos', 'R16': 'Octavos', 'QF': 'Cuartos', 'SF': 'Semis', 'Final': 'Final'}
ROUND_DEPTH = {'R32': 1, 'R16': 2, 'QF': 3, 'SF': 4, 'Final': 5}
# etiqueta = hasta qué ronda el jugador lleva al equipo (profundidad que ALCANZA)
DEPTH_LBL = {2: 'hasta octavos', 3: 'hasta cuartos', 4: 'hasta semis', 5: 'hasta la final'}


def load_pred(slug):
    g, k = {}, {}
    with open(os.path.join(PRED, f'{slug}.csv'), encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            g[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    p = os.path.join(PRED, f'{slug}_ko.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r.get('ganador'):
                    k[int(r['match_no'])] = r['ganador'].strip().upper()
    return g, k


def load_goleador(slug):
    """Figura (goleador) elegida por el jugador, desde su _especiales.csv."""
    p = os.path.join(PRED, f'{slug}_especiales.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r['clave'] == 'goleador' and r['valor']:
                    return r['valor']
    return ''


def load_goles():
    """norm(figura) -> goles, desde data/goleadores.csv (lo refresca fetch_goleadores)."""
    d = {}
    p = os.path.join(DATA, 'goleadores.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                d[norm(r['figura'])] = int(r.get('goles') or 0)
    return d


def load_fotos():
    """norm(nombre) -> jpg base64, desde data/figuras_fotos.json."""
    p = os.path.join(DATA, 'figuras_fotos.json')
    if os.path.exists(p):
        return {norm(k): v for k, v in json.load(open(p, encoding='utf-8')).items()}
    return {}


_flags = {}
def flag(iso):
    """(b64, w, h) de la bandera w40 de flagcdn, o None."""
    if iso in _flags:
        return _flags[iso]
    try:
        data = urllib.request.urlopen(f'https://flagcdn.com/w40/{iso}.png', timeout=12).read()
        w, h = struct.unpack('>II', data[16:24])
        _flags[iso] = (base64.b64encode(data).decode(), w, h)
    except Exception as ex:
        print(f'  ⚠ bandera {iso}: {ex}')
        _flags[iso] = None
    return _flags[iso]


def flag_span(iso, disp_h):
    f = flag(iso)
    if not f:
        return ''
    _, w, h = f
    dw = round(disp_h * w / h)
    return f'<span class="flag fl-{iso}" style="width:{dw}px;height:{disp_h}px"></span>'


def load_results():
    rg, rk = {}, {}
    p = os.path.join(DATA, 'resultados.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('gl') not in (None, '') and r.get('gv') not in (None, ''):
                    rg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    p = os.path.join(DATA, 'resultados_ko.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('ganador'):
                    rk[int(r['match_no'])] = r['ganador']
    return rg, rk


def depth_of(pb, team):
    d = 0
    for rnd, lvl in ROUND_DEPTH.items():
        if team in pb['sets'][rnd]:
            d = lvl
    return d


def main():
    if len(sys.argv) < 2:
        print('uso: python build/gen_recap.py <YYYY-MM-DD> [--prueba]'); return
    fecha = sys.argv[1]
    prueba = '--prueba' in sys.argv
    y, m, d = map(int, fecha.split('-'))
    dt = datetime.date(y, m, d)

    eq = E.load_equipos(); fixture = E.load_fixture(); terceros = E.load_terceros()
    NM = {c: eq[c]['nombre_es'] for c in eq}
    ISO = {c: eq[c]['iso'] for c in eq}
    rg, rk = load_results()

    # partidos de la fecha
    dia = [mm for mm in fixture if mm['fecha'] == fecha]
    dia.sort(key=lambda mm: (mm['hora_chile'], mm['match_no']))
    if not dia:
        print(f'No hay partidos el {fecha}'); return

    groups_done = len(rg) >= 72
    real_r32 = (E.build_r32(E.compute_all_standings(E.group_results_by_group(rg, fixture), eq), fixture, terceros)
                if groups_done else {})

    # brackets de cada jugador (para picks KO)
    brackets = {}
    for slug in PLAYERS:
        pg, pk = load_pred(slug)
        brackets[slug] = (pg, pk, E.full_bracket(pg, pk, eq, fixture, terceros))

    blocks = []
    fase_set = set()
    for mm in dia:
        mn = mm['match_no']; fase = mm['fase']; fase_set.add(fase)
        if fase == 'grupos':
            a, b = mm['local'], mm['visita']
        elif mn in real_r32:
            a, b = real_r32[mn]
        else:
            a, b = None, None  # KO con equipos aún no resueltos

        # cabecera del partido
        jugado = (mn in rg) or (mn in rk)
        badge = (f'<span class="played">{FASE_LBL.get(fase, fase).upper()} · JUGADO</span>' if jugado
                 else f'<span class="venue">{FASE_LBL.get(fase, fase)} · {mm["sede"].replace("Estadio ", "")}</span>')
        if a and b:
            teams_html = (f'{flag_span(ISO[a], 18)} {NM[a]} <span class="code">{a}</span>'
                          f'<span class="vs">vs</span>'
                          f'{flag_span(ISO[b], 18)} {NM[b]} <span class="code">{b}</span>')
        else:
            teams_html = f'<b>{FASE_LBL.get(fase, fase)}</b> <span class="vs">(cruce por definir)</span>'

        # picks por jugador
        preds = []
        for slug in PLAYERS:
            pg, pk, pb = brackets[slug]
            cls = 'pred casa' if slug == 'CASA' else 'pred'
            if fase == 'grupos':
                sc = pg.get(mn)
                if sc:
                    gl, gv = sc
                    win = a if gl > gv else (b if gv > gl else None)
                    tag = (NM[win] if win else 'Empate')
                    preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                                 f'<div class="pick">{gl}-{gv}</div><div class="tag">{tag}</div></div>')
                else:
                    preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                                 f'<div class="pick none">—</div><div class="tag">sin pronóstico</div></div>')
            else:  # KO: el pick = el equipo que el jugador hace GANAR este cruce (lo lleva a la ronda siguiente)
                da = depth_of(pb, a) if a else 0
                db = depth_of(pb, b) if b else 0
                if fase == 'Final':
                    champ = pb.get('champion')
                    cands = [(champ, 6)] if champ in (a, b) else []
                else:
                    need = ROUND_DEPTH.get(fase, 1) + 1   # para ganar este cruce debe llegar a la ronda siguiente
                    cands = [(t, d) for t, d in ((a, da), (b, db)) if t and d >= need]
                if not cands:
                    # su llave no hace ganar este cruce a ninguno de los dos equipos reales.
                    # mostramos a quién tenía él en ese casillero (calza con el caso "tenía a Croacia").
                    suyo = pb['win'].get(mn)
                    tag = f'tenía a {NM[suyo]}' if (suyo and suyo not in (a, b)) else 'sin pronóstico'
                    preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                                 f'<div class="pick none">—</div><div class="tag">{tag}</div></div>')
                else:
                    pick, dep = max(cands, key=lambda x: x[1])
                    tag = 'Ganador'
                    preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                                 f'<div class="pick">{flag_span(ISO[pick], 12)}{NM[pick]}</div>'
                                 f'<div class="tag">{tag}</div></div>')

        blocks.append(f'''  <div class="match">
    <div class="mtop">
      <span class="hour">{mm['hora_chile']}</span>
      <div class="teams">{teams_html}</div>
      {badge}
    </div>
    <div class="grid">
      {''.join(preds)}
    </div>
  </div>''')

    # sección de goleadores (figura + foto + goles de cada jugador)
    goles = load_goles(); fotos = load_fotos()
    figdata = [(slug, load_goleador(slug)) for slug in PLAYERS]
    figdata = [(slug, fig, (goles.get(norm(fig), 0) if fig else None)) for slug, fig in figdata]
    max_g = max([g for _, _, g in figdata if g is not None] or [-1])
    golcards = []
    for slug, fig, g in figdata:
        cls = 'golcard casa' if slug == 'CASA' else 'golcard'
        if g is not None and g == max_g and max_g > 0:
            cls += ' lead'
        b64 = fotos.get(norm(fig)) if fig else None
        face = (f'<div class="golface" style="background-image:url(data:image/jpeg;base64,{b64})"></div>'
                if b64 else '<div class="golface noface">⚽</div>')
        goals_html = (f'<div class="golgoals">{g}<span> gol{"es" if g != 1 else ""}</span></div>'
                      if g is not None else '<div class="golgoals nogol">—</div>')
        golcards.append(f'<div class="{cls}">{face}<div class="golname">{PNAME[slug]}</div>'
                        f'<div class="golfig">{fig or "sin figura"}</div>{goals_html}</div>')
    golsec = (f'''  <div class="golsec">
    <div class="goltitle">⚽ Goleadores · la figura de cada uno <span>(goles en el torneo, en vivo)</span></div>
    <div class="golgrid">
      {''.join(golcards)}
    </div>
  </div>
''' if any(fig for _, fig, _ in figdata) else '')

    # CSS de banderas usadas
    flag_css = ''.join(f'  .fl-{iso}{{background-image:url(data:image/png;base64,{f[0]})}}\n'
                       for iso, f in _flags.items() if f)

    es_ko = fase_set and fase_set <= {'R32', 'R16', 'QF', 'SF', '3P', 'Final'}
    konote = ('''  <div class="konote">
    🏆 <b>Eliminatorias.</b> Aquí no se pide marcador: cada cuadro avanza solo según sus
    pronósticos. El pick de cada jugador es el equipo que su propia llave hace pasar en ese cruce.
  </div>
''' if es_ko else '')
    fase_lbl = (FASE_LBL.get(sorted(fase_set, key=lambda x: ROUND_DEPTH.get(x, 0))[0], 'Eliminatorias')
                + ' de final' if es_ko else 'Fase de grupos')
    prueba_banner = ('''  <div class="prueba">⚠️ TARJETA DE PRUEBA — diseño de ejemplo, no es la jornada real</div>
''' if prueba else '')

    html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{'PRUEBA · ' if prueba else ''}Predicciones · {DIAS[dt.weekday()]} {d:02d}-{m:02d}</title>
<style>
  :root{{--bg0:#0b1220;--bg1:#11192b;--card:#161f33;--card2:#1c2740;--line:#27324d;
    --txt:#eaf0ff;--mut:#8b9bc4;--accent:#22d3a6;--accent2:#3b82f6;--gold:#f5c451;--pill:#202c45}}
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Segoe UI',system-ui,-apple-system,Roboto,sans-serif;
    background:radial-gradient(1200px 600px at 50% -10%, #16223d 0%, var(--bg0) 60%);
    color:var(--txt);padding:36px 18px;display:flex;justify-content:center}}
  .sheet{{width:920px;max-width:100%}}
  .prueba{{background:#3a2410;border:1px solid var(--gold);color:var(--gold);font-weight:700;
    text-align:center;padding:9px;border-radius:10px;margin-bottom:18px;font-size:13.5px;letter-spacing:.3px}}
  .head{{display:flex;align-items:center;gap:18px;padding:6px 4px 22px;border-bottom:1px solid var(--line);margin-bottom:24px}}
  .crest{{width:64px;height:64px;border-radius:16px;flex:0 0 64px;
    background:linear-gradient(135deg,var(--accent),var(--accent2));
    display:flex;align-items:center;justify-content:center;font-size:30px;box-shadow:0 8px 24px rgba(34,211,166,.25)}}
  .head h1{{font-size:23px;letter-spacing:.2px}}
  .head .sub{{color:var(--mut);font-size:13.5px;margin-top:4px;font-weight:500}}
  .head .date{{margin-left:auto;text-align:right}}
  .date .big{{font-size:21px;font-weight:700;color:var(--gold)}}
  .date .small{{font-size:12.5px;color:var(--mut);letter-spacing:.5px;text-transform:uppercase}}
  .konote{{background:linear-gradient(180deg,#1a2238,#141c30);border:1px solid var(--line);
    border-left:3px solid var(--gold);border-radius:12px;padding:12px 16px;margin-bottom:18px;
    color:var(--mut);font-size:13px;line-height:1.5}}
  .konote b{{color:var(--txt)}}
  .match{{background:linear-gradient(180deg,var(--card),var(--bg1));border:1px solid var(--line);
    border-radius:18px;padding:18px 20px;margin-bottom:18px;box-shadow:0 6px 22px rgba(0,0,0,.28)}}
  .mtop{{display:flex;align-items:center;gap:14px;margin-bottom:16px}}
  .hour{{font-size:13px;font-weight:700;color:#06281f;background:var(--accent);padding:5px 11px;border-radius:999px;letter-spacing:.4px}}
  .teams{{display:flex;align-items:center;gap:9px;font-size:17px;font-weight:700}}
  .code{{background:var(--pill);border:1px solid var(--line);border-radius:10px;padding:5px 10px;font-size:13px;letter-spacing:1px;color:#cfe0ff}}
  .vs{{color:var(--mut);font-size:13px;font-weight:600}}
  .venue{{margin-left:auto;color:var(--mut);font-size:12.5px;white-space:nowrap}}
  .played{{margin-left:auto;color:#0b1220;background:var(--gold);font-weight:700;font-size:11.5px;padding:4px 9px;border-radius:999px;letter-spacing:.3px}}
  .flag{{display:inline-block;vertical-align:middle;border-radius:2px;background-size:cover;
    background-position:center;box-shadow:0 0 0 1px rgba(255,255,255,.18);margin-right:4px}}
{flag_css}  .grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}
  .pred{{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:11px 8px;text-align:center}}
  .pred .name{{font-size:11.5px;color:var(--mut);font-weight:600;margin-bottom:7px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .pred .pick{{font-size:15px;font-weight:800;letter-spacing:.2px}}
  .pred .tag{{font-size:10.5px;color:var(--mut);margin-top:4px;font-weight:600}}
  .pred.casa{{border-color:var(--accent);box-shadow:inset 0 0 0 1px rgba(34,211,166,.25)}}
  .pred.casa .name{{color:var(--accent)}}
  .pred .none{{color:var(--mut);font-weight:800;font-size:18px}}
  .golsec{{margin:20px 0 4px;background:linear-gradient(180deg,#141c30,#10182a);border:1px solid var(--line);border-radius:18px;padding:16px 18px;box-shadow:0 6px 22px rgba(0,0,0,.28)}}
  .goltitle{{font-size:14px;font-weight:700;color:var(--gold);margin-bottom:14px}}
  .goltitle span{{color:var(--mut);font-weight:500;font-size:11.5px}}
  .golgrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}
  .golcard{{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:12px 8px 11px;text-align:center}}
  .golcard.casa{{border-color:var(--accent)}}
  .golcard.lead{{border-color:var(--gold);box-shadow:inset 0 0 0 1px rgba(245,196,81,.3)}}
  .golface{{width:56px;height:56px;border-radius:50%;margin:0 auto 8px;background-size:cover;background-position:center top;border:2px solid var(--line)}}
  .golcard.casa .golface{{border-color:var(--accent)}}
  .golcard.lead .golface{{border-color:var(--gold)}}
  .golface.noface{{display:flex;align-items:center;justify-content:center;font-size:24px;background:var(--pill)}}
  .golname{{font-size:11px;color:var(--mut);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .golcard.casa .golname{{color:var(--accent)}}
  .golfig{{font-size:12.5px;font-weight:700;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .golgoals{{font-size:19px;font-weight:800;margin-top:6px;color:var(--accent)}}
  .golgoals span{{font-size:10px;color:var(--mut);font-weight:600}}
  .golcard.lead .golgoals{{color:var(--gold)}}
  .golgoals.nogol{{color:var(--mut)}}
  .foot{{display:flex;align-items:center;gap:10px;color:var(--mut);font-size:12px;margin-top:22px;padding-top:14px;border-top:1px solid var(--line)}}
  .foot .dot{{color:var(--accent)}}
  .foot .right{{margin-left:auto}}
</style>
</head>
<body>
<div class="sheet">
{prueba_banner}  <div class="head">
    <div class="crest">⚽</div>
    <div>
      <h1>Fisioterapia &amp; Futbolito FC</h1>
      <div class="sub">Quiniela Mundial 2026 · Pronósticos de la jornada</div>
    </div>
    <div class="date">
      <div class="big">{DIAS[dt.weekday()]} {d} · {MESES[m-1]}</div>
      <div class="small">{fase_lbl}</div>
    </div>
  </div>
{konote}{''.join(blocks)}
{golsec}  <div class="foot">
    <span class="dot">●</span> 5 jugadores · pozo $50.000 · reparto 50/30/20
    <span class="right">2026-mundial.netlify.app</span>
  </div>
</div>
</body>
</html>
'''
    out = os.path.join(RECAP, f'predicciones-{"PRUEBA-" if prueba else ""}{fecha}.html')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✓ {os.path.relpath(out, HERE)} · {len(dia)} partido(s) · banderas {sum(1 for v in _flags.values() if v)}/{len(_flags)}')


if __name__ == '__main__':
    main()
