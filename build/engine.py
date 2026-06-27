#!/usr/bin/env python
"""Motor de cálculo de la quiniela Mundial 2026.

Parte 1 (este archivo, fase 1): tablas de posiciones con desempates FIFA,
ranking de los 8 mejores terceros, y armado del R32 vía la tabla de 495.

Desempates de grupo implementados (Art 13):
  pts → H2H(pts, dif, goles entre empatados) → dif global → goles global → seed (pos del sorteo).
  ⚠️ NO se modela 'conducta' (tarjetas) ni ranking FIFA: el jugador predice marcadores,
  no tarjetas. El seed (posición de sorteo 1-4) actúa como desempate final determinístico.
  Aproximación pragmática para un pool familiar (la recursión exacta FIFA de subconjuntos
  parciales no se implementa; se marca `tie_flag` si dos quedan idénticos antes del seed).
"""
import csv, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # quiniela/
DATA = os.path.join(HERE, 'data')

# etiqueta de slot de tercero -> nº de partido R32 (del reglamento / tabla 495)
THIRD_SLOT_MATCH = {
    '3-ABCDF': 74, '3-CDFGH': 77, '3-CEFHI': 79, '3-EHIJK': 80,
    '3-BEFIJ': 81, '3-AEHIJ': 82, '3-EFGIJ': 85, '3-DEIJL': 87,
}

