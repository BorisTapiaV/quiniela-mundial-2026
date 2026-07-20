# Retrospectiva del experimento de pronóstico — La Casa vs la realidad

> 🔒 **USO INTERNO.** Cierre del experimento del 2026-06-07 (scouting de 61 agentes + validación de consenso → planilla "La Casa"), evaluado contra los resultados reales del Mundial 2026 al terminar el torneo (2026-07-19).
> **Reproducible:** `python build/retro_experimento.py` (computa todo desde `data/resultados*.csv` + `data/predicciones/CASA*.csv`).
> **Insumos:** `referencias/scouting-48-pronostico-casa.md` (el pronóstico) · `referencias/validacion-consenso.md` (la validación) · `referencias/analisis-3-modelos.md` (diseño de mecánica).

---

## 1. Qué fue el experimento

La hipótesis: **¿una máquina de Deep Research + validación de consenso predice mejor un Mundial que las corazonadas humanas de una quiniela?**

El pipeline (2026-06-07):
1. **Scouting de 61 agentes** (48 scouts web + 1 normalizador de fuerza + 12 de grupo), prompt optimizado por Leonor v4.5 → rúbrica de fuerza 0-100 comparable + triangulación de fuentes → `data/scouting_48.json`.
2. **Pronóstico "La Casa"** (la planilla de Boris, NO compartida con los jugadores): 12 grupos, bracket KO, semis, finalistas, campeón, goleador.
3. **Validación de consenso** (7 agentes): cruce contra apuestas (bet365/DraftKings/FanDuel/Kalshi), simuladores (Opta/TDS/PELE) y expertos → **93% de coincidencia ponderada** (Paulo 75%).

---

## 2. Scorecard — predicho vs. real (computado desde los resultados)

| Predicción | Resultado real | Acierto |
|---|---|:--:|
| **Ganadores de grupo** | **11/12** — único fallo Grupo K (predijo Portugal → salió Colombia) | 🟢 92% |
| **Marcadores exactos** | **13/72 (18%)** — el más alto del pool → **ganó la quiniela** (+75 sobre el 2º) | 🟢 |
| **Semifinalistas** | **4/4 exactos** (España, Francia, Inglaterra, Argentina) | ✅ |
| **Finalistas** | **2/2 exactos** (España, Argentina) | ✅ |
| **Campeón** | **España** | ✅ |
| **Goleador (Bota)** | **Mbappé** (10 goles) | ✅ |
| Primer eliminado *(especial retirado)* | Cabo Verde → CPV terminó **2º de grupo y avanzó** | ❌ |
| Sorpresa *(especial retirado)* | Bosnia → BIH avanzó como **mejor 3º** (predicho 2º) | 🟡 |

---

## 3. Análisis — dónde el método fue fuerte y dónde débil

- **Fuerte en lo estructural / favoritos:** 11/12 ganadores de grupo, el final four completo, campeón. Ahí la fuerza de plantel + FIFA + consenso convergen y el método tiene señal real.
- **Débil en la cola de baja información:** el peor fallo fue "primer eliminado = Cabo Verde", que terminó 2º y avanzó (le ganó a Uruguay). Elegir entre minnows quasi-equivalentes no tiene señal en una rúbrica de fuerza. **Retirar los especiales de cola (primer eliminado / sorpresa) fue correcto** — esta retrospectiva confirma por qué eran ruido.
- **El valor real del scouting caro fueron los marcadores.** Los binarios de cabeza (campeón, ganadores de grupo) coincidieron con el consenso *gratis*; lo que ganó el pozo fueron los **13/72 exactos**, que salen de la granularidad GF/GC por selección que el mercado no da (el mercado dice "gana X", no "2-1").

---

## 4. La decisión clave — la recalibración del campeón (fue humana, y fue tuya)

