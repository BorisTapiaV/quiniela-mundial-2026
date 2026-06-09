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

## Plantilla de captura por jugador (Paso 7) ★

| Script | Salida | Qué hace |
|--------|--------|----------|
| `gen_plantilla.py` | `PLANTILLA_QUINIELA_EN_BLANCO.xlsx` | Genera la planilla **en blanco** que se reparte. Una sola hoja de trabajo (bracket-challenge): el jugador pone los 72 marcadores de grupo, el **cuadro se arma solo** (standings con desempates FIFA + 8 mejores terceros vía tabla 495 → R32), y elige ganadores KO en **desplegables dependientes** hasta el campeón. Hojas: Instrucciones · Grupos · Eliminatorias · Especiales (+ ocultas `_calc`/`_t495`/`_eq`). |
| `ingest_plantilla.py` | `data/predicciones/<slug>.csv` (+`_ko`+`_especiales`) | Ingiere una plantilla **llena** al formato propio (igual que MF/CASA). El **motor es autoritativo**: re-deriva el bracket desde los 72 marcadores y avisa si algún ganador KO elegido no está en su llave derivada. Uso: `python build/ingest_plantilla.py <archivo.xlsx> [slug]`. |

**Cómo el Excel replica el motor (clave compuesta).** El motor ordena cada bloque de empate en UNA pasada (pts → H2H pts/dif/goles entre equipos con mismos puntos globales → dif/goles global → seed). Eso se reproduce en Excel con una **clave numérica compuesta lexicográfica** por equipo (`_calc!K`), ordenada con `RANK`. Validado **== engine** en 48.000 órdenes de grupo y **0 desajustes de R32 en 3.000 torneos completos**; recálculo real del libro (lib `formulas`) con datos de MF = **R32 16/16** y cascada KO → campeón correcto. ⚠️ Magnitud importante: en la clave de terceros `gf*100` (no `*10`) para que `letterord (1..12)` no se solape.

> openpyxl **no recalcula** fórmulas. Por eso el puntaje real nunca depende del Excel: `ingest_plantilla.py` + `engine.py` son la fuente de verdad. El Excel solo guía al jugador. Tras editar `gen_plantilla.py`, conviene abrir el libro 1 vez en Excel para confirmar que las fórmulas vivas renderizan antes de repartir.

---

## Generadores del visor (salida a `site/`)

| Script | Salida | Qué renderiza |
|--------|--------|---------------|
| `gen_site.py` | `site/index.html` | bracket completo de **1** jugador + tablas de grupo + banderas |
| `gen_demo_site.py` | `site/index.html` | **demo 12 jugadores, torneo EN CURSO** (cutoff configurable): leaderboard parcial, carrera de 2 actos, próximos partidos, sub-campeonatos, supervivencia de campeones |
| `gen_calendar.py` | `site/calendario.html` | calendario mensual jun+jul, partidos con hora + banderas (grupos) / ronda (KO) |
| `gen_jugador.py` | `site/p/<slug>.html` (+`private/links-jugadores.md`) | **Página individual de confirmación por jugador** (pre-cierre): su cuadro + tablas de grupo + campeón/especiales + sello "✓ recibido" + aviso link privado. `noindex`. Un link **no listado** por jugador (cada uno ve solo lo suyo → sin copia antes del cierre). Excluye La Casa (`DENY`). Uso: `python build/gen_jugador.py [SLUG...]` (sin args = todos los ingeridos). |

| `gen_galeria.py` | `site/index.html` (portada) | **Galería pública + leaderboard** (post-cierre). Lee predicciones reales (excluye La Casa) + `data/resultados.csv`/`_ko`/`_especiales` (parciales) + `data/validados.csv` (quién validó; ausente=todos). Estado DINÁMICO (por comenzar/grupos/KO/cerrado), leaderboard con nombre → `p/<slug>.html` + su campeón + badge vivo/cayó/sellado, **panel de premios** (pozo validados, 50/30/20), galería grid, y secciones ricas (carrera/evolución/sub-campeonatos/supervivencia) SOLO con resultados. Modo `--demo` para previsualizar. Reusa helpers de `gen_demo_site` vía import. |

