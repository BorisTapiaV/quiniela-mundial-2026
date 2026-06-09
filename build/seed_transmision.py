#!/usr/bin/env python
"""Genera data/transmision.csv (match_no,abierta) — qué partidos van por TV ABIERTA.

Contexto Chile (jun-2026, verificado): los 104 partidos van por DSports/DirecTV (cable)
y Paramount+ (streaming). El diferenciador útil es cuáles son GRATIS por TV abierta
(Chilevisión, 52 partidos). Esta tabla marca `abierta=1` en los confirmados.

Lista confirmada (fuente: Cooperativa, guía de TV fase de grupos, 08-jun-2026) —
PARCIAL (hasta 18/6 en esa nota). Completar a medida que Chilevisión publique su grilla:
editar CHV_ABIERTA abajo o el CSV a mano (abierta=1).

Uso: python build/seed_transmision.py
"""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, 'data')

# partidos confirmados por TV abierta (Chilevisión): (fecha MM-DD, nombre local, nombre visita)
CHV_ABIERTA = [
    ('06-11', 'Mexico', 'Sudafrica'),
    ('06-12', 'Canada', 'Bosnia y Herzegovina'),
    ('06-12', 'Estados Unidos', 'Paraguay'),
    ('06-13', 'Catar', 'Suiza'),
    ('06-13', 'Brasil', 'Marruecos'),
    ('06-14', 'Paises Bajos', 'Japon'),
    ('06-15', 'Belgica', 'Egipto'),
    ('06-15', 'Arabia Saudita', 'Uruguay'),
    ('06-16', 'Francia', 'Senegal'),
    ('06-16', 'Argentina', 'Argelia'),
    ('06-17', 'Inglaterra', 'Croacia'),
    ('06-17', 'Uzbekistan', 'Colombia'),
    ('06-18', 'Suiza', 'Bosnia y Herzegovina'),
    ('06-18', 'Canada', 'Catar'),
]


def main():
    eq = engine.load_equipos(); fixture = engine.load_fixture()
    # nombre (sin tildes/acentos, normalizado) -> code
    import unicodedata

    def norm(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()
    name2code = {norm(v['nombre_es']): c for c, v in eq.items()}
    # (fecha, local, visita) -> match_no
    key2mn = {}
    for m in fixture:
        if m['fase'] == 'grupos':
            key2mn[(m['fecha'][5:], m['local'], m['visita'])] = m['match_no']

    abierta = set()
    faltan = []
    for fch, ln, vn in CHV_ABIERTA:
        lc, vc = name2code.get(norm(ln)), name2code.get(norm(vn))
        mn = key2mn.get((fch, lc, vc)) or key2mn.get((fch, vc, lc))  # por si el orden difiere
        if mn:
            abierta.add(mn)
        else:
            faltan.append((fch, ln, vn))

    with open(os.path.join(DATA, 'transmision.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['match_no', 'abierta'])
        for m in fixture:
            w.writerow([m['match_no'], '1' if m['match_no'] in abierta else ''])

    print(f'✓ data/transmision.csv · {len(abierta)} partidos por TV abierta (Chilevisión) confirmados')
    if faltan:
        print('  ⚠ no mapeados (revisar nombres):', faltan)
    print('  Resto: por confirmar (todos siguen en DSports/DirecTV + Paramount+).')


if __name__ == '__main__':
    main()
