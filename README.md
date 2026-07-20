# Quiniela Mundial 2026 🎯

Quiniela/polla del Mundial FIFA 2026 (Canadá · México · EE.UU.) entre ~12 amigos/familia. Boris administra; el sistema genera un **visor HTML estático de solo lectura** (Netlify) a partir de datos versionados. Modelo "bracket challenge": cada jugador pronostica todo antes de empezar y la gracia es ver **la carrera** del torneo.

**Estado al 2026-06-07:** backend completo y validado. Falta la plantilla de captura + orquestación con resultados reales.

> 🏆 **Torneo 2026 CERRADO (2026-07-19):** España campeón, Boris ganó su propia quiniela (424 pts, +75). El experimento de pronóstico ("La Casa") acertó 11/12 grupos · 4/4 semis · 2/2 finalistas · campeón · goleador → `referencias/RETROSPECTIVA_EXPERIMENTO_PRONOSTICO_2026-07.md`.
> 🕐 **¿Volviste para el Mundial 2030?** Lee **`ARRANQUE_2030.md`** — es el único doc que necesitas (qué se reusa/cambia + método de pronóstico refinado + gotchas).

---

## 🧭 Decisiones clave (todas tomadas)

| Tema | Decisión |
|------|----------|
| **Plataforma** | Visor HTML estático de solo lectura → **Netlify**. NO app, NO editar Excel a mano. |
| **Source of truth** | CSV/markdown versionados en el repo → generadores Python → HTML. Mismo patrón que el ala álbum. |
| **Qué se predice** | 72 marcadores de grupo (escalonado) + bracket de eliminatorias (quién avanza, sin marcador) + especiales. **Una sola planilla, todo antes de empezar.** |
| **Bracket** | Auto-derivado de los 72 de cada jugador (posiciones + 8 terceros vía tabla 495); el jugador solo elige ganadores KO. |
| **Puntaje** | Escalonado (exacto 5 / dif 3 / 1X2 2) + avance KO (2/4/6/10/16) + especiales (campeón 50 / gol 25). **Máx 683 = 53% grupos / 36% KO / 11% especiales.** (primer eliminado y sorpresa retirados 28-jun, ambiguos.) |
| **Jugadores** | ~12. |
| **Imágenes** | Solo banderas (flagcdn, dominio público) + nombre. NO escudos/logos FIFA ni arte Panini (copyright). |

> Detalle y "por qué" de cada decisión en `config/reglas-puntaje.md`, `docs/` y `referencias/`.

---

## 📂 Estructura

```
quiniela/
├── README.md                      ← este archivo (entrada + estado)
├── data/                          source of truth (CSV) — ver data/README.md
│   ├── equipos.csv                48 equipos (código, grupo, pos, nombres, bandera ISO)
│   ├── fixture.csv                104 partidos (fecha/hora/sede + cruces)
│   ├── fixture_grupos.csv         72 de grupo (determinístico)
│   ├── terceros_495.csv           495 combinaciones de mejores terceros (Annexe C)
│   └── predicciones/              pronósticos por jugador
│       └── MF.csv / MF_ko.csv / MF_especiales.csv   (predicción real ingerida)
├── config/
│   └── reglas-puntaje.md          modelo de puntaje + la "carrera" + disyuntiva resuelta
├── docs/
│   ├── VISION_Y_REQUISITOS.md     RF-1…RF-9
│   ├── ARQUITECTURA.md            SoT → generadores → HTML + modelo de datos
│   ├── IDEAS_DEEP_RESEARCH.md     catálogo de features (deep research)
│   └── EXPERIENCIA_EN_VIVO_Y_WOW.md  ⭐ la dimensión en vivo + gráficas + efecto wow
├── referencias/
│   ├── analisis-3-modelos.md      análisis de 3 plantillas Excel de referencia
│   ├── balance-puntaje-disyuntiva.md  research volumen-vs-audacia (paradoja de Aldous)
│   └── datos-imagenes-apis.md     APIs de fútbol + banderas para sitio estático
├── reglas/                        reglamento FIFA modularizado (Art 11-14) + PDF fuente
│   └── INDEX.md
├── build/                         generadores Python — ver build/README.md
│   ├── engine.py                  ★ motor: posiciones+desempates · 8 terceros · R32 vía 495 · cascada KO · scoring · r32_partial/bracket_partial (resolución parcial del cuadro sin exigir los 72)
│   ├── bootstrap_fixture.py       genera fixture.csv (desde Excel + reglamento)
│   ├── bootstrap_terceros.py      genera terceros_495.csv (desde Excel FIFA)
│   ├── ingest_mf.py               ingesta de una predicción externa (.xlsm) → nuestro formato
│   ├── gen_site.py                visor: bracket de 1 jugador
│   ├── gen_demo_site.py           visor demo: 12 jugadores, torneo en curso (cutoff configurable)
│   ├── gen_calendar.py            calendario mensual (jun+jul) con partidos y horas
│   └── gen_recap.py               ★ recap diario para WhatsApp (grupos: marcador+ganador · KO: Avanza/Cae/— + cuadro-leyenda · goleadores + campeones, ambos con picks muertos 💀). NO deploya (vive en recap/)
└── site/                          salida estática (deploy a Netlify)
    ├── index.html                 leaderboard + carrera + evolución + cuadro real KO + sub-campeonatos + supervivencia + archivo grupos plegable + resultados por día
    └── calendario.html            calendario mensual (los KO muestran equipos en cuanto se resuelven)
```