El modelo crudo de 61 agentes daba **Francia** campeón (fuerza 95, empatada #1 con Argentina; España 94) y final **Francia vs Argentina**. En el vértice del bracket la rúbrica tenía un **cuasi-empate de 3** que no sabía resolver.

La capa de validación de consenso marcó a **España** como el #1 real del mercado (18.2% implícita, #1 en 4 casas + 2/3 modelos). Boris **envió España campeón y mantuvo Argentina** como la otra finalista → clavó la final exacta **España-Argentina + campeón**.

Eso le ganó incluso a la recomendación del consenso, que sugería finalistas España+Francia. El humano-en-el-loop **combinó el bracket del modelo (Argentina por su lado) con la señal de campeón del consenso (España)** y acertó las dos. Esta es la jugada que separó al experimento de un simple "copiar las cuotas".

---

## 5. 🔧 Refinamientos para el próximo predict (2030) — candidatos a probar

> ⚠️ **Todos son N=1** (un solo Mundial). Son hipótesis a testear el próximo ciclo, no leyes. Se documentan para que el "predict que se decide de los resultados" deje de ser ad-hoc y sea un proceso repetible.

**R1 — Gate de consenso en el vértice del bracket.** Cuando el top de la rúbrica de fuerza está en cuasi-empate (Δ ≤ ~3 pts), el modelo NO tiene poder resolutivo para los binarios de cabeza (campeón, finalistas). Regla: en esa franja, **deferir al #1 del consenso de mercado**. Evidencia: Francia 95 = Argentina 95 = España 94 era irresoluble para la rúbrica; el mercado sí resolvió (España), y la recalibración fue el acierto decisivo.

**R2 — Descuento por bandera cualitativa.** El único fallo de grupo (Portugal, fuerza 88 #4 → cayó a Colombia, y encima eliminado en octavos) estaba **anticipado en la propia nota de scouting**: "dependencia de Ronaldo (41), fragilidad defensiva (7 GC en 6), histórico de quedarse corto". La rúbrica numérica lo sobre-rankeó igual. Regla: cuando la nota cualitativa de una selección marca **dependencia de estrella + fragilidad defensiva + "se queda corto"**, aplicar un ajuste a la baja explícito; los flags cualitativos predijeron mejor que el número.

**R3 — No apostar la cola.** Mantener retirados los especiales de "primer eliminado" y "sorpresa" entre minnows: sin señal de modelo (Cabo Verde fue el contraejemplo perfecto). Si un formato futuro los exige, marcarlos como puro azar y no gastarles esfuerzo de modelo.

**R4 — División del trabajo, en este orden.** (1) **Consenso primero** para los binarios de cabeza (campeón/finalistas/ganadores de grupo) — barato y de alta precisión. (2) **Scouting profundo** reservado para los **marcadores/GF-GC** (los exactos), que es donde tiene valor único y donde de hecho se ganó el pozo. Invertir el orden ahorra agentes sin perder aciertos.

**R5 — Estrategia de pool: alinear con consenso gana; diferenciarse solo con edge real.** La Casa (93% consenso) ganó por +75; la única diferenciación del modelo crudo (Francia campeón) habría **perdido**. En un pool de humanos casuales, maximizar alineación con el consenso es la estrategia dominante; diferenciarse solo paga donde hay edge defendible (a N=1, el único edge demostrado fue la granularidad de los exactos).

**R6 — Formalizar el "recalibration gate" como paso del pipeline.** El acierto del campeón fue una decisión discrecional bien tomada, pero ad-hoc. Convertirla en un paso fijo: *scouting → pronóstico crudo → gate de consenso que decide, binario por binario, si el modelo se override con el mercado* (aplicar R1). Es el mismo instinto del loop de calibración de Profiler (reference class + consenso + Brier): la corazonada se vuelve un gate documentado.

---

## 6. Caveat honesto (N=1)

El acierto del campeón es **un binario único**: con un solo Mundial no se separa limpio skill de suerte *en ese campo*. Lo que sí es difícil de atribuir al azar es la **amplitud** — 11/12 grupos + 4/4 semis + 2/2 finalistas, eventos cuasi-independientes. Esa amplitud es la evidencia de que el método scouting+consenso tiene skill de forecasting al nivel favorito/estructural. El experimento validó la hipótesis, con la humildad de que un Mundial es una muestra.

---

## 7. Reproducibilidad

- `python build/retro_experimento.py` → recomputa el scorecard de §2 desde los datos.
- Fuentes del pronóstico: `data/predicciones/CASA.csv` (grupos), `CASA_ko.csv` (bracket), `CASA_especiales.csv` (campeón/goleador).
- Resultados reales: `data/resultados.csv` (grupos), `data/resultados_ko.csv` (KO).
- Motor de bracket/standings: `build/engine.py` (`full_bracket`, `compute_all_standings`).

*Generado 2026-07-19 · cierre del experimento de pronóstico Mundial 2026 · 0 voseo.*
