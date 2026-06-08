# Arquitectura — Quiniela Mundial 2026

> ⚠️ **ARQUITECTURA FINAL 2026-06-07:** **visor HTML estático de solo lectura** en Netlify (NO app, NO Excel-relay). Recorrido de decisión: Excel→Sheets → (descartado app web por mantención) → **visor HTML estático**, que es el patrón del álbum. Principio rector: **minimizar mantención**, debe correr solo las ~5 semanas.
>
> **Pipeline real:**
> ```
> 1. Generador emite UNA plantilla Excel en blanco          → Boris la comparte
> 2. Cada participante la llena y la envía
> 3. Se cargan sus pronósticos → data/predicciones/<slug>.csv (o SQLite)
> 4. Se cargan resultados de partidos → data/resultados.csv  (manual o vía API)
> 5. gen_quiniela.py lee datos + puntaje + tabla 495 → emite HTML/CSS + gráficas
> 6. Deploy a Netlify (solo lectura). Regenerar al entrar resultados.
> ```
> - **Entrada = Excel** (lo que mandan). **Salida = HTML** (para mirar). "Wrapper de Excel".
> - **SQLite opcional**: capa de consulta de solo lectura para estadísticas (1X2 vs exacto, rachas…).
> - **Imágenes oficiales** (banderas/escudos) como assets estáticos. **Datos en vivo** opcional vía JS cliente (research APIs en curso).
>
> Sigue vigente todo lo de abajo: source of truth como CSV en repo, modelo de datos, lógica de puntaje/desempates/tabla-495. Solo cambia el ENTREGABLE: HTML estático en vez de xlsx.

---

## (Referencia de lógica) — modelo de datos y puntaje. Aplica al visor HTML.

---

## Principio: source of truth ≠ entregable

```
  SOURCE OF TRUTH                GENERADOR              ENTREGABLE
  (markdown + CSV, git)   →   gen_quiniela.py   →    quiniela.xlsx   →  Google Sheets
                              (Python/openpyxl)        (regenerable)      (Boris sube)
```

- **El Excel NUNCA es la verdad.** Se regenera desde los archivos fuente. Si llega una corrección de un pronóstico o un resultado, se edita el CSV/MD y se regenera.
- Mismo patrón que el **álbum** (`registro_maestro.csv` + `gen_print.py` → HTML).

## Por qué markdown SoT y no editar el Excel

- **Versionable / diffeable** en git (se ve qué cambió y cuándo).
- **Regenerable y determinístico** (mismo input → mismo Excel).
- **Separa contenido de presentación**: las fórmulas/colores/paneles del Excel son lógica del generador, no datos que se ensucian a mano.
- **Auditable**: timestamp de cada predicción ingresada.

## División markdown vs CSV

| Tipo de dato | Formato | Por qué |
|--------------|---------|---------|
| Reglas, config de puntaje, docs, decisiones | **Markdown** | Human-facing, prosa + tablas chicas |
| Equipos (48), grupos sembrados | **CSV** | Estructurado, lo consume el generador |
| Fixture (104 partidos: fecha/sede/grupo) | **CSV** | Matriz, derivable del reglamento + draw |
| Resultados reales (se van llenando) | **CSV** | Una fila por partido |
| Predicciones por participante | **CSV** (uno por persona o matriz) | 72+ filas × N jugadores; markdown sería inmanejable |
| Tabla de 495 combinaciones de terceros | **CSV** | Lookup oficial FIFA (Annexe C) |

## Modelo de datos (borrador)

- `data/equipos.csv` — `codigo, equipo, grupo, seed, bandera`
- `data/fixture.csv` — `match_id, fase, grupo, fecha, hora, sede, equipo_local, equipo_visita`
- `data/resultados.csv` — `match_id, goles_local, goles_visita, penales_local, penales_visita, estado`
- `data/predicciones/<slug>.csv` — `match_id, goles_local, goles_visita` (+ pronósticos especiales)
- `data/terceros_495.csv` — `clave, grupos_8, slot_1..slot_8` (mapeo FIFA)
- `config/puntaje.md` — reglas de puntaje (editable)
- `config/participantes.csv` — `slug, nombre, fecha_alta`

## Qué hace el generador (gen_quiniela.py) — esbozo

1. Lee equipos + fixture + resultados + todas las predicciones + config de puntaje.
2. Calcula tablas de posiciones (con desempates FIFA), 8 mejores terceros (lookup 495), bracket.
3. Calcula puntaje de cada participante por partido y total.
4. Emite `quiniela.xlsx` con:
   - Pestaña **Panel** (comparación de todos + leaderboard).
   - Pestaña **Resultados** (partidos jugados + histórico).
   - Una pestaña **por participante**.
   - Pestaña **Estadísticas** (1X2 vs marcador exacto, rachas, etc.).
   - Pestaña **Plantilla** en blanco para compartir.
5. Compatibilidad Google Sheets: **calcular en Python y escribir valores** donde una fórmula 365 no sea portable; usar solo fórmulas básicas (`SUM`, `COUNTIF`, `RANK`, `INDEX/MATCH`, `VLOOKUP`) si se quieren vivas en Sheets.

## Plantilla compartible (flujo RF-2/RF-3)

- El generador emite una **plantilla en blanco** (solo fixture + celdas de pronóstico).
- El participante la llena y la devuelve.
- Boris pasa los datos a Claude → se vuelca a `data/predicciones/<slug>.csv` → se regenera el Excel con su pestaña + panel actualizado.
- Alternativa a evaluar: que la plantilla sea un **Google Form** que escribe a una hoja (elimina el ida y vuelta de archivos). Decisión pendiente.

## Riesgos / cosas a cuidar

- **Fórmulas que no sobreviven la importación a Sheets** → preferir valores precalculados en Python.
- **Penales** en eliminatorias: campo dedicado, no sumar al marcador (error común de los modelos).
- **Candado por deadline**: como Boris relaya, es operativo; registrar timestamp de ingreso por auditoría.
- **Nombres/acentos** de equipos: usar `codigo` (POR, ARG…) como clave, nunca el nombre como join (los modelos sufren por esto).
