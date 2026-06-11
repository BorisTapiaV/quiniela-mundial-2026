#!/usr/bin/env python
"""Auto-fetch de resultados del Mundial desde football-data.org (tier GRATIS).

Lee los partidos TERMINADOS de la API y los vuelca a:
  data/resultados.csv      (fase de grupos: actualiza gl/gv en su sitio)
  data/resultados_ko.csv   (eliminatorias: ganador por llave, penales incluidos)

El mapeo equipo-API -> nuestro código FIFA se hace por TLA -> nombre EN -> nombre ES
(normalizado sin acentos). Cualquier equipo que NO se logre mapear se reporta
ruidosamente y se OMITE (nunca se escribe un resultado dudoso).

Requiere la variable de entorno FOOTBALL_DATA_TOKEN.

Uso:
  FOOTBALL_DATA_TOKEN=xxxx python build/fetch_resultados.py          # escribe los CSV
  FOOTBALL_DATA_TOKEN=xxxx python build/fetch_resultados.py --dry    # solo muestra, no escribe
"""
import csv, os, sys, json, unicodedata, urllib.request, urllib.error

BUILD = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(BUILD)
DATA = os.path.join(HERE, 'data')
sys.path.insert(0, BUILD)
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
import engine

COMP = 'WC'                                   # código competición = FIFA World Cup
API = f'https://api.football-data.org/v4/competitions/{COMP}/matches'
DRY = '--dry' in sys.argv


def norm(s):
    """minúsculas, sin acentos, solo alfanumérico — para casar nombres robustamente."""
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return ''.join(ch for ch in s.lower() if ch.isalnum())


def fetch_matches(token):
    req = urllib.request.Request(API, headers={'X-Auth-Token': token})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r).get('matches', [])
    except urllib.error.HTTPError as e:
        print(f'✗ HTTP {e.code} de la API: {e.read().decode()[:200]}')
        sys.exit(1)
    except Exception as e:
        print(f'✗ Error llamando la API: {e}')
        sys.exit(1)


# Aliases API football-data.org (normalizado) -> nuestro código FIFA.
# football-data.org usa TLAs alineados a FIFA salvo excepciones puntuales.
ALIAS = {
    'cur': 'CUW',          # Curaçao: la API usa tla CUR; FIFA/nosotros CUW
    'curacao': 'CUW',
}


def build_crosswalk(eq):
    """dict normalizado -> código FIFA nuestro. Llaves: código, nombre_es, nombre_en, aliases."""
    x = {}
    for code, t in eq.items():
        x[norm(code)] = code
        for k in ('nombre_es', 'nombre_en'):
            if t.get(k):
                x[norm(t[k])] = code
    x.update(ALIAS)        # los aliases ganan/complementan
    return x


def api_code(team, xwalk):
    """Resuelve el equipo de la API a nuestro código probando tla, shortName, name."""
    for key in ('tla', 'shortName', 'name'):
        v = team.get(key)
        if v and norm(v) in xwalk:
            return xwalk[norm(v)]
    return None


KO_STAGES = {'LAST_32', 'LAST_16', 'QUARTER_FINALS', 'SEMI_FINALS', 'THIRD_PLACE', 'FINAL'}


def read_resultados_rows():
    p = os.path.join(DATA, 'resultados.csv')
    with open(p, encoding='utf-8') as f:
        rd = csv.DictReader(f)
        return rd.fieldnames, list(rd)


