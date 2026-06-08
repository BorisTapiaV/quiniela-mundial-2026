#!/usr/bin/env python
"""Bootstrap del fixture completo (104 partidos) del Mundial 2026.

Fuente de fechas/horas/sedes/numero: tabla `tDatos` del modelo Excel
Fixture-Copa-Mundial-FIFA-2026_ClasesExcel.xlsx (hoja Recursos).
Fuente de los cruces de eliminatorias (slots): reglamento FIFA (Art 12.6-12.11),
ver reglas/02-clasificacion-cruces.md.

Produce data/fixture.csv (SoT). Verifica contra data/fixture_grupos.csv.

⚠️ Las fechas/sedes provienen de un modelo de terceros (ClasesExcel), NO de FIFA
primario. Marcar para verificar contra el calendario oficial FIFA antes de usar en serio.
"""
import csv, os, openpyxl

XLSX = os.path.expanduser('~/Downloads/Fixture-Copa-Mundial-FIFA-2026_ClasesExcel.xlsx')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # quiniela/

# Excel (ES, mayúsculas) -> código FIFA
NAME2CODE = {
    'ALEMANIA':'GER','ARABIA SAUDITA':'KSA','ARGELIA':'ALG','ARGENTINA':'ARG','AUSTRALIA':'AUS',
    'AUSTRIA':'AUT','BOSNIA y HERZEG.':'BIH','BRASIL':'BRA','BÉLGICA':'BEL','CABO VERDE':'CPV',
    'CANADÁ':'CAN','CATAR':'QAT','COLOMBIA':'COL','COREA del SUR':'KOR','COSTA de MARFIL':'CIV',
    'CROACIA':'CRO','CURAZAO':'CUW','ECUADOR':'ECU','EGIPTO':'EGY','ESCOCIA':'SCO','ESPAÑA':'ESP',
    'ESTADOS UNIDOS':'USA','FRANCIA':'FRA','GHANA':'GHA','HAITÍ':'HAI','INGLATERRA':'ENG','IRAK':'IRQ',
    'IRÁN':'IRN','JAPÓN':'JPN','JORDANIA':'JOR','MARRUECOS':'MAR','MÉXICO':'MEX','NORUEGA':'NOR',
    'NUEVA ZELANDA':'NZL','PANAMÁ':'PAN','PARAGUAY':'PAR','PAÍSES BAJOS':'NED','PORTUGAL':'POR',
    'REP. CHECA':'CZE','REP. del CONGO':'COD','SENEGAL':'SEN','SUDÁFRICA':'RSA','SUECIA':'SWE',
    'SUIZA':'SUI','TURQUÍA':'TUR','TÚNEZ':'TUN','URUGUAY':'URU','UZBEKISTÁN':'UZB',
}

# fase Excel -> código
FASE = {'Dieciseisavos':'R32','Octavos':'R16','Cuartos':'QF','Semifinal':'SF',
        'Tercer puesto':'3P','Final':'Final'}

# Cruces KO en términos de slots (reglamento FIFA Art 12.6-12.11)
# 1X=ganador grupo X · 2X=segundo · 3-XYZ=mejor 3º de esos grupos · W##=ganador M## · L##=perdedor M##
KO_SLOTS = {
    73:('2A','2B'),74:('1E','3-ABCDF'),75:('1F','2C'),76:('1C','2F'),77:('1I','3-CDFGH'),
    78:('2E','2I'),79:('1A','3-CEFHI'),80:('1L','3-EHIJK'),81:('1D','3-BEFIJ'),82:('1G','3-AEHIJ'),
    83:('2K','2L'),84:('1H','2J'),85:('1B','3-EFGIJ'),86:('1J','2H'),87:('1K','3-DEIJL'),88:('2D','2G'),
    89:('W74','W77'),90:('W73','W75'),91:('W76','W78'),92:('W79','W80'),
    93:('W83','W84'),94:('W81','W82'),95:('W86','W88'),96:('W85','W87'),
    97:('W89','W90'),98:('W93','W94'),99:('W91','W92'),100:('W95','W96'),
    101:('W97','W98'),102:('W99','W100'),103:('L101','L102'),104:('W101','W102'),
}

def main():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb['Recursos']
    def cell(r, c): return ws.cell(r, c).value

    # matchday por pareja (dentro del grupo) desde fixture_grupos.csv
    pair2md = {}
    with open(os.path.join(HERE, 'data/fixture_grupos.csv'), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            key = (row['grupo'], frozenset((row['local'], row['visita'])))
            pair2md[key] = row['matchday']

    out = []
    for r in range(2, 106):  # filas 2..105 = partidos 1..104
        num = cell(r, 6)
        if num is None:
            continue
        num = int(num)
        fecha = cell(r, 8)
        hora = cell(r, 9)
        grupo_raw = (cell(r, 12) or '').strip()
        sede = (cell(r, 13) or '').strip()
        fecha_iso = fecha.date().isoformat() if fecha else ''
        hora_txt = hora.strftime('%H:%M') if hora else ''

        if grupo_raw.startswith('Grupo '):
            g = grupo_raw.replace('Grupo ', '').strip()
            e1 = NAME2CODE[str(cell(r, 10)).strip()]
            e2 = NAME2CODE[str(cell(r, 11)).strip()]
            md = pair2md.get((g, frozenset((e1, e2))), '')
            out.append([num, 'grupos', g, md, fecha_iso, hora_txt, sede, e1, e2])
        else:
            fase = FASE.get(grupo_raw, grupo_raw)
            sl, sv = KO_SLOTS[num]
            out.append([num, fase, '', '', fecha_iso, hora_txt, sede, sl, sv])

    out.sort(key=lambda x: x[0])
    with open(os.path.join(HERE, 'data/fixture.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['match_no', 'fase', 'grupo', 'matchday', 'fecha', 'hora_local', 'sede', 'local', 'visita'])
        w.writerows(out)

    # ---- verificaciones ----
    assert len(out) == 104, f'esperaba 104, hay {len(out)}'
    grp = [x for x in out if x[1] == 'grupos']
    ko = [x for x in out if x[1] != 'grupos']
    assert len(grp) == 72 and len(ko) == 32, f'grupos={len(grp)} ko={len(ko)}'
    # cross-check: las 72 parejas de grupo coinciden con fixture_grupos.csv
    fg = set()
    with open(os.path.join(HERE, 'data/fixture_grupos.csv'), encoding='utf-8') as f:
        for row in csv.DictReader(f):
            fg.add((row['grupo'], frozenset((row['local'], row['visita']))))
    tdat = {(x[2], frozenset((x[7], x[8]))) for x in grp}
    assert tdat == fg, 'las parejas de grupo NO coinciden entre tDatos y fixture_grupos'
    # todos los partidos de grupo tienen matchday asignado
    assert all(x[3] in ('1', '2', '3') for x in grp), 'hay grupos sin matchday'
    # todas las fechas presentes
    sin_fecha = [x[0] for x in out if not x[4]]
    print(f'fixture.csv: {len(out)} partidos ({len(grp)} grupos + {len(ko)} KO)')
    print('cross-check parejas de grupo vs fixture_grupos: OK')
    print('matchday asignado a los 72 de grupo: OK')
    if sin_fecha:
        print('⚠️ partidos sin fecha:', sin_fecha)
    else:
        print('fechas presentes en los 104: OK')
    # rango de fechas
    fechas = sorted({x[4] for x in out if x[4]})
    print(f'rango de fechas: {fechas[0]} → {fechas[-1]}')

if __name__ == '__main__':
    main()
