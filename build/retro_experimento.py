#!/usr/bin/env python
"""Retrospectiva del experimento de pronóstico (La Casa) vs los resultados reales.

Cierra el loop del experimento del 2026-06-07 (scouting 61 agentes + validación de
consenso → planilla CASA). Computa, desde los resultados reales cargados en
data/resultados*.csv, cuánto acertó La Casa en: ganadores de grupo, marcadores
exactos, semifinalistas, finalistas, campeón, y los dos especiales retirados.

Reproducible: `python build/retro_experimento.py`. Fuente del análisis escrito:
referencias/RETROSPECTIVA_EXPERIMENTO_PRONOSTICO_2026-07.md
"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine, gen_jugador

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(HERE, 'data', 'predicciones')

eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
def nm(c): return eq[c].get('nombre', c) if c in eq else c


def load_casa():
    cg = {}
    for r in csv.DictReader(open(os.path.join(PRED, 'CASA.csv'), encoding='utf-8')):
        cg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    cko = {}
    for r in csv.DictReader(open(os.path.join(PRED, 'CASA_ko.csv'), encoding='utf-8')):
        if r['ganador']:
            cko[int(r['match_no'])] = r['ganador']
    cesp = {r['clave']: r['valor'] for r in
            csv.DictReader(open(os.path.join(PRED, 'CASA_especiales.csv'), encoding='utf-8'))}
    return cg, cko, cesp


def main():
    rg, rk = gen_jugador._load_results()
    real = engine.full_bracket(rg, rk, eq, fixture, terceros)
    cg, cko, cesp = load_casa()
    casa = engine.full_bracket(cg, cko, eq, fixture, terceros)

    print('=== GANADORES DE GRUPO (1º) — La Casa vs REAL ===')
    hits = 0
    for g in 'ABCDEFGHIJKL':
        p = casa['standings'][g][0]['code']; r = real['standings'][g][0]['code']
        ok = p == r; hits += ok
        print(f'  {g}: pred {nm(p):<16} | real {nm(r):<16} {"✅" if ok else "❌"}')
    print(f'  --> {hits}/12 ganadores de grupo')

    def names(s): return sorted(nm(c) for c in s)
    print('\n=== FASES FINALES ===')
    print(f'  Semifinalistas pred: {names(casa["sets"]["SF"])}')
    print(f'  Semifinalistas real: {names(real["sets"]["SF"])}')
    print(f'  --> {len(set(casa["sets"]["SF"]) & set(real["sets"]["SF"]))}/4')
    print(f'  Finalistas pred: {names(casa["sets"]["Final"])}')
    print(f'  Finalistas real: {names(real["sets"]["Final"])}')
    print(f'  --> {len(set(casa["sets"]["Final"]) & set(real["sets"]["Final"]))}/2')
    print(f'  Campeón pred: {nm(cesp.get("campeon",""))} | real: {nm(real["champion"])} '
          f'{"✅" if cesp.get("campeon") == real["champion"] else "❌"}')
    print(f'  Goleador pred: {cesp.get("goleador")} | real: Kylian Mbappé (10)')

    ex = sum(1 for mn, gv in rg.items() if cg.get(mn) == gv)
    print(f'\n=== EXACTOS DE GRUPO: {ex}/72 ===')

    r32 = set()
    for a, b in real['r32'].values():
        r32.add(a); r32.add(b)
    print('\n=== ESPECIALES RETIRADOS (referencia) ===')
    print(f'  Sorpresa Bosnia (BIH) avanzó a 16avos? {"SÍ" if "BIH" in r32 else "NO"} (predicho 2º Grupo B)')
    print(f'  Primer eliminado Cabo Verde (CPV) avanzó? {"SÍ" if "CPV" in r32 else "NO"} (predicho primer eliminado)')


if __name__ == '__main__':
    main()
