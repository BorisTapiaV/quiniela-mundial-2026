#!/usr/bin/env python
"""Diagnóstico temporal: imprime el objeto 'score' de los partidos KO terminados,
para confirmar qué campos trae el tier (fullTime, penalties, duration). Borrar tras usar."""
import os, sys, json, urllib.request

COMP = 'WC'
API = f'https://api.football-data.org/v4/competitions/{COMP}/matches'

token = os.environ.get('FOOTBALL_DATA_TOKEN')
if not token:
    print('✗ Falta FOOTBALL_DATA_TOKEN'); sys.exit(1)
req = urllib.request.Request(API, headers={'X-Auth-Token': token})
data = json.load(urllib.request.urlopen(req, timeout=25))
matches = data.get('matches', [])
ko = [m for m in matches if m.get('stage') not in ('GROUP_STAGE', None) and m.get('status') == 'FINISHED']
print(f'KO terminados: {len(ko)}')
for m in ko[:4]:
    ht = (m.get('homeTeam') or {}).get('shortName') or (m.get('homeTeam') or {}).get('name')
    at = (m.get('awayTeam') or {}).get('shortName') or (m.get('awayTeam') or {}).get('name')
    print(f'\n=== {ht} vs {at} · stage={m.get("stage")} ===')
    print(json.dumps(m.get('score', {}), indent=2, ensure_ascii=False))
    print('minute/last:', m.get('minute'), m.get('lastUpdated'))
