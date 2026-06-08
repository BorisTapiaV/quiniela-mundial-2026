# Análisis de 3 modelos de quiniela Excel (referencia de diseño)

> Insumo del 2026-06-07. Tres plantillas Excel ya construidas, analizadas con agentes (openpyxl, fórmulas + valores + validaciones + nombres + formato condicional). Objetivo: robar las mejores mecánicas para nuestra quiniela. Archivos fuente en `C:\Users\boris\Downloads\`.

---

## Comparación rápida

| | **WCup 4.2.6** (Hermann Baum, DE) | **ADMIN-Excel** (M.Á. Tejero, comercial) | **Fixture ClasesExcel** |
|---|---|---|---|
| **Qué es** | Planner de Mundial + capa de quiniela | Quiniela comercial multi-jugador pulida | Solo fixture/cuadro auto-calculado (NO quiniela) |
| **Hojas** | 30 (muchas ocultas) | 14 (datos en `veryHidden`) | ~20 (1 sola de input) |
| **Predice** | Marcadores grupos + equipos KO + marcador final/3º + campeón | Todo: marcador, posiciones, clasificados, campeón, goleadores, MVP | Nada (se llenan resultados reales) |
| **Multi-jugador** | Sí, ~26/hoja × 2 hojas. Escala copiando bloques de 13 col | Sí, **5 jugadores** (más = versión de pago). Admin pega valores | **No** |
| **Puntaje** | Acumulativo configurable: 1X2=5, GD=5, exacto=10, aprox=3, equipo KO=10, final=10 | Por capas + **crédito parcial por GD** + **bonus por jornada** | n/a (3/1/0 deportivo interno) |
| **8 mejores 3º** | Coeficiente único + `LARGE`; **tabla FIFA 495** (`AssignThird`) por `VLOOKUP` | **Tabla 495** (`Combinaciones3`) + flag de fila activa | **Bitmask potencias de 2** + **tabla 495** (`tMT`) por `VLOOKUP` |
| **Desempates grupo** | Cadena FIFA completa con H2H + detector de ambigüedad | 6 escenarios, parte manual | Clave compuesta + `RANK` + H2H + detección + dropdown manual |
| **Input** | Números de equipo a mano (frágil) | Marcador texto libre + dropdowns de grupo | 1 hoja `Ingreso`, marcadores |
| **Datos 2026** | 48 reales sembrados + fixture + sedes reales | 48 sembrados (muestra) + fechas | 48 reales + fixture + sedes reales |

---

## 🎯 El hallazgo convergente (lo más importante)

**Los 3 modelos resuelven el problema de los 8 mejores terceros de la misma forma: una tabla precalculada de las 495 combinaciones (C(12,8)) + un lookup.** Ninguno intenta derivarlo por fórmula/IFs. Es la pieza FIFA oficial (asignación tercero→slot del bracket según qué grupos aportan tercero).

→ **Decisión de diseño casi forzada:** nuestra quiniela también necesita esa tabla de 495 filas. Es la columna vertebral del formato 2026. (Coincide con el Annexe C del reglamento que ya guardamos.)

---

## 🥷 Lista para robar (mejores mecánicas)

1. **Tabla de 495 combinaciones de terceros como lookup.** Los 3 coinciden. Imprescindible.
2. **Clave numérica compuesta + `RANK`/`LARGE` para ordenar** (terceros y desempates):
   - Baum: `H = Pts·1e6 + (GD+500)·1e3 + GF·1 + fairplay·1e-3 + rankFIFA·1e-6`, luego `LARGE`.
   - ClasesExcel: bitmask con potencias de 2 (A=1, B=2, C=4…L=2048) para codificar el set de 8 grupos en un entero único.
   - Convierte un orden lexicográfico multi-criterio en un solo número ordenable. Limpio y auditable.
3. **Crédito parcial por diferencia de goles** (Tejero): en vez de todo-o-nada, `puntos_GD · (1 − |Δreal − Δpred|·ajuste)` con piso en 0. Scoring más fino.
4. **Bonus por jornada/fase** (Tejero, columna `I`): multiplica los puntos según la fase, premiando más las rondas finales.
5. **Puntaje acumulativo en una hoja de settings** (Baum `PrSettings`, Tejero `ADMIN`): cambiar reglas sin tocar fórmulas. Buena UX.
6. **Separación de capas:** datos / motor / input / presentación, con motor en hojas ocultas. Los 3.
7. **Detector de empate irresoluble** que pide intervención manual solo cuando hace falta (Baum `Distinctness` + punto rojo; ClasesExcel aviso + dropdown).
8. **Gating por contador** para no mostrar cruces basura hasta completar la fase de grupos (ClasesExcel `AL8=144`).
9. **Motor de grupo parametrizado por letra** (`CODE(letra)-65`): una sola fórmula replicada a 12 grupos.

---

## ⚠️ Errores a evitar (debilidades de los 3)

- **Input de equipos por número escrito a mano** → usar **dropdowns validados** contra la lista de selecciones.
- **Multi-jugador por copiar-pegar valores manual** (Baum y Tejero) → es el punto más frágil y tedioso. Si va a haber varios participantes, evaluar **Google Sheets / Forms** o estructura mejor que un xlsx compartido.
- **Sin bloqueo por deadline** → en archivo compartido permite editar una predicción después del kickoff. Falta candado temporal.
- **Marcador como string concatenado** tipo `"1|2-1"` (Tejero), parseado con `MID`/`FIND` → frágil. Usar columnas separadas de goles.
- **Fórmulas monstruo por concatenación de nombres** (ClasesExcel, joins por texto sensibles a acentos/espacios) → con `XLOOKUP`/`LET`/`FILTER` quedaría mucho más limpio.
- **Dependencia de Excel 365** (arrays dinámicos, `ANCHORARRAY`) → rompe en LibreOffice/Sheets.

---

## Decisiones que esto abre (para los próximos pasos)

1. **Plataforma:** ¿Excel/Sheets como los modelos, o algo distinto (web/Python, más afín a tu stack)? El dolor común de los 3 es el multi-jugador en xlsx.
2. **Qué se predice:** ¿marcador exacto de cada partido, o algo más liviano (1X2 + clasificados + campeón)? Define la fricción para los participantes.
3. **Sistema de puntaje:** acumulativo configurable + crédito parcial + bonus por fase es el estado del arte de estos modelos.
4. **Alcance del bracket:** ¿se predicen cruces exactos (necesita la tabla 495 del lado del jugador) o solo "quién avanza"?

*Las plantillas fuente: `WCup_2026_4.2.6_en.xlsx`, `ADMIN-Excel-Mundial-2026.xlsx`, `Fixture-Copa-Mundial-FIFA-2026_ClasesExcel.xlsx` (en Downloads).*
