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
SITE_URL = 'https://2026-mundial.netlify.app'
DENY = set()                          # La Casa (Boris Tapia V) pública. {'CASA'} para volver a ocultarla.
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


KO_SCORE = {}   # match_no -> {g_gan, g_per, dur, pen_gan, pen_per} (poblado por load_results, usado por el bracket)


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
    KO_SCORE.clear()
    if os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            for r in csv.DictReader(f):
                if r.get('ganador'):
                    mn = int(r['match_no'])
                    rk[mn] = r['ganador']
                    if r.get('g_gan') not in (None, ''):
                        KO_SCORE[mn] = {'g_gan': r['g_gan'], 'g_per': r['g_per'],
                                        'dur': r.get('duracion', 'REGULAR'),
                                        'pen_gan': r.get('pen_gan', ''), 'pen_per': r.get('pen_per', '')}
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
    # ganadores reales de las llaves KO ya jugadas (73-104) → precisión de eliminatorias
    real_ko_win = {mn: real_view['win'][mn] for mn in range(73, 105) if real_view['win'].get(mn)}
    nko = len(real_ko_win)
    # Bota de Oro: goles en vivo por figura + quién está eliminado, para el estado del pick de cada jugador
    scorers = engine.load_scorers()
    eliminated = set(eq) - set(survivors)
    en2code = {eq[c]['nombre_en']: c for c in eq}
    max_g = max((g for g, _ in scorers.values()), default=0)
    players = []
    for slug in slugs:
        gs, ko, esp = load_pred(slug)
        sc = engine.score_player(gs, ko, real_view, real_group, esp, real_esp, eq, fixture, terceros)
        champ = sc['bracket']['champion']
        h1x2 = sum(1 for mn, (rl, rv) in real_group.items()
                   if mn in gs and engine._outcome(*gs[mn]) == engine._outcome(rl, rv))
        hx = sum(1 for mn, (rl, rv) in real_group.items() if gs.get(mn) == (rl, rv))
        # acertó ganador de KO: su bracket hace ganar la llave al equipo que realmente ganó
        hko = sum(1 for mn, w in real_ko_win.items() if sc['bracket']['win'].get(mn) == w)
        # goleador elegido: goles actuales, bandera del equipo y estado (💀 sin chance / 👑 líder / 🟢 en carrera)
        gpick = (esp.get('goleador') or '').strip()
        ginfo = scorers.get(engine._norm(gpick)) if gpick else None
        ggoals = ginfo[0] if ginfo else 0
        gcode = en2code.get(ginfo[1]) if ginfo else None
        if engine.goleador_dead(gpick, scorers, eliminated, eq):
            gstate = 'dead'
        elif ggoals and ggoals == max_g:
            gstate = 'lead'
        else:
            gstate = 'run'
        players.append({'slug': slug, 'name': esp.get('jugador') or display_name(slug), 'url': f'p/{slug_url(slug)}.html',
                        'apodo': apodos.get(slug, ''),
                        'sc': sc, 'champ': champ, 'h1x2': h1x2, 'hx': hx, 'hko': hko, 'nko': nko,
                        'gs': gs, 'ko': ko, 'esp': esp,
                        'gol_pick': gpick, 'gol_goals': ggoals, 'gol_code': gcode, 'gol_state': gstate,
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


MESES = ['', 'ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


def fmt_fecha(s):
    try:
        y, m, d = s.split('-'); return f'{int(d)} {MESES[int(m)]}'
    except Exception:
        return s


def build_groups_archive(rg, eq, fixture, NM, ISO):
    """Cuando los 72 de grupo están cerrados: bloque PLEGABLE con las 12 tablas
    finales (1º/2º avanzan, 3º al ranking de mejores terceros). Mientras la fase
    siga en curso devuelve '' (la cronología vive en 'Resultados por día')."""
    group_mns = {m['match_no'] for m in fixture if m['fase'] == 'grupos'}
    if not group_mns.issubset(set(rg)):
        return ''
    allst = engine.compute_all_standings(engine.group_results_by_group(rg, fixture), eq)

    def flag(c, w=20):
        return f'<img src="https://flagcdn.com/w{w}/{ISO[c]}.png" alt="">' if c in ISO else ''

    cards = ''
    for g in 'ABCDEFGHIJKL':
        rows = ''
        for t in allst[g]:
            mark = 'gq1' if t['pos'] <= 2 else ('gq3' if t['pos'] == 3 else '')
            rows += (f'<tr class="{mark}"><td class="gp">{t["pos"]}</td>'
                     f'<td class="gt">{flag(t["code"])}<span>{NM.get(t["code"], t["code"])}</span></td>'
                     f'<td>{t["pts"]}</td><td>{t["gd"]:+d}</td></tr>')
        cards += (f'<div class="garch"><h4>Grupo {g}</h4><table>'
                  f'<tr class="gh"><th></th><th></th><th>Pts</th><th>DG</th></tr>{rows}</table></div>')
    return ('<details class="grpdet"><summary>✅ Fase de grupos — cerrada '
            '<span class="note">(12 tablas finales · 🟢 1º-2º avanzan · 🟡 los 8 mejores 3º también)</span></summary>'
            f'<div class="garchgrid">{cards}</div></details>')


def build_real_bracket(rg, rk, eq, fixture, terceros, NM, ISO):
    """Sección 'Cuadro del torneo' — el bracket KO real, que se llena solo a medida
    que cierran los grupos (16avos) y avanzan las llaves (resultados_ko.csv)."""
    teams, win = engine.bracket_partial(rg, rk, eq, fixture, terceros)
    fxno = {m['match_no']: m for m in fixture}
    eliminated = set()
    for mn, (a, b) in teams.items():
        w = win.get(mn)
        if w and a and b:
            eliminated.add(b if w == a else a)

    def flag(c, w=40):   # w30 NO existe en flagcdn (404) → usar w40, válido
        return f'<img src="https://flagcdn.com/w{w}/{ISO[c]}.png" alt="">' if c in ISO else ''

    def slot_lbl(s):
        if not s: return '—'
        if s.startswith('3-'): return '3º'
        if s[0] in '12': return f'{s[0]}º{s[1]}'
        return '—'

    champion = win.get(104)

    def chip(code, raw_slot, is_win):
        if not code:
            return f'<div class="bteam tbd">{slot_lbl(raw_slot)}</div>'
        if code == champion:
            cls = 'bteam champ'
        elif is_win:
            cls = 'bteam win'
        elif code in eliminated:
            cls = 'bteam out'
        else:
            cls = 'bteam'
        return f'<div class="{cls}">{flag(code)}<span>{NM.get(code, code)}</span></div>'

    def score_line(mn, a, b, w):
        d = KO_SCORE.get(mn)
        if not d or not w or not (a and b):
            return ''
        try:
            gg, gp = int(d['g_gan']), int(d['g_per'])
        except (ValueError, TypeError, KeyError):
            return ''
        ga, gb = (gg, gp) if w == a else (gp, gg)            # orientar al chip de arriba/abajo
        extra, dur = '', d.get('dur', 'REGULAR')
        if dur == 'PENALTY_SHOOTOUT' and str(d.get('pen_gan', '')) != '':
            pg, pp = d['pen_gan'], d['pen_per']
            pa, pb = (pg, pp) if w == a else (pp, pg)
            extra = f'<span class="bpen">pen {pa}-{pb}</span>'
        elif dur == 'EXTRA_TIME':
            extra = '<span class="bpen">prórroga</span>'
        return f'<div class="bscore">{ga}<i>-</i>{gb}{extra}</div>'

    ROUNDS = [('16avos', range(73, 89)), ('Octavos', range(89, 97)),
              ('Cuartos', range(97, 101)), ('Semis', (101, 102)), ('Final', (104,))]
    cols = ''
    for title, rng in ROUNDS:
        cards = ''
        for mn in rng:
            m = fxno[mn]; a, b = teams.get(mn, (None, None)); w = win.get(mn)
            cards += (f'<div class="bmatch">{chip(a, m["local"], w == a and a is not None)}'
                      f'{chip(b, m["visita"], w == b and b is not None)}{score_line(mn, a, b, w)}</div>')
        cols += f'<div class="bround"><h4>{title}</h4>{cards}</div>'
    champ_html = (f'<div class="bchamp">🏆 Campeón: {flag(champion, 40)}<b>{NM.get(champion, champion)}</b></div>'
                  if champion else '')
    return (f'<h2 class="sec">🏆 Cuadro del torneo '
            f'<span class="note">(se llena solo a medida que avanzan las llaves · eliminados en gris)</span></h2>'
            f'{champ_html}<div class="bracket-live">{cols}</div>')


def build_matches_json(NM, ISO):
    """Datos de los 104 partidos (kickoff en UTC) para el indicador 'en juego' client-side.

    Los cruces del R32 se resuelven con la info disponible (1X/2X de grupos ya
    cerrados; el bracket se completa solo cuando entran los 72 de grupo)."""
    import json as _json
    from datetime import datetime as _dt, timedelta as _td
    rounds = {**{n: '16avos' for n in range(73, 89)}, **{n: 'Octavos' for n in range(89, 97)},
              **{n: 'Cuartos' for n in range(97, 101)}, 101: 'Semifinal', 102: 'Semifinal', 103: '3er puesto', 104: 'Final'}
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    rg = {}
    rp = os.path.join(HERE, 'data', 'resultados.csv')
    if os.path.exists(rp):
        for r in csv.DictReader(open(rp, encoding='utf-8')):
            if r.get('gl') not in (None, '') and r.get('gv') not in (None, ''):
                rg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    r32 = engine.r32_partial(rg, eq, fixture, terceros)
    out = []
    with open(os.path.join(HERE, 'data', 'fixture.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            mn = int(r['match_no']); fecha = r['fecha']; hora = (r.get('hora_chile') or r.get('hora') or '00:00').strip()
            try:
                ko = (_dt.strptime(f'{fecha} {hora}', '%Y-%m-%d %H:%M') + _td(hours=4)).strftime('%Y-%m-%dT%H:%M:00Z')
            except Exception:
                continue
            la, vi = r['local'], r['visita']
            if la in ISO and vi in ISO:
                out.append({'n': mn, 'ko': ko, 'h': NM.get(la, la), 'a': NM.get(vi, vi), 'hi': ISO[la], 'ai': ISO[vi], 'hc': hora})
            elif mn in r32 and r32[mn][0] and r32[mn][1]:
                a, b = r32[mn]
                out.append({'n': mn, 'ko': ko, 'h': NM.get(a, a), 'a': NM.get(b, b), 'hi': ISO[a], 'ai': ISO[b], 'hc': hora})
            else:
                out.append({'n': mn, 'ko': ko, 'h': rounds.get(mn, 'Eliminatorias'), 'a': '', 'hi': '', 'ai': '', 'hc': hora})
    return _json.dumps(out, ensure_ascii=False)


# JS client-side del indicador "en juego" / "próximo partido" (sin API: usa el horario + reloj del navegador)
LIVE_JS = """
function _fl(i){return i?('<img src="https://flagcdn.com/w20/'+i+'.png" class="lf" alt="">'):'';}
function _left(ms){var s=Math.floor(ms/1000),h=Math.floor(s/3600),m=Math.floor(s%3600/60);return h>0?(h+'h '+m+'m'):(m+'m');}
function _band(){
  var now=Date.now(), DUR=135*60*1000, el=document.getElementById('liveband');
  if(!el)return;
  var live=M.filter(function(x){var k=Date.parse(x.ko);return k<=now&&now<k+DUR;});
  if(live.length){
    el.innerHTML=live.map(function(x){return '<span class="lvdot"></span> EN JUEGO: '+_fl(x.hi)+' <b>'+x.h+'</b>'+(x.a?(' vs <b>'+x.a+'</b> '+_fl(x.ai)):'');}).join(' &nbsp;·&nbsp; ')+' <span class="lvsub">— los puntos entran cuando termina el partido</span>';
    el.className='liveband live'; el.hidden=false;
    var st=document.querySelector('.state');
    if(st && /no comienza/.test(st.textContent)){st.innerHTML='⚽ <b>¡El Mundial está en marcha!</b> Pronósticos sellados — la tabla se mueve cuando termina cada partido.';}
    return;
  }
  var up=M.filter(function(x){return Date.parse(x.ko)>now;}).sort(function(a,b){return Date.parse(a.ko)-Date.parse(b.ko);})[0];
  if(up){
    el.innerHTML='⏳ Próximo: '+_fl(up.hi)+' <b>'+up.h+'</b>'+(up.a?(' vs <b>'+up.a+'</b> '+_fl(up.ai)):'')+' <span class="lvsub">— empieza en '+_left(Date.parse(up.ko)-now)+' ('+up.hc+' hora Chile)</span>';
    el.className='liveband next'; el.hidden=false; return;
  }
  el.hidden=true;
}
_band(); setInterval(_band,30000);
"""


def render(players, has_results, state, real_view, fxno, NM, ISO, ranks, miles, is_demo, n_played=0, real_group=None, bracket_html='', groups_archive=''):
    def flag(c, w=40):
        return f'<img class="flag" src="https://flagcdn.com/w{w}/{ISO[c]}.png" alt="">' if c in ISO else ''

    def apo(p):
        return f'<span class="apo">«{p["apodo"]}»</span>' if p.get('apodo') else ''

    # ---- galería (siempre) ----
    gallery = ''
    for p in sorted(players, key=lambda p: p['name']):
        ch = f'{flag(p["champ"], 80)}<div class="ggc">🏆 {NM.get(p["champ"], p["champ"])}</div>' if p['champ'] else '<div class="ggc">—</div>'
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
            if not p['champ']:
                badge = '<span class="b seal">— sin campeón</span>'
            elif not p['alive']:
                badge = '<span class="b dead">💀 su campeón cayó</span>'
            else:
                badge = '<span class="b alive">🟢 vivo</span>'
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
        rey_ko = max(players, key=lambda p: p['hko'])
        nko_subs = players[0]['nko'] if players else 0
        # supervivencia
        cg = ''
        for p in sorted(players, key=lambda p: p['name']):
            st = 'dead' if not p['alive'] else 'alive'
            cg += (f'<div class="cg {st}">{flag(p["champ"], 80)}<div class="cgn">{p["name"]}</div>'
                   f'<div class="cgc">{"💀 eliminado" if not p["alive"] else "🟢 en carrera"} · {NM.get(p["champ"], p["champ"])}</div></div>')
        # Bota de Oro: espejo de la de campeones — pick de goleador de cada jugador + goles + estado
        GST = {'lead': '👑 líder', 'run': '🟢 en carrera', 'dead': '💀 sin chance'}
        bg = ''
        for p in sorted(players, key=lambda p: (-p.get('gol_goals', 0), p['name'])):
            gst = p.get('gol_state', 'run')
            stc = 'dead' if gst == 'dead' else 'alive'
            gc = p.get('gol_code')
            fl = flag(gc, 80) if gc else '<div class="cgnofl">⚽</div>'
            pick = p.get('gol_pick') or '—'
            goals = p.get('gol_goals', 0)
            bg += (f'<div class="cg {stc}">{fl}<div class="cgn">{p["name"]}</div>'
                   f'<div class="cgc">{GST[gst]} · {pick} · {goals} gol{"" if goals == 1 else "es"}</div></div>')
        # Liga de Consolación (ESPN ladder): los de fuera del podio compiten aparte
        cons_html = ''
        if len(players) > 3:
            crows = ''
            for j, p in enumerate(players[3:], 1):
                med = '🏅' if j == 1 else str(j + 3)
                deadc = '' if p['alive'] else 'dead'
                crows += (f'<tr class="{deadc}"><td class="rk">{med}</td>'
                          f'<td class="nm">{flag(p["champ"], 20)}<span>{p["name"]}</span>{apo(p)}</td>'
                          f'<td class="tot">{p["sc"]["total"]}</td></tr>')
            cons_html = (
                '<h2 class="sec">🪜 Liga de Consolación '
                '<span class="note">(el campeonato de los que hoy están fuera del podio — aquí hasta el último pelea su propia corona)</span></h2>'
                f'<table class="lead cons"><tr><th>#</th><th>Jugador</th><th>Total</th></tr>{crows}</table>')
        evo = demo.evolution_svg(ranks, miles, [p['name'] for p in players]) if ranks else ''
        evo_sec = f'<h2 class="sec">📈 Evolución del ranking</h2><div class="evo">{evo}</div>' if evo else ''
        # Precisión por jugador: grupos (1X2 + exactos) y eliminatorias (acertó ganador de la llave), acumulado sobre lo jugado
        nko = players[0]['nko'] if players else 0
        prec_rows = ''
        for p in sorted(players, key=lambda q: (-q['h1x2'], -q['hx'], q['name'])):
            ko_cells = (f'<td>{nko}</td><td class="tot">{p["hko"]}</td>') if nko else '<td class="note" colspan="2">aún no</td>'
            prec_rows += (f'<tr><td class="nm">{p["name"]}{apo(p)}</td><td>{n_played}</td>'
                          f'<td class="tot">{p["h1x2"]}</td><td>{p["hx"]}</td>{ko_cells}</tr>')
        nota_elim = f' · eliminatorias sobre {nko} llave(s)' if nko else ''
        prec_html = (f'<h2 class="sec">🎯 Precisión <span class="note">(grupos sobre {n_played} partido(s){nota_elim})</span></h2>'
                     f'<table class="lead prec"><tr><th>Jugador</th><th title="grupos jugados">Jug.</th><th>Ganador</th><th>🎯 Exactos</th>'
                     f'<th title="eliminatorias jugadas">⚔️ Jug.</th><th>Ganador</th></tr>{prec_rows}</table>')
        rich = f"""
<h2 class="sec">📊 La carrera <span class="note">(verde = grupos · dorado = eliminatorias)</span></h2>
<div class="race">{race}</div>
{prec_html}
{evo_sec}
<h2 class="sec">🏅 Sub-campeonatos</h2>
<div class="subs">
<div class="subc"><div class="t">👑 Rey de la fase de grupos</div><div class="w">{rg_['name']}</div><div class="x">{rg_['sc']['grupo']} pts</div></div>
<div class="subc"><div class="t">🔮 El Profeta (bracket)</div><div class="w">{pf['name']}</div><div class="x">{pf['sc']['avance']} pts de avance</div></div>
<div class="subc"><div class="t">🎯 Rey del 1X2</div><div class="w">{r1['name']}</div><div class="x">{r1['h1x2']} resultados</div></div>
<div class="subc"><div class="t">🎯 Rey del marcador exacto</div><div class="w">{rx['name']}</div><div class="x">{rx['hx']} clavados</div></div>
<div class="subc"><div class="t">⚔️ Rey de las eliminatorias</div><div class="w">{rey_ko['name'] if nko_subs else '—'}</div><div class="x">{f"{rey_ko['hko']} de {nko_subs} llaves" if nko_subs else 'aún no arrancan'}</div></div>
</div>
{bracket_html}
<h2 class="sec">💀 Supervivencia de campeones</h2>
<div class="cgrid">{cg}</div>
<h2 class="sec">🥇 Bota de Oro <span class="note">(el goleador que eligió cada jugador · 👑 = puntero)</span></h2>
<div class="cgrid">{bg}</div>
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

    # ---- Resultados por día (A): marcador + quién acertó, lo más reciente arriba ----
    results_html = ''
    if real_group:
        byday = {}
        for mn, (gl, gv) in real_group.items():
            m = fxno.get(mn)
            if not m or m.get('fase') != 'grupos':
                continue
            byday.setdefault(m['fecha'], []).append((mn, gl, gv, m))
        daysec = ''
        for fecha in sorted(byday, reverse=True):
            rows = ''
            for mn, gl, gv, m in sorted(byday[fecha], key=lambda t: -t[0]):
                la, vi = m['local'], m['visita']
                clav = [pp['name'] for pp in players if pp['gs'].get(mn) == (gl, gv)]
                gana = [pp['name'] for pp in players if pp['gs'].get(mn) and pp['gs'].get(mn) != (gl, gv)
                        and engine._outcome(*pp['gs'][mn]) == engine._outcome(gl, gv)]
                who = ''
                if clav:
                    who += f'<div class="rwho hit">🎯 clavaron: {", ".join(clav)}</div>'
                if gana:
                    who += f'<div class="rwho gan">✓ ganador: {", ".join(gana)}</div>'
                if not clav and not gana:
                    who = '<div class="rwho none">nadie acertó</div>'
                rows += (f'<div class="rmatch"><div class="rsc">{flag(la, 40)}<span class="rt">{NM.get(la, la)}</span>'
                         f'<span class="rscore">{gl}<i>-</i>{gv}</span><span class="rt">{NM.get(vi, vi)}</span>{flag(vi, 40)}</div>{who}</div>')
            daysec += f'<div class="rday"><div class="rdate">{fmt_fecha(fecha)}</div>{rows}</div>'
        if daysec:
            results_html = (f'<details class="grpdet resdet"><summary>📋 Resultados por día '
                            f'<span class="note">(toca para abrir · lo más reciente arriba)</span></summary>'
                            f'<div class="resbody">{daysec}</div></details>')

    head = demo.HEAD.replace('{TITLE}', 'Pronósticos y tabla').replace('</head>', og + '</head>')
    html = head + EXTRA_CSS + f"""
<header><img class="brand-logo" src="fisio-fc.png" alt="Fisioterapia & Futbolito FC">
<div class="kick">Copa Mundial FIFA 2026 · Canadá · México · EE.UU.</div>
<h1>Quiniela 2026</h1>
<div class="sponsor">⚽ El fútbol lo ponemos nosotros, la fisioterapia la pone la edad
<span class="sponsor-sub">patrocinado por el kinesiólogo de confianza y el ibuprofeno 600 💊🧊</span></div>
<nav><a class="on" href="index.html">Posiciones</a><a href="calendario.html">Calendario</a></nav>
<a class="share" href="{share_href}" target="_blank" rel="noopener">📲 Compartir al grupo</a>
{demobanner}</header>

<div class="state">{state}</div>
<div id="liveband" class="liveband" hidden></div>

<h2 class="sec">🏁 Tabla de posiciones</h2>
{lead_note}
<table class="lead"><tr><th>#</th><th>Jugador</th><th>Su campeón</th><th>Grupos</th><th>KO</th><th>Total</th>{'<th title="cambio desde la jornada anterior">±</th>' if show_delta else ''}<th>Estado</th></tr>{lb}</table>

{groups_archive}
{results_html}

{premios}

<h2 class="sec">🖼️ Galería de pronósticos <span class="note">(click en un jugador para ver su cuadro completo)</span></h2>
<div class="ggrid">{gallery}</div>
{rich}
<footer>Banderas: flagcdn.com (dominio público) · gen_galeria.py{' · datos de muestra' if is_demo else ''}</footer>
</div></body></html>"""

    html = html.replace('</body></html>',
                        '<script>\nvar M=' + build_matches_json(NM, ISO) + ';' + LIVE_JS + '</script>\n</body></html>')

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
/* ---- Cuadro del torneo (KO real, se llena solo) ---- */
.bracket-live{display:flex;gap:12px;overflow-x:auto;padding-bottom:10px;-webkit-overflow-scrolling:touch}
.bround{min-width:152px;flex:1 0 auto}
.bround h4{font-size:10px;text-transform:uppercase;letter-spacing:.12em;color:var(--mut);margin:0 0 8px;text-align:center;font-weight:700}
.bmatch{background:#0e1738;border:1px solid var(--line);border-radius:7px;margin-bottom:8px;overflow:hidden}
.bteam{display:flex;align-items:center;gap:6px;padding:5px 8px;font-size:12px;border-bottom:1px solid rgba(255,255,255,.05);white-space:nowrap}
.bteam:last-child{border-bottom:none}
.bteam img{width:18px;border-radius:2px;flex:0 0 auto}
.bteam span{overflow:hidden;text-overflow:ellipsis}
.bteam.win{background:linear-gradient(90deg,rgba(28,125,78,.5),transparent);font-weight:700}
.bteam.champ{background:linear-gradient(90deg,rgba(255,180,60,.32),transparent);color:#ffe7ad;font-weight:700}
.bteam.out{opacity:.42;text-decoration:line-through}
.bscore{text-align:center;font-size:11px;font-weight:700;color:var(--gold);padding:3px 6px;background:rgba(0,0,0,.22);letter-spacing:.5px}
.bscore i{color:var(--mut);font-style:normal;margin:0 1px}
.bpen{display:inline-block;margin-left:6px;font-size:9.5px;font-weight:600;color:var(--mut);letter-spacing:.3px}
.bteam.tbd{color:var(--mut);font-style:italic;justify-content:center;font-size:11px}
.bchamp{text-align:center;font-size:15px;margin:4px 0 14px;color:#ffe7ad}
.bchamp img{width:30px;border-radius:3px;vertical-align:-7px;margin:0 4px}
/* ---- Archivo plegable: fase de grupos cerrada ---- */
.grpdet{margin:14px auto;max-width:920px;background:rgba(255,255,255,.025);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.grpdet summary{cursor:pointer;padding:12px 16px;font-weight:700;font-size:15px;list-style:none}
.grpdet summary::-webkit-details-marker{display:none}
.grpdet summary::before{content:"▸ ";color:var(--mut)}
.grpdet[open] summary::before{content:"▾ "}
.resdet{max-width:980px}
.resbody{padding:4px 14px 14px}
.garchgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;padding:4px 16px 16px}
.garch{background:#0e1738;border:1px solid var(--line);border-radius:8px;padding:8px 10px}
.garch h4{margin:0 0 6px;font-size:12px;color:var(--gold);letter-spacing:.05em}
.garch table{width:100%;border-collapse:collapse;font-size:12px}
.garch th{color:var(--mut);font-weight:600;font-size:10px;text-align:right;padding:1px 3px}
.garch td{padding:2px 3px;text-align:right}
.garch td.gp{color:var(--mut);width:16px;text-align:center}
.garch td.gt{text-align:left;display:flex;align-items:center;gap:5px;white-space:nowrap;overflow:hidden}
.garch td.gt img{width:16px;border-radius:2px;flex:0 0 auto}
.garch td.gt span{overflow:hidden;text-overflow:ellipsis}
.garch tr.gq1{background:linear-gradient(90deg,rgba(34,224,140,.10),transparent)}
.garch tr.gq3{background:linear-gradient(90deg,rgba(255,211,90,.09),transparent)}
.ggrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px}
.gg{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 12px;text-align:center;text-decoration:none;color:var(--txt);transition:.15s}
.gg:hover{border-color:var(--gold);transform:translateY(-2px)}
.gg .flag{width:50px;border-radius:5px;box-shadow:0 3px 10px #0007}
.ggc{color:var(--gold);font-size:12px;margin-top:8px}
.ggn{font-weight:700;font-size:15px;margin-top:6px}
.ggl{color:var(--mut);font-size:12px;margin-top:6px}
.brand-logo{width:84px;height:84px;border-radius:18px;object-fit:cover;box-shadow:0 6px 20px #0008;border:2px solid var(--line);display:block;margin:2px auto 8px}
.sponsor{color:var(--gold);font-size:14px;font-weight:700;font-style:italic;margin:8px auto 2px;max-width:600px;line-height:1.35}
.sponsor-sub{display:block;color:var(--mut);font-weight:500;font-style:normal;font-size:12px;margin-top:3px}
@media(max-width:560px){.brand-logo{width:66px;height:66px}.sponsor{font-size:12px;padding:0 10px}}
.liveband{margin:10px auto 0;max-width:760px;padding:10px 16px;border-radius:12px;font-size:14px;font-weight:600;text-align:center}
.liveband.live{background:#2a1224;border:1px solid #c0392b;color:#ffd0d8}
.liveband.next{background:#141d36;border:1px solid var(--line);color:var(--mut)}
.liveband .lf{width:18px;vertical-align:-4px;border-radius:2px;margin:0 3px}
.liveband b{color:#fff}.liveband.next b{color:var(--txt)}
.lvsub{font-weight:500;opacity:.85}
.lvdot{display:inline-block;width:9px;height:9px;border-radius:50%;background:#ff3b5c;animation:lvp 1.4s infinite}
@keyframes lvp{0%{box-shadow:0 0 0 0 #ff3b5c88}70%{box-shadow:0 0 0 8px #ff3b5c00}100%{box-shadow:0 0 0 0 #ff3b5c00}}
.rday{margin:8px 0 14px}
.rdate{color:var(--gold);font-size:12px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--line);padding-bottom:6px;margin-bottom:10px}
.rmatch{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin-bottom:8px}
.rsc{display:flex;align-items:center;justify-content:center;gap:8px;font-size:15px;flex-wrap:wrap}
.rsc .flag{width:30px;border-radius:3px;box-shadow:0 2px 6px #0007}
.rsc .rt{font-weight:600;min-width:88px;text-align:center}
.rscore{font-size:22px;font-weight:800;color:var(--gold);padding:0 4px}
.rscore i{color:var(--mut);font-style:normal;margin:0 3px}
.rwho{font-size:12px;color:var(--mut);text-align:center;margin-top:7px}
.rwho.hit{color:#16d97b;font-weight:600}.rwho.gan{color:#b9c2e8}.rwho.none{color:#6b7398;font-style:italic}
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
    bracket_html = build_real_bracket(rg, rk, eq, fixture, terceros, NM, ISO) if rg else ''
    groups_archive = build_groups_archive(rg, eq, fixture, NM, ISO)
    out = render(players, has, state, real_view, fxno, NM, ISO, ranks, miles, is_demo=False, n_played=len(rg), real_group=rg, bracket_html=bracket_html, groups_archive=groups_archive)
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
    bracket_html = build_real_bracket(rg, rk, eq, fixture, terceros, NM, ISO) if rg else ''
    groups_archive = build_groups_archive(rg, eq, fixture, NM, ISO)
    out = render(players, has, state, real_view, fxno, NM, ISO, ranks, miles, is_demo=True, n_played=len(rg), real_group=rg, bracket_html=bracket_html, groups_archive=groups_archive)
    print(f'{out} (DEMO) generado · {len(players)} jugadores · líder {players[0]["name"]} {players[0]["sc"]["total"]}')


if __name__ == '__main__':
    if '--demo' in sys.argv:
        run_demo()
    else:
        run_real()
