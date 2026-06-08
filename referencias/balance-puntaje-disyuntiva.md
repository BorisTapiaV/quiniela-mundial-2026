# Balance de puntaje — volumen vs. apuesta audaz (disyuntiva resuelta con evidencia)

> Deep research 2026-06-07 (run `wf_cc725e23-b64`, prompt optimizado por Leonor v4.5). 20 fuentes, 24 claims verificados / 1 refutado. Responde la disyuntiva del jugador A (45/72 grupos, bracket reventado) vs jugador B (10/72, clava al campeón).

---

## 🔬 El hallazgo clave: la "Paradoja del Torneo de Pronóstico" (peer-reviewed)

**Aldous, *A Prediction Tournament Paradox*, The American Statistician (2019/2021):** en un torneo de pronóstico con muchos jugadores, **el ganador rara vez es el más preciso**. En una simulación de 300 concursantes, el ganador estaba ~puesto 100 en precisión y el #1 nunca ganó. Razón: trade-off media-varianza — el más hábil tiene menor error esperado pero **menor varianza**; un jugador menos preciso pero más **audaz** (alta varianza) gana por suerte cuando los buenos se agrupan en el mismo puntaje.

→ **Esto reformula tu disyuntiva:** si pones demasiado peso en el campeón/bracket (mucha varianza), **la suerte decide y la habilidad no se premia**. Para un pool donde quieres que el que sabe tenga ventaja real, NO conviene el extremo audaz. (Fuente primaria, voto 3-0.)

---

## 1. Cómo lo resuelven las plataformas

| Plataforma | Esquema | Filosofía |
|---|---|---|
| **Kicktipp** (DE) | Grupos 2/3/4 (tendencia/dif/exacto). KO: puntos base = nº de ronda, exacto duplica | **Volumen** + escalada KO suave |
| **Superbru** (UK/global) | 1 / 1.5 (cerca) / 3. Win Point KO: 1 / 1.5 / 2 / 3 (grupos→final) | Volumen + escalada suave |
| **NCAA bracket** (ESPN/CBS/Yahoo/Fox, ~70% pools) | **Geométrico 1-2-4-8-16-32** por ronda → campeón = 32× primera ronda (~17% del total) | **Apuesta audaz extrema** |
| **Práctica casual** (printyourbrackets) | **Intermedio 1-2-3-4-6-10** | Equilibrio (recomendado) |

**Nuestro modelo escalonado (2/3/exacto) = exactamente el estándar Kicktipp.** ✓ Vamos bien.

## 2. Proporción grupos / KO / especiales

⚠️ **[DATA GAP honesto]:** ninguna plataforma publica el reparto % para un formato idéntico al nuestro (grupos con marcador + bracket sin marcador + especiales). Las plataformas son *o* puro bracket (NCAA) *o* puro pronóstico por partido (Kicktipp/Superbru). El reparto recomendado abajo es **recomendación de diseño inferida, no benchmark** — no presentarlo como "lo que hace la industria".

## 3. Mecánicas de equilibrio (que NO fuerzan elegir)

| Mecánica | Cómo | Protege a | Esfuerzo |
|---|---|---|---|
| **Multiplicador underdog** (Kicktipp Quoten-Regel) | acertar al outsider vale más que al favorito (calculado desde los picks de todos) | al audaz | Alto (>15 jugadores) |
| **Bonus por cercanía** (Superbru) | punto extra al pick correcto más cercano de cada partido | al consistente | Medio |
| **Upset / seed bonus** (NCAA) | puntos extra por avanzar sorpresas (definidas por ranking/seed) | al audaz | Medio |
| **Sub-campeonatos / premios paralelos** | "Rey de grupos" + "El Profeta" | a ambos | Bajo |

## 4. Recomendación del research (no de mí)

**[RECOMENDACIÓN DE DISEÑO]** para pool casual/familiar:
- **Reparto: ~45-55% grupos / ~30-40% KO / ~10-15% especiales.**
- **Escalada KO INTERMEDIA** (tipo 1-2-3-4-6 por ronda, **NO** 1-2-4-8-16): da ventaja al que clava al campeón **sin** que un solo acierto sentencie.
- Campeón con valor **alto pero NO dominante**.
- + bonus por cercanía (grupos) + ponderación creciente del bracket.
- **Trade-off asumido:** se sacrifica parte de la "pureza" del premio a la audacia para mantener vivos a ambos perfiles — coherente con la paradoja de Aldous (evitar que la varianza pura decida).

## ⚠️ Caveats honestos del research

- El reparto % es **inferencia de diseño**, no benchmark publicado.
- Evidencia más fuerte de pesos KO viene de **NCAA básquet**, no fútbol (transferencia estructural válida bracket=bracket, pero no validada en fútbol).
- **Precedente contrario:** Superbru usó puntaje KO **plano** (sin escalar) para el Mundial 2018 específicamente.
- Cifras de prevalencia (~70%/81%/5%) son de fuente secundaria propietaria.
- **Refutado:** que Kicktipp "recomiende oficialmente más puntos al KO" — NO lo hace; la escalada es configurable por el admin.

## Preguntas abiertas (afinan la decisión)

1. **N de jugadores** — con muchos, la varianza domina (Aldous); la Quoten-Regel necesita >15. Con 8 vs 40 cambia el balance.
2. Nuestro bracket es **sin marcador** → el multiplicador underdog de Kicktipp (opera sobre marcador) habría que **reformularlo como bonus por ranking FIFA** del equipo avanzado.
3. Valor relativo de los 3 especiales (campeón vs goleador vs primer eliminado) — sin benchmark.

---

## 🎯 Qué implica para NUESTROS pesos actuales

**Hoy:** grupos 360 (71%) / KO 124 (24%) / especiales 25 (5%). → **grupos pesa demasiado** vs el 45-55% recomendado. Tu instinto (que el bracket pese más) está respaldado.

**Rebalanceo propuesto** (para ~50/35/15, manteniendo escalada KO intermedia):
| Componente | Hoy | Propuesto |
|---|---|---|
| Grupos (72 × exacto) | 5 → 360 | 5 → 360 (sin cambio) |
| Avance KO por equipo | R32 1 / R16 2 / QF 3 / SF 5 / Final 8 → **124** | R32 2 / R16 4 / QF 6 / SF 10 / Final 16 → **248** |
| Especiales | 10/5/5/5 → 25 | campeón 50 / goleador 25 / 1º elim 20 / sorpresa 15 → **110** |
| **Total / reparto** | 509 (71/24/5) | **718 (50% / 35% / 15%)** ✓ |

Campeón (50) = ~7% del total: alto pero **no dominante** (respeta la paradoja). Todo en 3 líneas de `engine.py` (W_ADV, W_ESP).
