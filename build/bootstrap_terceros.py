#!/usr/bin/env python
"""Bootstrap de la tabla de 495 combinaciones de mejores terceros (formato 2026).

Fuente: hoja `AssignThird` del modelo Excel WCup_2026_4.2.6_en.xlsx
(rotulada "FIFA, 23.06.2025"). C(12,8)=495 combinaciones.

Cada fila: dado QUÉ 8 grupos aportan tercero clasificado (columna combo),
a qué partido de R32 va el tercero de cada grupo. Garantiza que dos equipos
del mismo grupo no se crucen en R32 (Annexe C del reglamento FIFA).

Produce data/terceros_495.csv (SoT). Verificación fuerte de correctitud.
"""
import csv, os, openpyxl

XLSX = os.path.expanduser('~/Downloads/WCup_2026_4.2.6_en.xlsx')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Columna AssignThird (D..K) -> nº de partido R32 que aloja ese slot de tercero.
# (verificado contra el reglamento Art 12.6: D='3-CEFHI'=1A=M79, etc.)
COL2MATCH = {4:79, 5:85, 6:81, 7:74, 8:82, 9:77, 10:87, 11:80}  # col idx -> Mxx
# Conjunto de grupos permitidos por cada slot (del reglamento / etiqueta 3-XYZ)
ALLOWED = {
    74:set('ABCDF'), 77:set('CDFGH'), 79:set('CEFHI'), 80:set('EHIJK'),
    81:set('BEFIJ'), 82:set('AEHIJ'), 85:set('EFGIJ'), 87:set('DEIJL'),
}
MATCHES = [74, 77, 79, 80, 81, 82, 85, 87]  # orden de columnas de salida

def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb['AssignThird']

    rows = []
    for r in range(8, 503):  # 495 filas de datos
        combo = ws.cell(r, 3).value  # col C
        if not combo:
            continue
        combo = str(combo).strip()
        # leer asignación: para cada columna D..K, qué grupo va al match COL2MATCH[col]
        assign = {}
        for col, m in COL2MATCH.items():
            assign[m] = str(ws.cell(r, col).value).strip()
        rows.append((combo, assign))

    # ---- verificaciones ----
    assert len(rows) == 495, f'esperaba 495 filas, hay {len(rows)}'
    seen = set()
    for combo, assign in rows:
        letters = set(combo)
        assert len(combo) == 8 and len(letters) == 8, f'combo invalido: {combo}'
        assert letters <= set('ABCDEFGHIJKL'), f'combo fuera de A-L: {combo}'
        assert combo not in seen, f'combo duplicado: {combo}'
        seen.add(combo)
        assert ''.join(sorted(combo)) == combo, f'combo no ordenado: {combo}'
        placed = [assign[m] for m in MATCHES]
        # los 8 terceros colocados son exactamente los 8 grupos del combo (permutacion)
        assert set(placed) == letters, f'{combo}: colocados {sorted(placed)} != combo'
        assert len(set(placed)) == 8, f'{combo}: grupo repetido en colocacion'
        # cada tercero va a un slot permitido (no choque de grupo en R32)
        for m in MATCHES:
            assert assign[m] in ALLOWED[m], f'{combo}: 3º de {assign[m]} no permitido en M{m} {sorted(ALLOWED[m])}'

    # escribir
    with open(os.path.join(HERE, 'data/terceros_495.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['combo'] + [f'm{m}' for m in MATCHES])
        for combo, assign in rows:
            w.writerow([combo] + [assign[m] for m in MATCHES])

    print(f'terceros_495.csv: {len(rows)} combinaciones')
    print('checks OK: 495 unicas, cada combo=8 grupos distintos ordenados,')
    print('           colocacion=permutacion del combo, cada 3º en slot permitido (sin choque de grupo)')
    print('columnas:', ['m%d' % m for m in MATCHES], '(grupo cuyo 3º juega ese partido R32)')
    print('ejemplo:', rows[0][0], '->', {f'M{m}': rows[0][1][m] for m in MATCHES})

if __name__ == '__main__':
    main()
