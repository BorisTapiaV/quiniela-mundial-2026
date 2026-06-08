#!/usr/bin/env python
"""Procesa el output del workflow scouting-mundial-48 → pronóstico de 'La Casa'.

Lee los 48 perfiles + fuerzas normalizadas + predicciones de los 12 grupos del
workflow, y produce:
- data/predicciones/CASA.csv (72 marcadores de grupo)
- data/predicciones/CASA_ko.csv (ganadores KO por fuerza)
- data/predicciones/CASA_especiales.csv (campeón, goleador, 1º eliminado, sorpresa)
- data/scouting_48.json (perfiles, para el informe)
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.expanduser('~/AppData/Local/Temp/claude/C--Users-boris/49d00e54-60ab-4dce-824c-350a34e21fc9/tasks/w5u5gbvtj.output')

def main():
    data = json.load(open(OUT, encoding='utf-8'))
    res = data.get('result', data)
    profiles = res['profiles']
    fnorm = res.get('fuerza_normalizada', {})
    grupos = res['grupos']
    prof = {p['code']: p for p in profiles}
    # fuerza final: normalizada > fuerza_norm del perfil > fuerza
    fuerza = {}
    for c, p in prof.items():
        fuerza[c] = fnorm.get(c, p.get('fuerza_norm', p.get('fuerza', 50)))

    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    # pares de grupo -> (match_no, local, visita)
    pair = {(m['grupo'], frozenset((m['local'], m['visita']))): (m['match_no'], m['local'], m['visita'])
            for m in fixture if m['fase'] == 'grupos'}
    grp_of = {c: eq[c]['grupo'] for c in eq}

    # ---- 72 marcadores de grupo ----
    rows = []; faltan = []
    for g in grupos:
        for pa in g['partidos']:
            lc, vc = pa['local'], pa['visita']
            gl, gv = int(pa['gl']), int(pa['gv'])
            G = grp_of.get(lc)
            key = (G, frozenset((lc, vc)))
            if key not in pair:
                faltan.append((lc, vc)); continue
            mno, loc, vis = pair[key]
            if lc == loc: rows.append([mno, loc, vis, gl, gv])
            else:         rows.append([mno, loc, vis, gv, gl])
    rows.sort(key=lambda x: x[0])
    seen = {r[0] for r in rows}
    # si falta algún partido (grupo fallido), rellenar por fuerza
    for m in fixture:
        if m['fase'] == 'grupos' and m['match_no'] not in seen:
            a, b = m['local'], m['visita']
            fa, fb = fuerza.get(a, 50), fuerza.get(b, 50)
            d = (fa - fb) / 25.0
            gl = max(0, round(1.3 + max(d, 0)));  gv = max(0, round(1.3 + max(-d, 0)))
            rows.append([m['match_no'], a, b, gl, gv]); faltan.append(('relleno', m['match_no']))
    rows.sort(key=lambda x: x[0])
    base = os.path.join(HERE, 'data/predicciones')
    with open(os.path.join(base, 'CASA.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['match_no', 'local', 'visita', 'gl', 'gv']); w.writerows(rows)
    assert len(rows) == 72, f'esperaba 72, hay {len(rows)}'

    # ---- bracket por fuerza ----
    gs = {r[0]: (r[3], r[4]) for r in rows}
    allst = engine.compute_all_standings(engine.group_results_by_group(gs, fixture), eq)
    r32 = engine.build_r32(allst, fixture, terceros)

    def ko_by_strength(r32):
        win, lose, winners = {}, {}, {}
        ko = sorted([m for m in fixture if m['fase'] != 'grupos'], key=lambda m: m['match_no'])
        def slot(s): return win[int(s[1:])] if s.startswith('W') else lose[int(s[1:])]
        for m in ko:
            mn = m['match_no']
            A, B = r32[mn] if mn in r32 else (slot(m['local']), slot(m['visita']))
            wa = (fuerza.get(A, 50), prof.get(A, {}).get('gf_pm', 1))
            wb = (fuerza.get(B, 50), prof.get(B, {}).get('gf_pm', 1))
            w = A if wa >= wb else B
            win[mn] = w; lose[mn] = B if w == A else A; winners[mn] = w
        return winners
    ko = ko_by_strength(r32)
    with open(os.path.join(base, 'CASA_ko.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['match_no', 'ganador'])
        for mn in sorted(ko): w.writerow([mn, ko[mn]])

    pb = engine.full_bracket(gs, ko, eq, fixture, terceros)
    campeon = pb['champion']
    # especiales
    goleador = prof.get(campeon, {}).get('goleador', '')
    primer_elim = min(fuerza, key=lambda c: fuerza[c])                       # equipo más débil
    # sorpresa = el clasificado MÁS DÉBIL (la cenicienta que llega a la ronda de 32)
    r32_teams = pb['sets']['R32']
    sorpresa = min(r32_teams, key=lambda c: fuerza[c]) if r32_teams else None
    with open(os.path.join(base, 'CASA_especiales.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['clave', 'valor'])
        w.writerow(['campeon', campeon or ''])
        w.writerow(['goleador', goleador])
        w.writerow(['primer_eliminado', primer_elim])
        w.writerow(['sorpresa', sorpresa or ''])

    # guardar perfiles para el informe
    json.dump({'profiles': profiles, 'fuerza': fuerza}, open(os.path.join(HERE, 'data/scouting_48.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    NM = {c: eq[c]['nombre_es'] for c in eq}
    print(f'CASA: 72 marcadores ({len(faltan)} rellenos/incidencias: {faltan[:5]})')
    print('Ganadores de grupo:', ', '.join(f'{g}:{NM[allst[g][0]["code"]]}' for g in 'ABCDEFGHIJKL'))
    print(f'\n🏆 CAMPEÓN (La Casa): {NM[campeon]}  (fuerza {fuerza[campeon]})')
    print(f'   Final: {NM[pb["win"][101]]} vs {NM[pb["win"][102]]}  ·  3º: {NM[pb["win"][103]]}')
    print(f'   Semis: {", ".join(NM[pb["win"][m]] for m in (101,102))}')
    print(f'   Goleador: {goleador} · 1º eliminado: {NM[primer_elim]} (fuerza {fuerza[primer_elim]}) · Sorpresa: {NM[sorpresa]} (fuerza {fuerza[sorpresa]})')
    print('\nTop-10 fuerza:', ', '.join(f'{NM[c]} {fuerza[c]}' for c in sorted(fuerza, key=lambda x:-fuerza[x])[:10]))

if __name__ == '__main__':
    main()
