#!/usr/bin/env python
"""Crea las plantillas EN BLANCO de resultados reales (lo que Boris va llenando).

Genera (NO sobrescribe si ya tienen datos):
  data/resultados.csv             match_no,fecha,hora,sede,local,visita,gl,gv   (72 grupos)
  data/resultados_ko.csv          match_no,fase,fecha,ganador                   (32 KO)
  data/resultados_especiales.csv  clave,valor                                   (4)

Boris llena gl/gv (grupos) y ganador (KO, código de equipo) a medida que se juegan.
Las columnas extra (fecha/sede/local/visita) son referencia visual; los generadores
solo leen match_no + gl/gv (grupos) y match_no + ganador (KO).

Uso: python build/seed_resultados.py [--force]
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
FORCE = '--force' in sys.argv


def has_data(path, value_cols):
    """True si el archivo existe y tiene al menos una fila con valor en value_cols."""
    if not os.path.exists(path):
        return False
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if any(r.get(c) for c in value_cols):
                return True
    return False


def main():
    eq = engine.load_equipos(); fixture = engine.load_fixture()
    NM = {c: eq[c]['nombre_es'] for c in eq}
    os.makedirs(os.path.join(DATA, 'historico'), exist_ok=True)

    # ---- resultados.csv (grupos) ----
    p = os.path.join(DATA, 'resultados.csv')
    if has_data(p, ('gl', 'gv')) and not FORCE:
        print(f'⏭  {p} ya tiene resultados — no se toca (usa --force para regenerar en blanco)')
    else:
        with open(p, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['match_no', 'fecha', 'hora', 'sede', 'local', 'visita', 'gl', 'gv'])
            for m in fixture:
                if m['fase'] == 'grupos':
                    w.writerow([m['match_no'], m['fecha'], m['hora_chile'], m['sede'],
                                NM[m['local']], NM[m['visita']], '', ''])
        print(f'✓ {p} (72 grupos en blanco)')

    # ---- resultados_ko.csv ----
    p = os.path.join(DATA, 'resultados_ko.csv')
    if has_data(p, ('ganador',)) and not FORCE:
        print(f'⏭  {p} ya tiene resultados — no se toca')
    else:
        with open(p, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['match_no', 'fase', 'fecha', 'ganador'])
            for m in fixture:
                if m['fase'] != 'grupos':
                    w.writerow([m['match_no'], m['fase'], m['fecha'], ''])
        print(f'✓ {p} (32 llaves KO en blanco — ganador = código de equipo)')

    # ---- resultados_especiales.csv ----
    p = os.path.join(DATA, 'resultados_especiales.csv')
    if has_data(p, ('valor',)) and not FORCE:
        print(f'⏭  {p} ya tiene datos — no se toca')
    else:
        with open(p, 'w', newline='', encoding='utf-8') as f:
            w = csv.writer(f); w.writerow(['clave', 'valor'])
            for k in ('campeon', 'goleador', 'primer_eliminado', 'sorpresa'):
                w.writerow([k, ''])
        print(f'✓ {p} (especiales en blanco)')

    print('\nLlena gl/gv (grupos) y ganador (KO) a medida que se juega.')
    print('Cuando los 72 grupos estén listos, `actualizar.py` puede anotar los equipos reales del KO.')


if __name__ == '__main__':
    main()
