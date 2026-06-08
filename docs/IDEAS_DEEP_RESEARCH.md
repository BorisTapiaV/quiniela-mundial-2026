# Catálogo de ideas — Quiniela Mundial 2026

> Fuente: deep research (2026-06-07, run `wf_6075ee80-517`) — 5 ángulos, 19 fuentes, 70 claims extraídos, 25 verificados con voto adversarial 3 votos, 23 confirmados / 2 refutados. **Más** relleno de criterio de diseño (Claude) para las 2 lagunas que el research no cubrió. Cada idea trae **esfuerzo Excel/Sheets** y **valor para el jugador**.

**Plataformas de referencia:** Kicktipp, Superbru, Sky Super6, Sportspoule, Bracket2026, Hermann Baum (Excel), HowToExcel, Matejero.

---

## 🏆 Matriz priorizada (lo verificado)

| # | Idea | Esfuerzo | Valor | Fuente |
|---|------|:--------:|:-----:|--------|
| 1 | **Puntaje 3 niveles**: 1X2 + diferencia de gol + marcador exacto | Bajo-Medio | **Alto** | Kicktipp, Superbru ✅ |
| 2 | **Configurabilidad**: pesos de puntaje en hoja Settings (celdas con nombre) | **Bajo** | Alto (indirecto) | Baum, HowToExcel ✅ |
| 3 | **Candado/deadline por jornada** (cierre al kickoff) | **Bajo** | **Alto** | Sky Super6 ✅ |
| 4 | **Pronósticos especiales de torneo** (campeón, goleador, primer eliminado, sorpresa) | **Bajo** | **Alto** | Kicktipp, Bracket2026 ✅ |
| 5 | **Joker / comodín** x2 o x3 limitado por jugador | Bajo-Medio | **Alto** | Sportspoule ✅ |
| 6 | **Crédito parcial por aproximación** (marcador "cercano") | Medio | Medio-Alto | Superbru, Baum ✅ |
| 7 | **2 variantes KO**: simple (quién avanza) vs completa (marcador + equipos) | Medio / Alto | Alto | Baum ✅ |
| 8 | **Hoja "Predictor"**: hasta qué ronda llega cada selección (independiente del marcador) | Medio | Medio-Alto | Matejero, Baum ✅ |
| 9 | **Tabla 495 combinaciones** (mejores terceros → bracket R32) | **Alto** | **Alto** | FIFA/Wikipedia, Baum ✅ |
| 10 | **Multiplicador de riesgo/underdog** (cuota según consenso del grupo) | **Alto** | Alto (competitivo) | Kicktipp "Quote" ✅ |
| 11 | Bonus extra: dark-horse +10, early-bird +20, "most upsets" | Medio | Medio | Bracket2026 ⚠️ 1 fuente |

---

## 1. Sistemas de puntaje (el núcleo)

**Convención dominante = puntaje escalonado de 3 niveles por partido**, con pesos configurables:

| Plataforma | 1X2 (tendencia) | Diferencia de gol | Marcador exacto |
|------------|:---------------:|:-----------------:|:---------------:|
| **Kicktipp** (default) | 2 | 3 | 4 |
| Kicktipp (esquema 8-20) | 4 | 6 | 8 |
| **Superbru** | 1 | 1.5 (close) | 3 |
| Sky Super6 / Sportspoule (2 niveles) | 2 | — | 5 |

- Los niveles son **escalonados, no acumulativos** en Kicktipp (te dan el nivel más alto que alcanzas), a diferencia de Baum que los suma. → **decisión de diseño nuestra.**
- **Alternativa simple de 2 niveles** (exacto=5, resultado=2, sin crédito por diferencia): más fácil, menos discriminante. Recomendado solo si el grupo es muy casual.
- **Crédito parcial por aproximación**: Superbru da 1.5 si aciertas el resultado y el marcador queda "cerca" (fórmula propietaria que mezcla diferencia de gol + total de goles; umbrales NO públicos → definir el nuestro, p. ej. `|Δpred − Δreal| ≤ 1`).
- **Multiplicador de riesgo (Kicktipp "Quote"):** los puntos dependen de cuánta gente predijo igual — acertar al outsider vale más que al favorito. Potente pero **esfuerzo alto** (recalcular cuotas con COUNTIF sobre las predicciones de todos y congelar al cierre) y difícil de explicar.

## 2. Mecánicas de engagement