---

## ⚙️ Pipeline

```
  DATOS (CSV, source of truth)              MOTOR              VISOR (estático)
  equipos · fixture · terceros_495   →   engine.py    →    site/*.html  →  Netlify
  predicciones/<jugador>.csv             (cálculo)         (banderas flagcdn)
  resultados.csv  (al jugar el torneo)
```

- **El motor (`engine.py`)** calcula, desde marcadores de grupo: tablas de posiciones (desempates FIFA), los 8 mejores terceros (tabla 495), el R32, la cascada KO y el puntaje. Sirve igual para los **resultados reales** que para el **bracket de cada jugador**, y **soporta resultados parciales** (puntúa "al día de hoy" → habilita los estados intermedios del torneo sin cambios).
- Los generadores `gen_*` leen datos + motor → emiten HTML estático.
- **Cuadro KO en vivo (2026-06-27):** `engine.r32_partial` resuelve los cruces de 16avos con lo disponible (1º/2º de grupos ya cerrados; placeholders `1ºJ`/`3º` para lo pendiente) y `engine.bracket_partial` extiende eso a todo el cuadro (R16→Final se llenan con los ganadores de `resultados_ko.csv`). El **calendario** y el **"🏆 Cuadro del torneo"** de la portada usan esto → se llenan **solos** a medida que cierran los grupos y avanzan las llaves, sin reventar como `build_r32` (que exige los 72). Al completarse los 72, la portada despliega el **archivo plegable "Fase de grupos — cerrada"** con las 12 tablas finales; la cronología completa vive en **"Resultados por día"**.

## 📸 Recap diario (pronósticos para WhatsApp)

Tarjeta HTML con los pronósticos de los 5 jugadores para los partidos de un día. **Vive en `recap/`, NO se deploya** (es para sacarle foto y mandarla al grupo) → no gasta cupo Netlify.

```bash
python build/gen_recap.py 2026-07-01          # tarjeta real de esa fecha
python build/gen_recap.py 2026-07-03 --prueba # marcada como PRUEBA
```
Salida: `recap/predicciones-<fecha>.html` (banderas embebidas en base64 → la foto nunca sale con banderas rotas).
> El `print` final puede lanzar `UnicodeEncodeError` en la consola Windows (cp1252 no codifica `✓`); es **cosmético** — el archivo se escribe completo antes de ese print.

### Qué muestra por partido

- **Fase de grupos:** el marcador que cada jugador puso + el ganador que implica (o "Empate").
- **Eliminatorias (KO):** el pick de cada jugador para ese cruce **real**, en 1 de 3 estados:

| Estado | Se ve | Significado | Cómo se calcula |
|--------|-------|-------------|-----------------|
| **Avanza** | equipo en **verde** + tag "Avanza" | el jugador lleva ese equipo a la ronda siguiente | **por conjunto** (`depth_of`): ¿alguno de los 2 equipos reales del cruce llega a la ronda siguiente en el bracket del jugador? Igual que el puntaje → puede "avanzar por otra llave" |
| **Cae** | equipo **tachado rojo** + tag "pierde" | tenía ese equipo en este mismo cruce y lo hizo perder | **por casillero** (`pb['teams'][mn]`): solo el equipo real que está en el MISMO casillero `mn` del jugador y que no eligió ganar |
| **—** | guion gris | no tiene a ninguno de los dos equipos del cruce en ese casillero | ninguno de los 2 equipos reales está en el casillero `mn` del jugador |