| `gen_tarjeta.py` | `tarjetas/tarjeta-dia.png` | **Tarjeta diaria compartible a WhatsApp** (recap de LIGA COMPLETA — decisión deep-research: cubrir a los 12, no individual). Junta las mecánicas validadas: 🏆 puntero · 👑 rey de la jornada (Kicktipp) · 📈/📉 delta de posiciones (Kicktipp) · 💀 campeones caídos · mini-tabla top5+último · link al sitio. HTML→PNG vía Edge headless. **Opción A ($0):** el organizador manda el PNG al grupo manualmente. Modo `--demo` / real (predicciones + resultados + snapshot previo opcional `data/historico/`). |

> **WhatsApp (sin backend, $0):** **(A)** `gen_tarjeta.py` genera el PNG, Boris lo manda al grupo a mano (~30 s/día, va con la carga de resultados). **(B)** `gen_galeria.py` pone botón **"📲 Compartir al grupo"** (`wa.me` con texto+link) + meta tags Open Graph + `site/og.png` para el preview del link. NO hay forma oficial de auto-postear imágenes a un grupo desde un sitio estático; los bots (whatsapp-web.js) requieren server + riesgo de baneo → descartados para un pool familiar.

> **Visibilidad por tiempo (Boris 2026-06-09):** ANTES del cierre (11-jun) cada jugador ve solo SU `site/p/<slug>.html` (link privado, no enlazado desde el sitio público). DESPUÉS del cierre se abre la galería pública de todos + leaderboard (`gen_galeria.py` → `index.html`). El visor de resultados en vivo se completa con `data/resultados.csv` a medida que avanza el torneo.
>
> **Nombres con tilde:** `data/equipos.csv` (`nombre_es`) trae los acentos (España, México, Bélgica…). Los nombres de jugador con tilde se preservan en `<slug>_especiales.csv` fila `jugador` (el slug es ASCII para la URL); `gen_jugador`/`gen_galeria` usan ese nombre real.

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

## Torneo en vivo — base de resultados + snapshots (Paso 8)

| Script | Qué hace |
|--------|----------|
| `seed_resultados.py` | Crea las plantillas EN BLANCO `data/resultados.csv` (72 grupos: gl/gv) + `resultados_ko.csv` (32 KO: ganador) + `resultados_especiales.csv`. NO sobrescribe si ya tienen datos (`--force` para regenerar). |
| `snapshot.py` | Snapshots por jornada en `data/historico/<NN>_<label>.csv` (slug,total,pos) + cálculo del **delta ▲▼** (posición vs el último snapshot). Lo consumen `gen_galeria` (columna ±) y `gen_tarjeta` (tiles + columna). |
| `actualizar.py` ★ | **Orquestador.** `python build/actualizar.py` regenera páginas + portada + tarjeta (delta vs último cierre). `--cierre "MD1"` además **guarda un snapshot** (punto de comparación de la próxima vez). Cuando los grupos están completos, imprime los cruces reales del R32 para llenar el KO. |

**Flujo diario de Boris:**
1. Llenar lo jugado en `data/resultados.csv` (gl/gv) y `data/resultados_ko.csv` (ganador = código).
2. `python build/actualizar.py` → regenera todo con el delta del día.
3. Mandar `tarjetas/tarjeta-dia.png` al grupo de WhatsApp.
4. Al cerrar la jornada/día: `python build/actualizar.py --cierre "MD2 grupos"` (guarda snapshot).
5. `netlify deploy --dir=site --prod --site <id>` para publicar.

> **Fix motor (2026-06-09):** `score_player` ahora gatea el avance R32 a "grupos completos" (`len(real_group)>=72`). Antes contaba ~32 equipos "clasificados" aun con grupos sin jugar → puntajes fantasma pre-torneo. Ahora pre-torneo = 0. Selftest sin regresión (los grupos completos siguen contando R32).

### Pendiente
- ✅ Plantilla (`gen_plantilla.py`) + ingesta (`ingest_plantilla.py`) + páginas + galería + tarjeta + base de resultados/snapshots.
- Resto del plan de enganche: sub-competencia de consolación (#4), ganchos nominales/apodos (#5).
