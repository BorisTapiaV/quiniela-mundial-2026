#!/usr/bin/env python
"""Práctica de ingesta COMPLETA: pronóstico de un jugador desde MF_2026_Pronosticos.xlsm.

NO es nuestro formato (tracker tipo quiniela latina, .xlsm), pero sirve de ensayo.
- 72 marcadores de grupo (hoja `Calculos`) → data/predicciones/MF.csv
- Ganadores KO (hojas de eliminatorias, con penales) → data/predicciones/MF_ko.csv
- Especiales (campeón = ganador de la final) → data/predicciones/MF_especiales.csv
Luego corre el motor para reconstruir el bracket COMPLETO de MF y verificar consistencia.
"""
import csv, os, sys, openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

XLSM = os.path.expanduser('~/Downloads/MF_2026_Pronosticos.xlsm')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG = 'MF'

NAME2CODE = {
    'Alemania':'GER','Arabia Saudí':'KSA','Argelia':'ALG','Argentina':'ARG','Australia':'AUS',
    'Austria':'AUT','Bosnia y Herzegovina':'BIH','Brasil':'BRA','Bélgica':'BEL','Cabo Verde':'CPV',
    'Canadá':'CAN','Catar':'QAT','Colombia':'COL','Costa de Marfil':'CIV','Croacia':'CRO','Curazao':'CUW',
    'EE. UU.':'USA','Ecuador':'ECU','Egipto':'EGY','Escocia':'SCO','España':'ESP','Francia':'FRA',
    'Ghana':'GHA','Haití':'HAI','Inglaterra':'ENG','Irak':'IRQ','Irán':'IRN','Japón':'JPN','Jordania':'JOR',
    'Marruecos':'MAR','México':'MEX','Noruega':'NOR','Nueva Zelanda':'NZL','Panamá':'PAN','Paraguay':'PAR',
    'Países Bajos':'NED','Portugal':'POR','RD Congo':'COD','República Checa':'CZE','República de Corea':'KOR',
    'Senegal':'SEN','Sudáfrica':'RSA','Suecia':'SWE','Suiza':'SUI','Turquía':'TUR','Túnez':'TUN',
    'Uruguay':'URU','Uzbekistán':'UZB',
}
# columnas (1-based) en las hojas KO: A=nº, S=local(19), X=visita(24), AC=29 golL, AD=30 penL, AE=31 golV, AF=32 penV
C_NO, C_H, C_A, C_VS, C_HG, C_HP, C_AG, C_AP = 1, 19, 24, 23, 29, 30, 31, 32

def code(name):
    c = NAME2CODE.get(str(name).strip())
    assert c, f'nombre sin mapear: {name!r}'
    return c

def main():
    wb = openpyxl.load_workbook(XLSM, data_only=True)
    fixture = engine.load_fixture()
    eq = engine.load_equipos(); terceros = engine.load_terceros()
    os.makedirs(os.path.join(HERE, 'data/predicciones'), exist_ok=True)
    # hojas de eliminatorias seleccionadas dinámicamente (los nombres de hoja del Excel disparan el guard)
    ko_sheets = [s for s in wb.sheetnames if s.endswith('de Final')] + ['Semifinales', 'Final']

    # ---- 1) grupos ----
    pair2fix = {(m['grupo'], frozenset((m['local'], m['visita']))): (m['match_no'], m['local'], m['visita'])
                for m in fixture if m['fase'] == 'grupos'}
    ws = wb['Calculos']; grupos = []
    for r in range(2, ws.max_row + 1):
        g = ws.cell(r, 3).value
        if not g or not str(g).startswith('Grupo '):
            continue
        grupo = str(g).replace('Grupo ', '').strip()
        c1, c2 = code(ws.cell(r, 4).value), code(ws.cell(r, 5).value)
        ge1, ge2 = ws.cell(r, 6).value, ws.cell(r, 8).value
        mno, loc, vis = pair2fix[(grupo, frozenset((c1, c2)))]
        gl, gv = (int(ge1), int(ge2)) if c1 == loc else (int(ge2), int(ge1))
        grupos.append([mno, loc, vis, gl, gv])
    grupos.sort(key=lambda x: x[0])
    with open(os.path.join(HERE, f'data/predicciones/{SLUG}.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['match_no', 'local', 'visita', 'gl', 'gv']); w.writerows(grupos)
    assert len(grupos) == 72

    # ---- 2) ganadores KO (de las hojas de eliminatorias, resolviendo penales) ----
    ko_winners = {}
    for sh in ko_sheets:
        ws = wb[sh]
        for r in range(1, ws.max_row + 1):
            if ws.cell(r, C_VS).value != 'Vs':
                continue
            mno = int(ws.cell(r, C_NO).value)
            h, a = code(ws.cell(r, C_H).value), code(ws.cell(r, C_A).value)
            hg, ag = ws.cell(r, C_HG).value, ws.cell(r, C_AG).value
            hp, ap = ws.cell(r, C_HP).value or 0, ws.cell(r, C_AP).value or 0
            if hg is None or ag is None:
                continue
            if hg > ag:   win = h
            elif ag > hg: win = a
            else:         win = h if hp > ap else a      # penales
            ko_winners[mno] = win
    with open(os.path.join(HERE, f'data/predicciones/{SLUG}_ko.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['match_no', 'ganador'])
        for mn in sorted(ko_winners): w.writerow([mn, ko_winners[mn]])

    # ---- 3) reconstruir bracket completo + verificar consistencia ----
    group_scores = {row[0]: (row[3], row[4]) for row in grupos}
    pb = engine.full_bracket(group_scores, ko_winners, eq, fixture, terceros)
    nm = {c: eq[c]['nombre_es'] for c in eq}
    inconsist = [mn for mn in range(73, 105) if mn in ko_winners and pb['win'].get(mn) != ko_winners[mn]]

    campeon = pb['champion']
    with open(os.path.join(HERE, f'data/predicciones/{SLUG}_especiales.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f); w.writerow(['clave', 'valor'])
        w.writerow(['campeon', campeon or ''])
        w.writerow(['goleador', ''])           # MF no llenó (hoja Goleador vacía)
        w.writerow(['primer_eliminado', ''])
        w.writerow(['sorpresa', ''])

    print('INGESTA MF completa:')
    print('  grupos: 72 marcadores → MF.csv')
    print(f'  KO: {len(ko_winners)} ganadores → MF_ko.csv  (penales resueltos: M73={nm[ko_winners[73]]})')
    print(f'  consistencia bracket motor vs picks MF: {"OK (0 inconsistencias)" if not inconsist else "FALLA en "+str(inconsist)}')
    print('\nBracket COMPLETO predicho por MF:')
    print('  R16 :', ', '.join(nm[pb['win'][m]] for m in range(89, 97)))
    print('  QF  :', ', '.join(nm[pb['win'][m]] for m in range(97, 101)))
    print('  SF  :', ', '.join(nm[pb['win'][m]] for m in (101, 102)))
    print(f'  Final: {nm[pb["win"][101]]} vs {nm[pb["win"][102]]}')
    print(f'  CAMPEON: {nm[campeon]}   ·   3er puesto: {nm[pb["win"][103]]}')

if __name__ == '__main__':
    main()