**Por qué la asimetría (conjunto para "Avanza", casillero para "Cae"):** el puntaje del motor es **por conjunto de equipos que avanzan** (no por casillero), así que "Avanza" debe reflejar eso — si el jugador lleva un equipo a la ronda siguiente y ese equipo pasa, suma, esté donde esté en su llave. En cambio "Cae" por conjunto mostraba equipos de **otras** llaves del jugador (caso real: a Jorge le salía "Bélgica Senegal" en el cruce Bélgica–Senegal porque tenía a Senegal cayendo en otro casillero) → confuso. Por casillero solo muestra el equipo real de **ese** cruce que el jugador eliminó ahí.

> **Anti-pattern documentado (no repetir):** antes el "Cae" usaba `depth_of` (por conjunto) y juntaba cualquier equipo real que apareciera en esa ronda del bracket, sin importar el casillero → mostraba 2 equipos sin sentido. La regla es: **"Avanza" por conjunto (calza con el puntaje), "Cae"/"—" por casillero (`mn`).**

**Cuadro-leyenda:** en fases KO el recap antepone automáticamente un cuadro "Cómo leer cada predicción" con los 3 estados (verde / tachado rojo / gris). Aparece solo en eliminatorias — mientras más se cierra el torneo y más se mezclan los estados, la leyenda siempre está.

### Picks muertos 💀 (goleadores + campeones)

Desde `PICKS_MUERTOS_DESDE = 2026-07-01` (`engine.py`), un pick que **ya no puede ganar** se apaga: gris + nombre tachado + 💀 + ✗. **NO toca el puntaje** (falla a "vivo" ante datos faltantes, no marca de más).

- **Goleador** (sección ⚽): su figura muere si la **selección quedó eliminada y ya es inalcanzable** (alguien tiene más goles). Helpers `teams_alive` / `load_scorers` / `goleador_dead`.
- **Campeón** (sección 🏆): una tarjeta por jugador con su campeón (bandera + país); muere en cuanto su selección sale del cuadro (`campeón ∈ set(equipos) − teams_alive(...)`). La sección solo aparece cuando algún jugador tiene campeón elegido. Se activó el 07-jul con **Portugal (Carlos)** como primer campeón caído.

El mismo criterio de campeón eliminado aplica en las páginas de jugador (`gen_jugador.py`, hero campeón).

## ▶️ Cómo correr (desde `quiniela/`)

```bash
python build/engine.py            # autotests del motor (fase 1 + 2)
python build/gen_demo_site.py     # regenera site/index.html (demo 12 jugadores)
python build/gen_calendar.py      # regenera site/calendario.html
# render opcional a PNG para revisar (Edge headless):
#   msedge --headless --screenshot=site/x.png --virtual-time-budget=9000 "file:///.../site/index.html"
```

---

## ✅ Estado por paso

| Paso | Estado |
|------|--------|
| 1 · Reglas FIFA modularizadas | ✅ `reglas/` |
| 1.5 · Análisis de 3 modelos Excel | ✅ `referencias/analisis-3-modelos.md` |
| 2 · Visión, arquitectura, ideas (deep research) | ✅ `docs/` |
| 3 · Data layer (equipos · fixture · tabla 495) | ✅ `data/` — verificado |
| 4 · Decisiones de puntaje + rebalanceo 50/35/15 | ✅ `config/reglas-puntaje.md` |
| 5 · Motor (posiciones · terceros · bracket · scoring) | ✅ `build/engine.py` — autotests OK |
| 5.5 · Ingesta probada (predicción real de MF) | ✅ `build/ingest_mf.py` — **16/16 R32 + 0 inconsistencias** |
| 6 · Visor base + demo 12 jugadores + demo intermedio + calendario | ✅ `site/` |

### Validaciones logradas
- **R32 16/16:** el motor reconstruye el mismo R32 que el Excel independiente de MF.
- **Bracket 0 inconsistencias:** reconstruye el bracket completo de MF (incl. penales).
- **Motor:** autotests de invariantes (sin choque de grupo en R32, jugador perfecto = máx 718, etc.).

## ⏳ Pendiente (Paso 7)

- **Plantilla en blanco** para repartir (lo que la gente llena: auto-bracket + listas desplegables dependientes). — *Boris: "después 2".*
- **`resultados.csv`** real + orquestación (predicciones + resultados parciales → motor → leaderboard) + **snapshots históricos por jornada** (para la evolución del ranking).
- **Experiencia en vivo + efecto wow** (`docs/EXPERIENCIA_EN_VIVO_Y_WOW.md`): marcador en vivo (minuto/eventos vía API), evolución del ranking fecha a fecha (line chart ⭐), head-to-head, racha, mapa de calor, animaciones, tarjeta compartible, narrativa de badges. Es el corazón del enganche durante el torneo.

---

*Parte del paraguas [`Mundial-2026/`](../README.md), hermana del ala `album/`. Última actualización: 2026-06-07.*