- **Joker / comodín** (#5): el jugador marca 1 partido por jornada para multiplicar sus puntos (x2 Kicktipp/Footy, x3 Sportspoule), con cupo limitado. **Mejor relación valor/esfuerzo** — añade estrategia y permite remontadas.
- **Pronósticos especiales de torneo** (#4): campeón (~10 pts), goleador/Golden Boot (~5 pts), primer eliminado, sorpresa. Se fijan al inicio y se resuelven al final → **mantienen enganchado al que va último** hasta la final.
- **Deadlines/candados** (#3): cierre duro al kickoff del primer partido de la jornada. En nuestro modelo (Boris ingresa) = hora-límite de envío. Es el **control anti-trampa más importante**.
- **Bonus extra** (#11, ⚠️ inspiración, 1 sola fuente vendor): dark-horse (+10 si avanza un equipo no-top-10 que pusiste), early-bird (+20 por enviar 24h antes — resuelve el problema operativo de que lleguen a tiempo), "most upsets".

## 3. Manejo del formato 2026

- 48 equipos / 12 grupos / **Round of 32** (16 partidos, ronda KO nueva) → avanzan 2 por grupo (24) + **8 mejores terceros** = 32. 104 partidos.
- **Crítico:** incrustar la tabla FIFA de asignación de terceros (**C(12,8)=495 combinaciones**, Annexe C) para que dos equipos del mismo grupo no se crucen en R32. Es la parte más difícil de automatizar. Sin esto el bracket es inválido. (Ya lo confirmaron los 3 modelos analizados.)
- **2 variantes de puntaje KO** (#7): (1) solo acertar qué equipos avanzan en cada ronda, el orden no importa — mantiene jugable la fase aunque falles marcadores; (2) marcador completo + equipos. La variante 1 es la recomendada para grupo casual.
- **Hoja "Predictor"** (#8): cada uno predice hasta qué ronda llega cada selección, independiente de los marcadores. Diversifica las vías de ganar puntos; engancha al que sabe de equipos pero no clava marcadores.

---

## 4. Estadísticas y visualizaciones ⚠️ (laguna del research — criterio Claude + modelos)

> El deep research NO trajo claims verificados para esto (tu punto 3, RF-7/RF-8). Relleno con diseño propio + lo visto en los 3 modelos (que sí tienen hojas Stats/DailyClas). Marcar como NO investigado.

| Idea | Esfuerzo | Valor |
|------|:--------:|:-----:|
| **Acierto 1X2 vs marcador exacto** por jugador (dos métricas separadas) — tu RF-7 | Bajo | Alto |
| **Leaderboard con desglose por fase** (grupos / R32 / R16…) | Bajo | Alto |
| **Evolución del ranking fecha a fecha** (sparkline por jugador) | Medio | Alto |
| **Racha** (aciertos consecutivos de resultado) | Medio | Medio-Alto |
| **Head-to-head** entre dos jugadores | Medio | Medio |
| **Percentil / nota** por jornada (no solo posición) | Bajo | Medio |
| **Pronóstico-consenso / contrarian**: cuánto te desvías del promedio del grupo | Medio | Medio-Alto |
| **Vista individual** por participante (su pestaña) — tu RF-8 | Bajo | Alto |
| **Puntos en juego por jornada** + distribución 1/X/2 del grupo | Bajo | Medio |
| **Tarjeta compartible** por jugador (estilo la del álbum) con su % de acierto | Medio | Alto |

## 5. Errores comunes a evitar ⚠️ (laguna del research — criterio Claude + modelos)

> Tampoco quedó cubierto por el research (tu punto 6). Síntesis de lo aprendido en los 3 modelos + diseño.

- **Premiar demasiado el marcador exacto** → desmotiva, porque es raro acertarlo; mejor que el 1X2 ya sume.
- **Sin desempate claro del leaderboard** → definir tiebreaker (p. ej. nº de marcadores exactos, luego pronóstico de campeón).
- **Sin candado temporal** → permite predecir con partidos ya jugados (la falla #1 de los modelos analizados).
- **Marcador como string concatenado** (`"1|2-1"`) → frágil; columnas separadas de goles.
- **Join por nombre de equipo** (acentos/espacios) → usar siempre el **código** (POR, ARG…) como clave.
- **Penales sumados al marcador** en KO → campo dedicado.
- **Fórmulas solo-Excel-365** (arrays dinámicos) → rompen al subir a Sheets.
- **Multi-jugador por copiar-pegar manual** → en nuestro modelo lo esquivamos: Boris ingresa, Claude regenera.
- **Reglas que cambian a mitad de torneo** → fijarlas y versionarlas desde el día 1.

---

## ⚠️ Claims REFUTADOS (no usar como hechos)

- ❌ Bonus por progresión escalado "grupo 3 / R32 5 / R16 10 / QF 20 / campeón 100" — refutado (voto 1-2). Era diseño propietario de una sola fuente.
- ❌ "Un Excel maneja el formato 2026 automáticamente con hasta 500 participantes" — refutado (0-3).
- Sky Super6 fue **descontinuado** en su forma de apuestas en 2024; vale como referencia de diseño, ya no opera.

## 🎯 Qué implica para nuestro diseño

1. **Adoptar el puntaje de 3 niveles configurable** (núcleo) + hoja Settings. Decisión pendiente: ¿escalonado (Kicktipp) o acumulativo (Baum)?
2. **Joker + especiales de torneo + candado** = el trío de engagement de mejor relación valor/esfuerzo; los 3 son esfuerzo bajo.
3. **La tabla 495** es obligatoria (ya confirmado por research + 3 modelos).
4. **Variante KO simple** ("quién avanza") para arrancar; la completa es opcional.
5. Las **estadísticas** (tu RF-7/8) hay que diseñarlas nosotros — el research no las cubrió. Buen candidato a un research focalizado posterior si quieres más.

> **Decisiones que destraban la construcción:** (a) qué se predice exactamente, (b) escalonado vs acumulativo, (c) variante KO simple vs completa, (d) qué especiales/jokers incluir. Todas en `VISION_Y_REQUISITOS.md` → "decisiones abiertas".
