# build/ — generadores Python

Todos los scripts se corren desde la raíz `quiniela/` (resuelven rutas relativas a sí mismos). Requieren `openpyxl` para leer los Excel de bootstrap/ingesta; el resto es stdlib.

---

## El motor — `engine.py` ★

Corazón del sistema. Importado por todos los generadores. Funciones públicas:

| Función | Qué hace |
|---------|----------|
| `load_equipos/load_fixture/load_terceros` | cargan los CSV de `data/` |
| `compute_standings(teams, matches, seed)` | tabla de un grupo con desempates FIFA (pts → H2H → dif → goles → seed) |
| `compute_all_standings(results_by_group, eq)` | las 12 tablas |
| `group_results_by_group(group_scores, fixture)` | convierte `match_no→(gl,gv)` a `grupo→lista` |
| `rank_thirds(all_standings)` | los 8 mejores terceros (combo + 4 fuera) |
| `build_r32(all_standings, fixture, terceros)` | arma el R32 (16 cruces) vía la tabla 495 |
| `resolve_bracket(r32, ko_winners, fixture)` | cascada KO (W74→W89→…→M104) |
| `reaching_sets(r32, win)` | conjuntos de equipos que alcanzan cada ronda + campeón |
| `full_bracket(group_scores, ko_winners, eq, fixture, terceros)` | bracket completo (real o de un jugador) |
| `score_player(...)` | puntaje: `{grupo, avance, especiales, total, bracket}` — **soporta resultados parciales** |

Pesos configurables: `W_GROUP` (5/3/2), `W_ADV` (R32 2 / R16 4 / QF 6 / SF 10 / Final 16), `W_ESP` (campeón 50 / gol 25 / 1º elim 20 / sorpresa 15). Máx total **718** (50/35/15).

**Desempates:** modela pts → enfrentamiento directo → dif/goles globales → seed del sorteo. NO modela conducta (tarjetas) ni ranking FIFA (el jugador predice goles, no tarjetas) → el seed es el desempate final determinístico.

`python build/engine.py` corre los **autotests** (invariantes fase 1 + scoring fase 2).

---

## Bootstrap de datos (una vez; el CSV resultante es la verdad)

| Script | Genera | Fuente |
|--------|--------|--------|
| `bootstrap_fixture.py` | `data/fixture.csv` (104 partidos) | fechas/sedes de `Fixture-…ClasesExcel.xlsx` (`tDatos`) + cruces KO del reglamento |
| `bootstrap_terceros.py` | `data/terceros_495.csv` (495 combos) | hoja `AssignThird` de `WCup_2026_4.2.6_en.xlsx` ("FIFA 23.06.2025") |

`data/equipos.csv` y `data/fixture_grupos.csv` se generaron inline (ver historial); `equipos.csv` viene del ala álbum (verificado físicamente). ⚠️ Los Excel fuente viven en `~/Downloads/`.

---

## Ingesta — `ingest_mf.py`

Práctica de ingesta de una predicción **externa** (`MF_2026_Pronosticos.xlsm`, tracker latino) al formato propio:
- 72 marcadores de grupo (hoja `Calculos`) → `data/predicciones/MF.csv` (mapeo nombres→códigos + alineación local/visita contra el fixture).
- Ganadores KO (hojas de eliminatorias, penales resueltos) → `MF_ko.csv`.
- Campeón → `MF_especiales.csv`.
- Verifica reconstruyendo el bracket con el motor: **R32 16/16** vs el Excel + **0 inconsistencias**.

Patrón reutilizable para ingerir cualquier predicción externa: mapear → alinear → verificar con el motor.

---

## Generadores del visor (salida a `site/`)

| Script | Salida | Qué renderiza |
|--------|--------|---------------|
| `gen_site.py` | `site/index.html` | bracket completo de **1** jugador + tablas de grupo + banderas |
| `gen_demo_site.py` | `site/index.html` | **demo 12 jugadores, torneo EN CURSO** (cutoff configurable): leaderboard parcial, carrera de 2 actos, próximos partidos, sub-campeonatos, supervivencia de campeones |
| `gen_calendar.py` | `site/calendario.html` | calendario mensual jun+jul, partidos con hora + banderas (grupos) / ronda (KO) |

> `gen_demo_site.py` genera 12 predicciones (1 real MF + 11 sintéticas con accuracy variable) y un **resultado simulado** con corte configurable (variable `real_ko` filtrada por nº de partido). Cambiar el corte muestra cualquier momento del torneo (grupos → final). En producción, esto se reemplaza por `data/predicciones/*` reales + `data/resultados*.csv`.

**Render a PNG** (verificación visual, Edge headless):
```bash
EDGE="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
"$EDGE" --headless --disable-gpu --virtual-time-budget=9000 \
  --screenshot="$(cygpath -m "$PWD/site/x.png")" "file:///$(cygpath -m "$PWD/site/index.html")"
```
(El `--virtual-time-budget` da tiempo a que carguen las banderas de flagcdn por red.)

---

## Banderas (flagcdn)

`https://flagcdn.com/w40/{iso}.png` donde `{iso}` = columna `iso_bandera` de `equipos.csv` (`cl`, `mx`, `gb-sct`, `gb-eng`…). Dominio público, sin problema legal. **No** usar escudos/logos FIFA ni arte Panini en el sitio.

---

## Hacia producción (Paso 7)

1. Plantilla Excel en blanco → repartir → cada jugador llena → ingerir a `data/predicciones/<slug>.csv`.
2. Cargar `data/resultados.csv` (parcial, lo jugado) a medida que avanza el torneo.
3. Un `gen_site.py` de producción: lee todas las predicciones + resultados → motor → leaderboard en vivo + vistas.
4. Deploy de `site/` a Netlify (regenerar al entrar resultados).
