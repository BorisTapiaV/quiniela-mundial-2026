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

# la consola de Windows es cp1252 → los prints con ✓/·/→/⚠ reventaban (UnicodeEncodeError)
# sin afectar el HTML; forzar UTF-8 en la salida para que el print final no falle.
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


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
FASE_LBL = {'R32': '16avos', 'R16': 'Octavos', 'QF': 'Cuartos', 'SF': 'Semis', '3P': '3er puesto', 'Final': 'Final'}
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


def load_campeon(slug):
    """Código de equipo del campeón elegido por el jugador, desde su _especiales.csv."""
    p = os.path.join(PRED, f'{slug}_especiales.csv')
    if os.path.exists(p):
        with open(p, encoding='utf-8-sig') as f:
            for r in csv.DictReader(f):
                if r['clave'] == 'campeon' and r['valor']:
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
    # equipos reales de TODO el cuadro KO (R32→Final), resueltos con lo disponible:
    # cada cruce muestra su selección real en cuanto entra el ganador que lo alimenta
    # (antes solo se resolvían los 16avos → octavos+ salían "cruce por definir").
    real_teams, _rw = E.bracket_partial(rg, rk, eq, fixture, terceros)

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
        else:
            a, b = real_teams.get(mn, (None, None))  # KO: equipos reales (None si el feeder aún no está definido)

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
            elif fase == '3P':
                # el 3er puesto no otorga avance (no se puntúa) → sin pick
                preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                             f'<div class="pick none">—</div><div class="tag">sin avance</div></div>')
            else:  # KO: estado POR EQUIPO (avanza ↑ / cae ✗ / ausente), consistente con el puntaje por conjunto.
                # El juego no es "en qué casillero cae" sino "clasifica o no, y en este cruce pasa o no".
                # Por cada selección real del cruce: la lleva más lejos que esta ronda (avanza), la tiene
                # clasificada pero no la pasa (cae), o no la clasificó (se omite).
                need = 99 if fase == 'Final' else ROUND_DEPTH.get(fase, 1) + 1
                chips = []
                for t in (a, b):
                    if not t:
                        continue
                    dp = depth_of(pb, t)
                    if dp == 0:
                        continue  # el jugador no clasificó a este equipo → no aparece
                    adv = (pb.get('champion') == t) if fase == 'Final' else (dp >= need)
                    chips.append((t, adv))
                if not chips:
                    # no tiene a ninguno de los dos que juegan este cruce → "—"
                    preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                                 f'<div class="pick none">—</div><div class="tag"></div></div>')
                else:
                    wins = [t for t, adv in chips if adv]
                    loses = [t for t, adv in chips if not adv]
                    if len(wins) == 2:    tag = 'Asegurado'   # tiene a los dos → suma gane quien gane
                    elif len(wins) == 1:  tag = 'Avanza'
                    elif len(loses) == 2: tag = 'Doble fallo'  # tenía a los dos fuera → no suma
                    else:                 tag = 'Cae'
                    picks_html = ' '.join(
                        f'<span class="tm {"win" if adv else "lose"}">{flag_span(ISO[t], 12)}{NM[t]}</span>'
                        for t, adv in chips)
                    preds.append(f'<div class="{cls}"><div class="name">{PNAME[slug]}</div>'
                                 f'<div class="pick multi">{picks_html}</div><div class="tag">{tag}</div></div>')

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
    # picks muertos (💀): goleador cuya selección quedó eliminada y ya es inalcanzable (desde 1-jul)
    muertos_on = dt >= E.PICKS_MUERTOS_DESDE
    _elim = set(eq) - E.teams_alive(rg, rk, eq, fixture, terceros)
    _scorers = E.load_scorers()
    golcards = []
    for slug, fig, g in figdata:
        cls = 'golcard casa' if slug == 'CASA' else 'golcard'
        if g is not None and g == max_g and max_g > 0:
            cls += ' lead'
        dead = muertos_on and E.goleador_dead(fig, _scorers, _elim, eq)
        if dead:
            cls += ' dead'
        b64 = fotos.get(norm(fig)) if fig else None
        face = (f'<div class="golface" style="background-image:url(data:image/jpeg;base64,{b64})"></div>'
                if b64 else '<div class="golface noface">⚽</div>')
        goals_html = (f'<div class="golgoals">{g}<span> gol{"es" if g != 1 else ""}</span></div>'
                      if g is not None else '<div class="golgoals nogol">—</div>')
        extra = '<span class="skull">💀</span><span class="exwm">✗</span>' if dead else ''
        golcards.append(f'<div class="{cls}">{extra}{face}<div class="golname">{PNAME[slug]}</div>'
                        f'<div class="golfig">{fig or "sin figura"}</div>{goals_html}</div>')
    golsec = (f'''  <div class="golsec">
    <div class="goltitle">⚽ Goleadores · la figura de cada uno <span>(goles en el torneo, en vivo)</span></div>
    <div class="golgrid">
      {''.join(golcards)}
    </div>
  </div>
''' if any(fig for _, fig, _ in figdata) else '')

    # sección de campeones (bandera + país de cada uno; el eliminado sale muerto 💀)
    champcards = []
    for slug in PLAYERS:
        camp = load_campeon(slug)
        cls = 'golcard casa' if slug == 'CASA' else 'golcard'
        dead = muertos_on and camp and camp in _elim
        if dead:
            cls += ' dead'
        pais = NM.get(camp, camp or 'sin campeón')
        fl = flag_span(ISO[camp], 46) if camp in ISO else ''
        flag_html = f'<div class="champflag">{fl}</div>' if fl else '<div class="golface noface">🏆</div>'
        estado = ('<div class="golgoals st nogol">eliminado</div>' if dead
                  else '<div class="golgoals st">en carrera</div>' if camp
                  else '<div class="golgoals st nogol">—</div>')
        extra = '<span class="skull">💀</span><span class="exwm">✗</span>' if dead else ''
        champcards.append(f'<div class="{cls}">{extra}{flag_html}<div class="golname">{PNAME[slug]}</div>'
                          f'<div class="golfig">{pais}</div>{estado}</div>')
    champsec = (f'''  <div class="golsec">
    <div class="goltitle">🏆 Campeones · el campeón de cada uno <span>(cae 💀 cuando su selección queda eliminada)</span></div>
    <div class="golgrid">
      {''.join(champcards)}
    </div>
  </div>
''' if any(load_campeon(s) for s in PLAYERS) else '')

    # CSS de banderas usadas
    flag_css = ''.join(f'  .fl-{iso}{{background-image:url(data:image/png;base64,{f[0]})}}\n'
                       for iso, f in _flags.items() if f)

    es_ko = fase_set and fase_set <= {'R32', 'R16', 'QF', 'SF', '3P', 'Final'}
    konote = ('''  <div class="konote">
    🏆 <b>Eliminatorias.</b> Aquí no se pide marcador: lo que puntúa es <b>qué equipos avanzan</b>.
    De las dos selecciones que juegan cada cruce, se marca cuáles tiene cada jugador en su cuadro
    y si las hace pasar (avanza ↑) o no (cae ✗).
  </div>
''' if es_ko else '')
    leyenda = ('''  <div class="leyenda">
    <div class="legtitle">Cómo leer cada predicción</div>
    <div class="legrow"><span class="lgs win">Equipo</span><span class="legtag">Avanza</span><span class="legdesc">lo tiene clasificado y lo hace pasar este cruce</span></div>
    <div class="legrow"><span class="lgs lose">Equipo</span><span class="legtag">Cae</span><span class="legdesc">lo tiene, pero no lo hace pasar</span></div>
    <div class="legrow"><span class="lgs win">A</span><span class="lgs win">B</span><span class="legtag">Asegurado</span><span class="legdesc">tiene a los dos del cruce → suma gane quien gane</span></div>
    <div class="legrow"><span class="lgs lose">A</span><span class="lgs lose">B</span><span class="legtag">Doble fallo</span><span class="legdesc">tenía a los dos fuera → no suma en este cruce</span></div>
    <div class="legrow"><span class="lgs none">—</span><span class="legtag"></span><span class="legdesc">no clasificó a ninguno de los dos</span></div>
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
  .pred .pick.lose{{font-size:13.5px;color:#c98b86;text-decoration:line-through;text-decoration-color:#ff7b72;text-decoration-thickness:2px}}
  .pred .pick.lose .flag{{opacity:.6}}
  .pred .pick.win{{color:var(--accent)}}
  .pred .pick.multi{{display:flex;flex-direction:column;gap:4px;align-items:center;font-size:13px;font-weight:800}}
  .pred .pick.multi .tm{{display:inline-flex;align-items:center;gap:3px}}
  .pred .pick.multi .tm.win{{color:var(--accent)}}
  .pred .pick.multi .tm.win:before{{content:"\\2191 ";font-size:11px}}
  .pred .pick.multi .tm.lose{{color:#c98b86;text-decoration:line-through;text-decoration-color:#ff7b72;text-decoration-thickness:2px}}
  .pred .pick.multi .tm.lose .flag{{opacity:.6}}
  .leyenda{{background:linear-gradient(180deg,#1a2238,#141c30);border:1px solid var(--line);border-radius:14px;padding:12px 16px;margin:0 0 14px}}
  .leyenda .legtitle{{font-size:11.5px;font-weight:700;color:var(--mut);margin-bottom:9px;text-transform:uppercase;letter-spacing:.5px}}
  .leyenda .legrow{{display:flex;align-items:center;gap:11px;margin:6px 0}}
  .leyenda .lgs{{min-width:92px;font-size:14px;font-weight:800;text-align:center}}
  .leyenda .lgs.win{{color:var(--accent)}}
  .leyenda .lgs.lose{{color:#c98b86;text-decoration:line-through;text-decoration-color:#ff7b72;text-decoration-thickness:2px}}
  .leyenda .lgs.none{{color:var(--mut);font-size:18px}}
  .leyenda .legtag{{min-width:56px;font-size:11px;font-weight:800;color:var(--mut);text-transform:uppercase;letter-spacing:.4px}}
  .leyenda .legdesc{{font-size:12.5px;color:var(--txt)}}
  .leyenda .legdesc:before{{content:"→ ";color:var(--mut)}}
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
  .champflag{{height:46px;margin:0 auto 8px;display:flex;align-items:center;justify-content:center}}
  .champflag .flag{{border:1px solid var(--line);border-radius:3px}}
  .golcard.dead .champflag{{filter:grayscale(1)}}
  .golgoals.st{{font-size:13px;font-weight:700;letter-spacing:.3px;margin-top:8px}}
  .golname{{font-size:11px;color:var(--mut);font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .golcard.casa .golname{{color:var(--accent)}}
  .golfig{{font-size:12.5px;font-weight:700;margin-top:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .golgoals{{font-size:19px;font-weight:800;margin-top:6px;color:var(--accent)}}
  .golgoals span{{font-size:10px;color:var(--mut);font-weight:600}}
  .golcard.lead .golgoals{{color:var(--gold)}}
  .golgoals.nogol{{color:var(--mut)}}
  .golcard.dead{{position:relative;overflow:hidden;filter:grayscale(.85);opacity:.6;border-color:#5c2626}}
  .golcard.dead .golface{{filter:grayscale(1)}}
  .golcard.dead .golfig{{text-decoration:line-through;text-decoration-color:#ff7b72;text-decoration-thickness:2px}}
  .golcard.dead .golgoals{{color:#7d7d7d}}
  .golcard .skull{{position:absolute;top:7px;right:8px;font-size:17px;z-index:2}}
  .golcard .exwm{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:110px;font-weight:900;color:#ff444414;pointer-events:none}}
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
{konote}{leyenda}{''.join(blocks)}
{golsec}{champsec}  <div class="foot">
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