def main():
    token = os.environ.get('FOOTBALL_DATA_TOKEN')
    if not token:
        print('✗ Falta FOOTBALL_DATA_TOKEN en el entorno.')
        sys.exit(1)

    eq = engine.load_equipos(); fixture = engine.load_fixture(); terceros = engine.load_terceros()
    NM = {c: eq[c]['nombre_es'] for c in eq}
    xwalk = build_crosswalk(eq)

    # par de códigos (frozenset) -> match_no, solo fase de grupos
    pair2mn = {}
    for m in fixture:
        if m['fase'] == 'grupos':
            pair2mn[frozenset((m['local'], m['visita']))] = m['match_no']

    matches = fetch_matches(token)
    finished = [m for m in matches if m.get('status') == 'FINISHED']
    print(f'API: {len(matches)} partidos · {len(finished)} terminados')

    unmapped = set()
    grupo_res = {}     # match_no -> (gl, gv)
    ko_finished = []   # (utcDate, {a,b}, winner_code)  -> se resuelven al final por bracket

    for m in finished:
        ht, at = m.get('homeTeam', {}), m.get('awayTeam', {})
        ca, cb = api_code(ht, xwalk), api_code(at, xwalk)
        if not ca or not cb:
            if not ca:
                unmapped.add(ht.get('name') or ht.get('tla') or '??')
            if not cb:
                unmapped.add(at.get('name') or at.get('tla') or '??')
            continue
        sc = m.get('score', {}).get('fullTime', {})
        gl, gv = sc.get('home'), sc.get('away')
        stage = m.get('stage')
        if stage == 'GROUP_STAGE':
            if gl is None or gv is None:
                continue                      # FINISHED pero el marcador aún no está publicado (delay del tier gratis)
            mn = pair2mn.get(frozenset((ca, cb)))
            if mn is None:
                print(f'  ⚠ par de grupo no encontrado en fixture: {NM.get(ca,ca)} vs {NM.get(cb,cb)}')
                continue
            # orientar gl/gv a nuestro local/visita
            fx = next(f for f in fixture if f['match_no'] == mn)
            if (ca, cb) == (fx['local'], fx['visita']):
                grupo_res[mn] = (gl, gv)
            else:
                grupo_res[mn] = (gv, gl)
        elif stage in KO_STAGES:
            w = m.get('score', {}).get('winner')        # HOME_TEAM / AWAY_TEAM (incluye penales en fullTime+penalties)
            wc = ca if w == 'HOME_TEAM' else (cb if w == 'AWAY_TEAM' else None)
            ko_finished.append((m.get('utcDate', ''), {ca, cb}, wc))

    # ---- escribir grupos ----
    fields, rows = read_resultados_rows()
    nwritten = 0
    for row in rows:
        mn = int(row['match_no'])
        if mn in grupo_res:
            gl, gv = grupo_res[mn]
            if str(row.get('gl', '')) != str(gl) or str(row.get('gv', '')) != str(gv):
                row['gl'], row['gv'] = gl, gv
                nwritten += 1
    rg_now = {int(r['match_no']): (int(r['gl']), int(r['gv']))
              for r in rows if r.get('gl') not in (None, '') and r.get('gv') not in (None, '')}

    # ---- resolver KO contra el bracket real (iterativo: cada llave resuelta destraba la siguiente) ----
    ko_out = {}
    if len(rg_now) >= 72 and ko_finished:
        rk = {}
        progressed = True
        while progressed:
            progressed = False
            view = engine.full_bracket(rg_now, rk, eq, fixture, terceros)
            slot = {frozenset(t): mn for mn, t in view['teams'].items() if all(t)}
            for utc, pair, wc in ko_finished:
                mn = slot.get(frozenset(pair))
                if mn and mn not in rk and wc:
                    rk[mn] = wc
                    progressed = True
        ko_out = rk

    # ---- reportes ----
    print(f'Grupos: {len(grupo_res)} terminados mapeados · {nwritten} celdas a actualizar')
    print(f'KO: {len(ko_finished)} terminados · {len(ko_out)} mapeados al bracket'
          + ('' if len(rg_now) >= 72 else ' (grupos incompletos → KO se mapea cuando terminen)'))
    if unmapped:
        print('  ⚠ EQUIPOS NO MAPEADOS (revisar crosswalk): ' + ', '.join(sorted(unmapped)))

    if DRY:
        print('\n[--dry] no se escribió nada. Muestra de grupos:')
        for mn in sorted(grupo_res)[:8]:
            fx = next(f for f in fixture if f['match_no'] == mn)
            print(f'  M{mn}: {NM.get(fx["local"])} {grupo_res[mn][0]}-{grupo_res[mn][1]} {NM.get(fx["visita"])}')
        return

    wrote = False
    # Grupos: reescribir SOLO si cambió algún marcador real (evita churn por line-endings → commit/deploy espurio).
    if nwritten > 0:
        with open(os.path.join(DATA, 'resultados.csv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader(); w.writerows(rows)
        wrote = True

    # KO: reescribir SOLO si el set de ganadores difiere del archivo existente.
    ko_path = os.path.join(DATA, 'resultados_ko.csv')
    existing_ko = {}
    if os.path.exists(ko_path):
        for r in csv.DictReader(open(ko_path, encoding='utf-8')):
            if r.get('ganador'):
                existing_ko[int(r['match_no'])] = r['ganador'].strip().upper()
    if ko_out and ko_out != existing_ko:
        with open(ko_path, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f); w.writerow(['match_no', 'ganador'])
            for mn in sorted(ko_out):
                w.writerow([mn, ko_out[mn]])
        wrote = True

    if wrote:
        print('\n✓ Escrito (cambios reales). Corre: python build/actualizar.py')
    else:
        print('\n= Sin cambios reales — no se reescribió nada (no dispara commit/deploy).')


if __name__ == '__main__':
    main()
