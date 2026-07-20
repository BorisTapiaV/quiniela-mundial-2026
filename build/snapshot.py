#!/usr/bin/env python
"""Snapshots por jornada + cálculo del delta de posiciones (▲▼).

Un snapshot = la tabla de posiciones en un momento (cierre de jornada):
  data/historico/<NN>_<label>.csv  con columnas slug,total,pos

El delta de cada jugador = posición en el snapshot anterior − posición actual
(positivo = subió). Es la mecánica validada por el deep research (Kicktipp,
aversión a la pérdida). `gen_galeria` y `gen_tarjeta` lo consumen vía `deltas()`.

Funciones públicas:
  load_players()                      -> [{slug,name,gs,ko,esp,champ}]
  compute_standings(players, rg, rk)  -> [{slug,name,total,exactos,pos,champ}] (ordenado)
  read_last()                         -> {slug: {'total':int,'pos':int}}  (último snapshot, o {})
  write_snapshot(standings, label)    -> path del snapshot escrito
  deltas(standings)                   -> {slug: {'rank_delta':int|None,'round_pts':int|None}}
  list_snapshots()                    -> [filenames ordenados]
"""
import csv, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = os.path.join(HERE, 'data', 'predicciones')
HIST = os.path.join(HERE, 'data', 'historico')
DENY = set()                        # La Casa (Boris Tapia V) pública. {'CASA'} para volver a ocultarla.


def _display_name(slug):
    return ' '.join(w.capitalize() for w in slug.replace('_', ' ').split())


def load_players():
    players = []
    if not os.path.isdir(PRED):
        return players
    for fn in sorted(os.listdir(PRED)):
        if not (fn.endswith('.csv') and not fn.endswith('_ko.csv') and not fn.endswith('_especiales.csv')):
            continue
        slug = fn[:-4]
        if slug in DENY:
            continue
        if not all(os.path.exists(os.path.join(PRED, f'{slug}{s}.csv')) for s in ('_ko', '_especiales')):
            continue
        gs, ko, esp = {}, {}, {}
        for r in csv.DictReader(open(os.path.join(PRED, f'{slug}.csv'), encoding='utf-8')):
            gs[int(r['match_no'])] = (int(r['gl']), int(r['gv']))
        for r in csv.DictReader(open(os.path.join(PRED, f'{slug}_ko.csv'), encoding='utf-8')):
            if r['ganador']:
                ko[int(r['match_no'])] = r['ganador']
        for r in csv.DictReader(open(os.path.join(PRED, f'{slug}_especiales.csv'), encoding='utf-8')):
            esp[r['clave']] = r['valor']
        players.append({'slug': slug, 'name': esp.get('jugador') or _display_name(slug),
                        'gs': gs, 'ko': ko, 'esp': esp})
    return players


def _load_real_especiales():
    """Especiales reales conocidos (goleador/…) desde data/resultados_especiales.csv.
    El campeón se deriva del bracket; el goleador es carga manual (Bota de Oro)."""
    re_ = {}
    p = os.path.join(HERE, 'data', 'resultados_especiales.csv')
    if os.path.exists(p):
        for r in csv.DictReader(open(p, encoding='utf-8')):
            if r.get('valor'):
                re_[r['clave']] = r['valor']
    return re_


def compute_standings(players, rg, rk, eq=None, fixture=None, terceros=None):
    eq = eq or engine.load_equipos(); fixture = fixture or engine.load_fixture()
    terceros = terceros or engine.load_terceros()
    rv = engine.full_bracket(rg, rk, eq, fixture, terceros)
    real_esp = _load_real_especiales()
    rows = []
    for p in players:
        sc = engine.score_player(p['gs'], p['ko'], rv, rg, p['esp'], real_esp, eq, fixture, terceros)
        exactos = sum(1 for mn, gv in rg.items() if p['gs'].get(mn) == gv)
        rows.append({'slug': p['slug'], 'name': p['name'], 'total': sc['total'],
                     'exactos': exactos, 'champ': sc['bracket']['champion']})
    rows.sort(key=lambda r: (-r['total'], -r['exactos'], r['slug']))
    for i, r in enumerate(rows, 1):
        r['pos'] = i
    return rows


def list_snapshots():
    if not os.path.isdir(HIST):
        return []
    return sorted(f for f in os.listdir(HIST) if re.match(r'^\d{2}_.*\.csv$', f))


def read_last():
    snaps = list_snapshots()
    if not snaps:
        return {}
    out = {}
    for r in csv.DictReader(open(os.path.join(HIST, snaps[-1]), encoding='utf-8')):
        out[r['slug']] = {'total': int(r['total']), 'pos': int(r['pos'])}
    return out


def deltas(standings):
    prev = read_last()
    out = {}
    for r in standings:
        pe = prev.get(r['slug'])
        out[r['slug']] = {
            'rank_delta': (pe['pos'] - r['pos']) if pe else None,
            'round_pts': (r['total'] - pe['total']) if pe else None,
        }
    return out


def write_snapshot(standings, label):
    os.makedirs(HIST, exist_ok=True)
    n = len(list_snapshots()) + 1
    safe = re.sub(r'[^A-Za-z0-9]+', '-', label.strip()).strip('-').lower() or 'jornada'
    path = os.path.join(HIST, f'{n:02d}_{safe}.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['slug', 'total', 'pos'])
        for r in standings:
            w.writerow([r['slug'], r['total'], r['pos']])
    return path


# CLI auxiliar
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        for s in list_snapshots():
            print(s)
    else:
        print('Snapshots en data/historico/:', len(list_snapshots()))
        for s in list_snapshots():
            print(' ', s)
