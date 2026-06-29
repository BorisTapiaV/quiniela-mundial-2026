#!/usr/bin/env python
"""Trae la tabla de goleadores del Mundial desde football-data.org → data/goleadores.csv.

Requiere FOOTBALL_DATA_TOKEN. Uso:
    FOOTBALL_DATA_TOKEN=xxx python build/fetch_goleadores.py          # escribe el csv
    FOOTBALL_DATA_TOKEN=xxx python build/fetch_goleadores.py --dry    # solo muestra

Si el tier gratis NO permite /scorers para el Mundial, el script lo dice claro
(HTTP 403/restricción) y no rompe nada — se cae al modo manual del csv.
"""
import os, sys, csv, json, urllib.request, urllib.error

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, 'data')
COMP = 'WC'
API = f'https://api.football-data.org/v4/competitions/{COMP}/scorers?limit=100'


def main():
    dry = '--dry' in sys.argv
    token = os.environ.get('FOOTBALL_DATA_TOKEN')
    if not token:
        print('✗ Falta FOOTBALL_DATA_TOKEN en el entorno.'); sys.exit(1)
    req = urllib.request.Request(API, headers={'X-Auth-Token': token})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=25))
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:400]
        print(f'✗ HTTP {e.code} de /scorers: {body}')
        print('→ El tier probablemente NO permite /scorers para el Mundial. Usar csv manual.')
        sys.exit(2)
    except Exception as e:
        print(f'✗ Error llamando /scorers: {e}'); sys.exit(3)

    scorers = data.get('scorers', [])
    print(f'✓ /scorers OK · {len(scorers)} goleadores devueltos')
    rows = []
    for s in scorers:
        name = (s.get('player') or {}).get('name', '?')
        goals = s.get('goals') or 0
        team = (s.get('team') or {}).get('name', '')
        rows.append((name, goals, team))
        print(f'  {goals:>2}  {name}  ({team})')

    if not dry and rows:
        out = os.path.join(DATA, 'goleadores.csv')
        with open(out, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f); w.writerow(['figura', 'goles', 'equipo'])
            for name, goals, team in rows:
                w.writerow([name, goals, team])
        print(f'✓ escrito data/goleadores.csv ({len(rows)} filas)')


if __name__ == '__main__':
    main()