# ---------- carga ----------
def load_equipos():
    eq = {}
    with open(os.path.join(DATA, 'equipos.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            eq[r['code']] = {'grupo': r['grupo'], 'pos': int(r['pos']),
                             'nombre_es': r['nombre_es'], 'iso': r['iso_bandera']}
    return eq

def load_fixture():
    rows = []
    with open(os.path.join(DATA, 'fixture.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            r['match_no'] = int(r['match_no'])
            rows.append(r)
    return rows

def load_terceros():
    t = {}
    with open(os.path.join(DATA, 'terceros_495.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            t[r['combo']] = {k: v for k, v in r.items() if k != 'combo'}
    return t

# ---------- posiciones de grupo ----------
def compute_standings(teams, matches, seed):
    """teams: lista de 4 códigos. matches: lista (home,away,gh,ga) con goles ya jugados.
    seed: dict code->pos sorteo (1-4). Devuelve lista ordenada de dicts con stats + pos + tie_flag."""
    st = {t: {'code': t, 'pts': 0, 'gf': 0, 'ga': 0, 'w': 0, 'd': 0, 'l': 0} for t in teams}
    for h, a, gh, ga in matches:
        st[h]['gf'] += gh; st[h]['ga'] += ga
        st[a]['gf'] += ga; st[a]['ga'] += gh
        if gh > ga:   st[h]['pts'] += 3; st[h]['w'] += 1; st[a]['l'] += 1
        elif gh < ga: st[a]['pts'] += 3; st[a]['w'] += 1; st[h]['l'] += 1
        else:         st[h]['pts'] += 1; st[a]['pts'] += 1; st[h]['d'] += 1; st[a]['d'] += 1
    for t in st.values():
        t['gd'] = t['gf'] - t['ga']

    def h2h(block):
        """mini-tabla entre los equipos de `block` (solo partidos entre ellos)."""
        bs = {t: {'pts': 0, 'gf': 0, 'ga': 0} for t in block}
        for h, a, gh, ga in matches:
            if h in bs and a in bs:
                bs[h]['gf'] += gh; bs[h]['ga'] += ga
                bs[a]['gf'] += ga; bs[a]['ga'] += gh
                if gh > ga:   bs[h]['pts'] += 3
                elif gh < ga: bs[a]['pts'] += 3
                else:         bs[h]['pts'] += 1; bs[a]['pts'] += 1
        return {t: (v['pts'], v['gf'] - v['ga'], v['gf']) for t, v in bs.items()}

    # ordenar: por puntos, y dentro de bloques empatados por H2H → global → seed
    order = sorted(teams, key=lambda t: -st[t]['pts'])
    result, i = [], 0
    while i < len(order):
        j = i
        while j < len(order) and st[order[j]]['pts'] == st[order[i]]['pts']:
            j += 1
        block = order[i:j]
        if len(block) > 1:
            hk = h2h(block)
            block = sorted(block, key=lambda t: (hk[t][0], hk[t][1], hk[t][2],
                                                 st[t]['gd'], st[t]['gf'], -seed[t]), reverse=True)
        result.extend(block)
        i = j

    out = []
    for pos, t in enumerate(result, 1):
        d = dict(st[t]); d['pos'] = pos; out.append(d)
    # tie_flag: dos equipos con stats globales idénticas (antes de seed) — revisar
    for k in range(len(out) - 1):
        a, b = out[k], out[k + 1]
        if (a['pts'], a['gd'], a['gf']) == (b['pts'], b['gd'], b['gf']):
            a['tie_flag'] = b['tie_flag'] = True
    return out

def compute_all_standings(results_by_group, eq):
    """results_by_group: dict grupo -> lista (home,away,gh,ga). Devuelve dict grupo -> standings."""
    allst = {}
    for g in 'ABCDEFGHIJKL':
        teams = [c for c, v in eq.items() if v['grupo'] == g]
        seed = {c: eq[c]['pos'] for c in teams}
        allst[g] = compute_standings(teams, results_by_group[g], seed)
    return allst

# ---------- mejores terceros ----------
def rank_thirds(all_standings):
    """Devuelve (combo_8_grupos_ordenado, dict grupo->3er_code, lista_ordenada, 4_grupos_fuera)."""
    thirds = [(g, st[2]) for g, st in all_standings.items()]  # (grupo, dict del 3º)
    thirds.sort(key=lambda x: (x[1]['pts'], x[1]['gd'], x[1]['gf'], x[0]), reverse=True)
    # nota: x[0] (letra grupo) como último criterio = determinístico (proxy de ranking/conducta no disponibles)
    top8 = thirds[:8]
    out4 = [g for g, _ in thirds[8:]]
    combo = ''.join(sorted(g for g, _ in top8))
    third_code_by_group = {g: st['code'] for g, st in [(g, all_standings[g][2]) for g in all_standings]}
    return combo, third_code_by_group, top8, out4

# ---------- armado R32 ----------
def build_r32(all_standings, fixture, terceros):
    """Devuelve dict match_no(73-88) -> (code_local, code_visita)."""
    combo, third_by_group, _, _ = rank_thirds(all_standings)
    row = terceros[combo]  # m74..m87 -> letra de grupo cuyo 3º juega ese partido

    def resolve(slot):
        if slot.startswith('3-'):
            mn = THIRD_SLOT_MATCH[slot]
            g = row[f'm{mn}']
            return all_standings[g][2]['code']           # 3º de ese grupo
        pos = int(slot[0]); g = slot[1]
        return all_standings[g][pos - 1]['code']          # 1X o 2X

    r32 = {}
    for m in fixture:
        if m['fase'] == 'R32':
            r32[m['match_no']] = (resolve(m['local']), resolve(m['visita']))
    return r32


def groups_complete(group_scores, fixture):
    """Conjunto de grupos (A..L) con sus 6 partidos ya jugados en group_scores."""
    total, played = {}, {}
    for m in fixture:
        if m['fase'] == 'grupos':
            g = m['grupo']
            total[g] = total.get(g, 0) + 1
            if m['match_no'] in group_scores:
                played[g] = played.get(g, 0) + 1
    return {g for g in total if played.get(g, 0) == total[g]}


def r32_partial(group_scores, eq, fixture, terceros):
    """Resuelve los cruces del R32 con la información disponible HOY.

    Devuelve dict match_no(73-88) -> (code_local|None, code_visita|None).
    - Si los 72 de grupo están jugados → bracket completo (incluye terceros).
    - Si no → resuelve cada slot 1X/2X cuyo grupo ya esté cerrado; los slots de
      tercero (3-XXXX) y los de grupos en juego quedan None (placeholder en la vista).
    """
    allst = compute_all_standings(group_results_by_group(group_scores, fixture), eq)
    if len(group_scores) >= 72:
        return build_r32(allst, fixture, terceros)
    done = groups_complete(group_scores, fixture)

    def resolve(slot):
        if slot.startswith('3-'):
            return None                                   # tercero: depende del combo de los 12 grupos
        pos = int(slot[0]); g = slot[1]
        if g not in done:
            return None                                   # grupo aún en juego
        return allst[g][pos - 1]['code']

    out = {}
    for m in fixture:
        if m['fase'] == 'R32':
            out[m['match_no']] = (resolve(m['local']), resolve(m['visita']))
    return out


def bracket_partial(group_scores, ko_winners, eq, fixture, terceros):
    """Cuadro KO completo resuelto con lo disponible HOY (para la vista 'cuadro real').

    Devuelve (teams, win):
      teams[mn] = (code_local|None, code_visita|None)   None = aún por definir
      win[mn]   = code_ganador|None                     None = aún sin jugar/cargar
    R32 vía r32_partial (placeholders para tercero/grupo en juego); R16→Final se
    llenan a medida que entran ganadores en data/resultados_ko.csv. Sirve para el
    estado parcial sin reventar como build_r32 (que exige los 72 de grupo)."""
    r32 = r32_partial(group_scores, eq, fixture, terceros)
    ko = sorted([m for m in fixture if m['fase'] != 'grupos'], key=lambda m: m['match_no'])
    teams, win, lose = {}, {}, {}

    def slot_team(slot):
        if slot.startswith('W'): return win.get(int(slot[1:]))
        if slot.startswith('L'): return lose.get(int(slot[1:]))
        return None

    for m in ko:
        mn = m['match_no']
        a, b = r32[mn] if mn in r32 else (slot_team(m['local']), slot_team(m['visita']))
        teams[mn] = (a, b)
        w = ko_winners.get(mn)
        if w and a and b and w in (a, b):
            win[mn] = w; lose[mn] = b if w == a else a
        else:
            win[mn] = None; lose[mn] = None
    return teams, win

# ---------- autotest ----------
def _selftest():
    import random
    random.seed(42)
    eq = load_equipos(); fixture = load_fixture(); terceros = load_terceros()

    # partidos de grupo desde fixture (los 72), con marcadores sintéticos deterministas
    grp_matches = {g: [] for g in 'ABCDEFGHIJKL'}
    for m in fixture:
        if m['fase'] == 'grupos':
            gh = random.randint(0, 4); ga = random.randint(0, 4)
            grp_matches[m['grupo']].append((m['local'], m['visita'], gh, ga))

    allst = compute_all_standings(grp_matches, eq)

    # --- invariantes de posiciones ---
    for g, st in allst.items():
        assert len(st) == 4 and [t['pos'] for t in st] == [1, 2, 3, 4], f'grupo {g} mal ordenado'
        # puntos no crecientes
        pts = [t['pts'] for t in st]
        assert pts == sorted(pts, reverse=True), f'grupo {g}: pts no ordenados'
        # cada equipo jugó 3
        for t in st:
            assert t['w'] + t['d'] + t['l'] == 3, f'{t["code"]} no jugó 3'
        # suma de puntos del grupo coherente (3*(no-empates) + 2*empates)
        assert sum(t['pts'] for t in st) <= 18
    flags = sum(1 for g in allst for t in allst[g] if t.get('tie_flag'))

    # --- invariantes de terceros ---
    combo, third_by_group, top8, out4 = rank_thirds(allst)
    assert len(combo) == 8 and len(set(combo)) == 8
    assert len(out4) == 4
    assert combo in terceros, f'combo {combo} no está en la tabla 495'
    # los 8 elegidos no son peores que los 4 fuera (orden pts,gd,gf)
    key = lambda s: (s['pts'], s['gd'], s['gf'])
    worst_in = min(key(allst[g][2]) for g, _ in top8)
    best_out = max(key(allst[g][2]) for g in out4) if out4 else (-9, -9, -9)
    assert worst_in >= best_out, 'un tercero fuera es mejor que uno dentro'

    # --- invariantes del R32 ---
    r32 = build_r32(allst, fixture, terceros)
    assert len(r32) == 16, f'R32 debe tener 16 partidos, tiene {len(r32)}'
    teams = [t for pair in r32.values() for t in pair]
    assert len(teams) == 32 and len(set(teams)) == 32, 'R32 no tiene 32 equipos distintos'
    # ningún cruce entre equipos del mismo grupo
    for mn, (a, b) in r32.items():
        assert eq[a]['grupo'] != eq[b]['grupo'], f'M{mn}: {a} y {b} mismo grupo'
    # los 32 = 12 primeros + 12 segundos + 8 terceros
    firsts = {allst[g][0]['code'] for g in allst}
    seconds = {allst[g][1]['code'] for g in allst}
    thirds_in = {allst[g][2]['code'] for g, _ in top8}
    assert set(teams) == firsts | seconds | thirds_in, 'composición R32 incorrecta'

    print('engine fase 1 — autotest OK')
    print(f'  12 grupos ordenados con desempates FIFA  (tie_flags sin resolver por goles: {flags})')
    print(f'  8 mejores terceros: combo={combo}  fuera={sorted(out4)}')
    print(f'  R32: 16 partidos, 32 equipos distintos, sin choque de grupo, composición correcta')
    print(f'  ejemplo M73={r32[73]}  ·  M79(1A v 3º)={r32[79]}  ·  M88={r32[88]}')

# ---------- resolución KO (cascada) ----------
def resolve_bracket(r32, ko_winners, fixture):
    """r32: dict mn(73-88)->(A,B). ko_winners: dict mn->code ganador (picks o real).
    Devuelve (teams, win, lose) para M73-M104. Resuelve W##/L## en orden."""
    teams, win, lose = {}, {}, {}
    ko = sorted([m for m in fixture if m['fase'] != 'grupos'], key=lambda m: m['match_no'])

    def slot_team(slot):
        if slot.startswith('W'): return win.get(int(slot[1:]))
        if slot.startswith('L'): return lose.get(int(slot[1:]))
        return None

    for m in ko:
        mn = m['match_no']
        A, B = r32[mn] if mn in r32 else (slot_team(m['local']), slot_team(m['visita']))
        teams[mn] = (A, B)
        w = ko_winners.get(mn)
        if w in (A, B) and w is not None:
            win[mn] = w; lose[mn] = B if w == A else A
        else:
            win[mn] = None; lose[mn] = None
    return teams, win, lose

def reaching_sets(r32, win):
    """Conjuntos de equipos que ALCANZAN cada ronda + campeón."""
    qualified = set()
    for a, b in r32.values():
        qualified.update((a, b))
    sets = {
        'R32': qualified,
        'R16': {win[mn] for mn in range(73, 89) if win.get(mn)},
        'QF':  {win[mn] for mn in range(89, 97) if win.get(mn)},
        'SF':  {win[mn] for mn in range(97, 101) if win.get(mn)},
        'Final': {win[mn] for mn in range(101, 103) if win.get(mn)},
    }
    return sets, win.get(104)

def group_results_by_group(group_scores, fixture):
    """Convierte marcadores en formato match_no->(gl,gv) a grupo->lista (home,away,gl,gv)."""
    by = {g: [] for g in 'ABCDEFGHIJKL'}
    for m in fixture:
        if m['fase'] == 'grupos' and m['match_no'] in group_scores:
            gl, gv = group_scores[m['match_no']]
            by[m['grupo']].append((m['local'], m['visita'], gl, gv))
    return by

def full_bracket(group_scores, ko_winners, eq, fixture, terceros):
    """Bracket completo desde marcadores de grupo (match_no->(gl,gv)) + ganadores KO.
    Sirve igual para resultados reales que para predicciones."""
    allst = compute_all_standings(group_results_by_group(group_scores, fixture), eq)
    r32 = build_r32(allst, fixture, terceros)
    teams, win, lose = resolve_bracket(r32, ko_winners, fixture)
    sets, champ = reaching_sets(r32, win)
    return {'standings': allst, 'r32': r32, 'teams': teams, 'win': win,
            'lose': lose, 'sets': sets, 'champion': champ}

# ---------- scoring ----------
W_GROUP = {'exact': 5, 'diff': 3, 'result': 2}                  # escalonado (nivel más alto)
# Rebalance 2026-06-07 → reparto ~50% grupos / 35% KO / 15% especiales (research disyuntiva,
# escalada INTERMEDIA no geométrica; campeón alto pero no dominante ~7% por paradoja de Aldous).
W_ADV = {'R32': 2, 'R16': 4, 'QF': 6, 'SF': 10, 'Final': 16}    # avance por fase = 248 máx (35%)
W_ESP = {'campeon': 50, 'goleador': 25, 'primer_eliminado': 20, 'sorpresa': 15}  # = 110 máx (15%)

def _outcome(l, v):
    return (l > v) - (l < v)

def score_group_match(pred, real, w=W_GROUP):
    pl, pv = pred; rl, rv = real
    if (pl, pv) == (rl, rv):       return w['exact']
    if (pl - pv) == (rl - rv):     return w['diff']    # misma diferencia ⇒ 1X2 correcto
    if _outcome(pl, pv) == _outcome(rl, rv): return w['result']
    return 0

def score_player(pred_group, pred_ko, real_bracket, real_group,
                 pred_especiales, real_especiales, eq, fixture, terceros):
    """Puntaje total de un jugador contra el bracket/resultados reales."""
    pb = full_bracket(pred_group, pred_ko, eq, fixture, terceros)
    grupo = sum(score_group_match(pred_group[mn], real_group[mn])
                for mn in real_group if mn in pred_group)
    avance, det = 0, {}
    groups_done = len(real_group) >= 72       # nadie "clasifica a R32" hasta que terminan los grupos
    for rnd, wt in W_ADV.items():
        if rnd == 'R32' and not groups_done:
            n = 0                              # grupos en curso/sin jugar: avance R32 aún no cuenta
        else:
            n = len(pb['sets'][rnd] & real_bracket['sets'][rnd])
        det[rnd] = n * wt; avance += n * wt
    esp = 0
    if pb['champion'] and pb['champion'] == real_bracket['champion']:
        esp += W_ESP['campeon']
    for k in ('goleador', 'primer_eliminado', 'sorpresa'):
        if pred_especiales.get(k) and pred_especiales.get(k) == real_especiales.get(k):
            esp += W_ESP[k]
    return {'grupo': grupo, 'avance': avance, 'avance_detalle': det,
            'especiales': esp, 'total': grupo + avance + esp, 'bracket': pb}

def _simulate_ko(r32, fixture, rng):
    """Genera un resultado KO real consistente eligiendo ganador al azar ronda a ronda."""
    win, lose, winners = {}, {}, {}
    ko = sorted([m for m in fixture if m['fase'] != 'grupos'], key=lambda m: m['match_no'])

    def slot(s):
        return win[int(s[1:])] if s.startswith('W') else lose[int(s[1:])]
    for m in ko:
        mn = m['match_no']
        A, B = r32[mn] if mn in r32 else (slot(m['local']), slot(m['visita']))
        w = rng.choice([A, B]); win[mn] = w; lose[mn] = B if w == A else A; winners[mn] = w
    return winners

def _selftest2():
    import random
    rng = random.Random(7)
    eq = load_equipos(); fixture = load_fixture(); terceros = load_terceros()

    # --- escenario REAL ---
    real_group = {}
    for m in fixture:
        if m['fase'] == 'grupos':
            real_group[m['match_no']] = (rng.randint(0, 4), rng.randint(0, 4))
    real_r32 = build_r32(compute_all_standings(group_results_by_group(real_group, fixture), eq), fixture, terceros)
    real_ko = _simulate_ko(real_r32, fixture, rng)
    real_b = full_bracket(real_group, real_ko, eq, fixture, terceros)
    real_esp = {'campeon': real_b['champion'], 'goleador': 'MESSI',
                'primer_eliminado': 'HAI', 'sorpresa': 'CUW'}

    # --- jugador PERFECTO (clava todo) ---
    pj = score_player(real_group, real_ko, real_b, real_group, real_esp, real_esp, eq, fixture, terceros)
    max_grupo = 72 * W_GROUP['exact']
    max_adv = (32 * W_ADV['R32'] + 16 * W_ADV['R16'] + 8 * W_ADV['QF']
               + 4 * W_ADV['SF'] + 2 * W_ADV['Final'])
    max_esp = sum(W_ESP.values())
    assert pj['grupo'] == max_grupo, (pj['grupo'], max_grupo)
    assert pj['avance'] == max_adv, (pj['avance'], max_adv)
    assert pj['especiales'] == max_esp, (pj['especiales'], max_esp)
    assert pj['total'] == max_grupo + max_adv + max_esp

    # --- jugador que clava GRUPOS pero falla KO y especiales ---
    bad_ko = _simulate_ko(real_r32, fixture, random.Random(99))
    pg = score_player(real_group, bad_ko, real_b, real_group,
                      {'goleador': 'X'}, real_esp, eq, fixture, terceros)
    assert pg['grupo'] == max_grupo                          # grupos perfectos
    assert pg['avance_detalle']['R32'] == 32 * W_ADV['R32']  # 32 clasificados correctos (grupos iguales)
    assert pg['avance'] <= max_adv and pg['total'] < pj['total']

    # --- jugador al azar: rango sano ---
    rg = {}
    for m in fixture:
        if m['fase'] == 'grupos':
            rg[m['match_no']] = (rng.randint(0, 4), rng.randint(0, 4))
    r_r32 = build_r32(compute_all_standings(group_results_by_group(rg, fixture), eq), fixture, terceros)
    rko = _simulate_ko(r_r32, fixture, rng)
    pr = score_player(rg, rko, real_b, real_group, {}, real_esp, eq, fixture, terceros)
    assert 0 <= pr['total'] <= pj['total']

    print('engine fase 2 — autotest OK')
    print(f'  jugador PERFECTO: grupo={pj["grupo"]} avance={pj["avance"]} esp={pj["especiales"]} → TOTAL {pj["total"]} (máximo)')
    print(f'  grupos-perfecto/KO-malo: grupo={pg["grupo"]} avance={pg["avance"]} total={pg["total"]} (R32 clasif={pg["avance_detalle"]["R32"]})')
    print(f'  jugador al azar: total={pr["total"]}  (avance det={pr["avance_detalle"]})')

if __name__ == '__main__':
    _selftest()
    _selftest2()
