#!/usr/bin/env python
"""Genera el informe de scouting (uso interno) desde data/scouting_48.json + CASA.
Salida: referencias/scouting-48-pronostico-casa.md
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    sc = json.load(open(os.path.join(HERE, 'data/scouting_48.json'), encoding='utf-8'))
    profiles = sc['profiles']; fuerza = sc['fuerza']
    prof = {p['code']: p for p in profiles}
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    NM = {c: eq[c]['nombre_es'] for c in eq}

    gs = {int(r['match_no']): (int(r['gl']), int(r['gv']))
          for r in csv.DictReader(open(os.path.join(HERE, 'data/predicciones/CASA.csv'), encoding='utf-8'))}
    ko = {int(r['match_no']): r['ganador']
          for r in csv.DictReader(open(os.path.join(HERE, 'data/predicciones/CASA_ko.csv'), encoding='utf-8'))}
    esp = {r['clave']: r['valor']
           for r in csv.DictReader(open(os.path.join(HERE, 'data/predicciones/CASA_especiales.csv'), encoding='utf-8'))}
    allst = engine.compute_all_standings(engine.group_results_by_group(gs, fixture), eq)
    pb = engine.full_bracket(gs, ko, eq, fixture, terceros)

    L = []
    L.append('# Scouting 48 selecciones + Pronóstico de La Casa — Mundial 2026')
    L.append('')
    L.append('> 🔒 **USO INTERNO (la "trampa" de Boris) — NO compartir con los jugadores.** Generado 2026-06-07 por un workflow de **61 agentes** (48 scouts web, 1 agente normalizador de fuerza, 12 agentes de grupo), con el prompt de scouting **optimizado por Leonor v4.5** (rúbrica de fuerza 0-100 comparable + triangulación de fuentes). Datos en `data/scouting_48.json`; pronóstico en `data/predicciones/CASA*.csv`.')
    L.append('')
    L.append('## 🏆 Pronóstico de La Casa')
    L.append('')
    L.append(f'- **Campeón:** {NM[esp["campeon"]]}')
    L.append(f'- **Final:** {NM[pb["win"][101]]} vs {NM[pb["win"][102]]}  ·  **3er puesto:** {NM[pb["win"][103]]}')
    L.append(f'- **Semifinalistas:** ' + ', '.join(NM[pb['win'][m]] for m in (97, 98, 99, 100)))
    L.append(f'- **Goleador:** {esp["goleador"]}  ·  **Primer eliminado:** {NM[esp["primer_eliminado"]]}  ·  **Sorpresa:** {NM[esp["sorpresa"]]}')
    L.append('')
    L.append('**Ganadores y 2º de cada grupo:**')
    L.append('')
    L.append('| Grupo | 1º | 2º | 3º | 4º |')
    L.append('|:-:|---|---|---|---|')
    for g in 'ABCDEFGHIJKL':
        st = allst[g]
        L.append(f'| {g} | {NM[st[0]["code"]]} | {NM[st[1]["code"]]} | {NM[st[2]["code"]]} | {NM[st[3]["code"]]} |')
    L.append('')

    L.append('## 📊 Ranking de fuerza (48 selecciones, normalizada)')
    L.append('')
    L.append('| # | Selección | Fuerza | Banda | FIFA | GF/p | GC/p | Goleador |')
    L.append('|:-:|---|:-:|---|:-:|:-:|:-:|---|')
    for i, c in enumerate(sorted(fuerza, key=lambda x: -fuerza[x]), 1):
        p = prof.get(c, {})
        L.append(f'| {i} | {NM[c]} | **{fuerza[c]}** | {p.get("banda","")} | {p.get("fifa_rank","")} | '
                 f'{p.get("gf_pm","")} | {p.get("ga_pm","")} | {p.get("goleador","")} |')
    L.append('')

    L.append('## 🔎 Perfiles por selección')
    L.append('')
    for c in sorted(fuerza, key=lambda x: -fuerza[x]):
        p = prof.get(c, {})
        L.append(f'### {NM[c]} ({c}) — fuerza {fuerza[c]} · {p.get("banda","")}')
        L.append(f'- **Estilo:** {p.get("estilo","")}')
        L.append(f'- **Fortalezas:** {p.get("fortalezas","")}')
        L.append(f'- **Debilidades:** {p.get("debilidades","")}')
        if p.get('bajas'):
            L.append(f'- **Bajas:** {p.get("bajas")}')
        L.append(f'- **Datos:** GF/p {p.get("gf_pm","")} · GC/p {p.get("ga_pm","")} · FIFA {p.get("fifa_rank","")} · '
                 f'goleador {p.get("goleador","")} · calidad {p.get("calidad_dato","")} · {p.get("fuentes","")} fuentes')
        nota = (p.get('nota','') or '').strip()
        if nota:
            L.append(f'- **Nota analista:** {nota}')
        L.append('')

    out = os.path.join(HERE, 'referencias/scouting-48-pronostico-casa.md')
    open(out, 'w', encoding='utf-8').write('\n'.join(L))
    print('informe escrito:', out, '·', len('\n'.join(L)), 'chars')

if __name__ == '__main__':
    main()
