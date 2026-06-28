#!/usr/bin/env python
"""Orquestador: carga de resultados -> regenera todo -> (opcional) snapshot de jornada.

Flujo diario de Boris:
  1. Llena lo jugado en data/resultados.csv (gl/gv) y data/resultados_ko.csv (ganador).
  2. python build/actualizar.py                 -> regenera portada + páginas + tarjeta
                                                    (con delta ▲▼ vs el último cierre).
  3. python build/actualizar.py --cierre "MD1"  -> además guarda un SNAPSHOT de jornada
                                                    (de ahí sale el delta de la próxima vez).

El delta de cada vista = posición actual vs el ÚLTIMO snapshot. Por eso se hace
`--cierre` cuando termina una jornada/día: marca el punto de comparación siguiente.

Uso:
  python build/actualizar.py [--cierre "Etiqueta de la jornada"]
"""
import csv, os, sys, subprocess
BUILD = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(BUILD)
DATA = os.path.join(HERE, 'data')
sys.path.insert(0, BUILD)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine
import snapshot


def load_results():
    rg, rk = {}, {}
    p = os.path.join(DATA, 'resultados.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('gl') not in (None, '') and r.get('gv') not in (None, ''):
                rg[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
    p = os.path.join(DATA, 'resultados_ko.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('ganador'):
                rk[int(r['match_no'])] = r['ganador'].strip().upper()
    return rg, rk


def cierre_label():
    if '--cierre' in sys.argv:
        i = sys.argv.index('--cierre')
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
        print('⚠ --cierre necesita una etiqueta, ej: --cierre "MD1 grupos"'); sys.exit(1)
    return None


def main():
    label = cierre_label()
    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    NM = {c: eq[c]['nombre_es'] for c in eq}

    print('── Regenerando sitio + tarjeta ' + '─' * 30)
    for s in ('gen_jugador.py', 'gen_galeria.py', 'gen_calendar.py', 'gen_tarjeta.py'):
        print(f'\n▶ {s}')
        subprocess.run([sys.executable, os.path.join(BUILD, s)], check=False)

    rg, rk = load_results()
    print('\n── Estado de resultados ' + '─' * 38)
    print(f'  grupos jugados: {len(rg)}/72 · llaves KO resueltas: {len(rk)}/32')

    # cuando los grupos están completos, mostrar los cruces REALES del R32 para llenar el KO
    if len(rg) >= 72:
        r32 = engine.build_r32(engine.compute_all_standings(engine.group_results_by_group(rg, fixture), eq), fixture, terceros)
        pend = [(mn, a, b) for mn, (a, b) in sorted(r32.items()) if mn not in rk]
        if pend:
            print('\n  Cruces reales del R32 (llena el ganador en resultados_ko.csv):')
            for mn, a, b in pend:
                print(f'    M{mn}: {NM.get(a, a)} vs {NM.get(b, b)}')

    # snapshot de jornada
    if label:
        players = snapshot.load_players()
        if not players:
            print('\n⚠ No hay predicciones ingeridas — no se puede snapshotear todavía.')
        else:
            st = snapshot.compute_standings(players, rg, rk, eq, fixture, terceros)
            path = snapshot.write_snapshot(st, label)
            print(f'\n✓ Snapshot de jornada guardado: {os.path.relpath(path, HERE)}')
            print(f'  ({len(snapshot.list_snapshots())} snapshots · líder {st[0]["name"]} {st[0]["total"]} pts)')
            print('  El delta ▲▼ de la próxima actualización se medirá contra este punto.')
    else:
        n = len(snapshot.list_snapshots())
        print(f'\n  (sin --cierre: no se guardó snapshot · hay {n} previos · delta medido vs el último)')

    print('\n── Listo ' + '─' * 52)
    print('  Sitio: site/index.html  ·  Tarjeta: tarjetas/tarjeta-dia.png (mándala al grupo)')


if __name__ == '__main__':
    main()
