#!/usr/bin/env python3
"""Refresca las secciones MECÁNICAS de CURRENT.md desde los datos reales.

Reescribe SOLO dos bloques, delimitados por marcadores HTML en CURRENT.md:
  <!-- AUTO:TABLA inicio --> ... <!-- AUTO:TABLA fin -->         (tabla de posiciones)
  <!-- AUTO:RESULTADOS inicio --> ... <!-- AUTO:RESULTADOS fin --> (resultados cargados)

Todo lo demás (cabecera narrativa, "Estado", "Mano a mano", pendientes, footer)
NO se toca — eso se escribe a mano. Así la tabla nunca queda mal (p. ej. que Boris
no aparezca) ni desactualizada respecto al cron.

Uso:
    python build/refresh_dashboard.py            # reescribe CURRENT.md
    python build/refresh_dashboard.py --check     # solo imprime, no escribe (dry-run)

Robusto: si faltan los marcadores, aborta con instrucciones y no toca el archivo.
"""
import os
import sys
import csv

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'build'))
import engine        # noqa: E402
import snapshot      # noqa: E402
import gen_jugador   # noqa: E402

CURRENT = os.path.join(HERE, 'CURRENT.md')
RECIENTES = 24       # cuántos partidos van en la tabla; el resto va condensado
MEDALLAS = {1: '🥇', 2: '🥈', 3: '🥉'}


def _fecha_corta(iso):
    """'2026-06-25' -> '25-jun'."""
    meses = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
             'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
    try:
        _, m, d = iso.split('-')
        return f'{int(d)}-{meses[int(m) - 1]}'
    except (ValueError, IndexError):
        return iso


def bloque_tabla(eq):
    rg, rk = gen_jugador._load_results()
    st = snapshot.compute_standings(snapshot.load_players(), rg, rk)
    n = len(rg)
    out = [f'## 🏆 Tabla de posiciones (tras {n} partidos)', '',
           '| Pos | Jugador | Campeón | Pts | Exactos | Vivo |',
           '|:---:|---------|---------|:---:|:---:|:---:|']
    for r in st:
        pos = MEDALLAS.get(r['pos'], str(r['pos']))
        champ = eq.get(r['champ'], {}).get('nombre_es', r['champ'])
        # negrita para el mano a mano de arriba (top 2)
        nombre = f'**{r["name"]}**' if r['pos'] <= 2 else r['name']
        pts = f'**{r["total"]}**' if r['pos'] <= 2 else str(r['total'])
        out.append(f'| {pos} | {nombre} | {champ} | {pts} | {r["exactos"]} | 🟢 |')
    return '\n'.join(out), n


def bloque_resultados(eq, fixture):
    fx = {m['match_no']: m for m in fixture}
    jugados = []
    with open(os.path.join(HERE, 'data', 'resultados.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r.get('gl') in (None, '') or r.get('gv') in (None, ''):
                continue
            mn = int(r['match_no'])
            m = fx.get(mn, {})
            jugados.append({
                'mn': mn,
                'local': m.get('local', r.get('local', '')),
                'visita': m.get('visita', r.get('visita', '')),
                'gl': int(r['gl']), 'gv': int(r['gv']),
                'fecha': m.get('fecha', r.get('fecha', '')),
            })
    jugados.sort(key=lambda x: x['mn'])
    n = len(jugados)
    rng = f'M{jugados[0]["mn"]}–M{jugados[-1]["mn"]}' if jugados else 'M0'

    def nombre(code):
        return eq.get(code, {}).get('nombre_es', code)

    recientes = jugados[-RECIENTES:][::-1]   # más nuevo primero
    viejos = jugados[:-RECIENTES] if n > RECIENTES else []

    out = [f'## 📊 Resultados cargados ({rng})', '',
           '| Match | Partido | Marcador | Fecha |',
           '|:-----:|---------|:--------:|------|']
    for j in recientes:
        out.append(f'| M{j["mn"]} | {nombre(j["local"])} – {nombre(j["visita"])} '
                   f'| {j["gl"]}-{j["gv"]} | {_fecha_corta(j["fecha"])} |')

    if viejos:
        f0, f1 = _fecha_corta(viejos[0]['fecha']), _fecha_corta(viejos[-1]['fecha'])
        rng_v = f'M{viejos[0]["mn"]}–M{viejos[-1]["mn"]}'
        chips = ' · '.join(f'{j["local"]} {j["gl"]}-{j["gv"]} {j["visita"]}'
                           for j in viejos)
        out += ['', f'**{rng_v} ({f0}–{f1}):** {chips}.']
    return '\n'.join(out), n


def reemplazar(texto, tag, contenido):
    ini, fin = f'<!-- AUTO:{tag} inicio', f'<!-- AUTO:{tag} fin -->'
    i = texto.find(ini)
    j = texto.find(fin)
    if i == -1 or j == -1:
        raise SystemExit(
            f'ERROR: faltan los marcadores AUTO:{tag} en CURRENT.md.\n'
            f'  Añade alrededor del bloque:\n'
            f'    <!-- AUTO:{tag} inicio — generado por build/refresh_dashboard.py, no editar a mano -->\n'
            f'    ...contenido...\n'
            f'    <!-- AUTO:{tag} fin -->')
    i_eol = texto.find('\n', i) + 1           # tras la línea del marcador inicial
    return texto[:i_eol] + contenido + '\n' + texto[j:]


def main():
    check = '--check' in sys.argv
    eq = engine.load_equipos()
    fixture = engine.load_fixture()
    tabla, n_pts = bloque_tabla(eq)
    res, n_res = bloque_resultados(eq, fixture)

    with open(CURRENT, encoding='utf-8') as f:
        texto = f.read()
    texto = reemplazar(texto, 'TABLA', tabla)
    texto = reemplazar(texto, 'RESULTADOS', res)

    if check:
        print('— DRY RUN (no escribe) —\n')
        print(tabla, '\n')
        print(f'(resultados: {n_res} partidos; tabla a {n_pts} de grupo)')
        return
    with open(CURRENT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(texto)
    print(f'CURRENT.md refrescado: tabla ({n_pts} de grupo) + resultados ({n_res} partidos).')


if __name__ == '__main__':
    main()
