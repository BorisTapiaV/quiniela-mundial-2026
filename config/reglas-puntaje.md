# Reglas de puntaje — Quiniela Mundial 2026

> Decisiones de Boris (2026-06-07). Valores **configurables** (se afinan sin tocar el motor). Provisionales abajo.

## Decisiones firmes

| # | Decisión | Elegido |
|---|----------|---------|
| 1 | Pronóstico por partido | **Marcador exacto** (ej. 2-1) |
| 2 | Cómo suma el puntaje | **Escalonado / Kicktipp** — te quedas con el nivel más alto, NO se suman |
| 3 | Eliminatorias | **Simple — quién avanza** (no marcador KO). **Alcance B:** 72 de grupo + el jugador pica quién avanza en cada ronda KO |
| 4 | Engagement | **Especiales de torneo** ✓ · **Bonus por fase** ✓ (KO vale más). **Joker NO** (no elegido) |

## Puntaje base por partido (escalonado, provisional)

| Acierto | Puntos |
|---------|:------:|
| Marcador exacto | **5** |
| Solo diferencia de gol | **3** |
| Solo 1X2 (resultado) | **2** |
| Nada | 0 |

→ Te quedas con el **más alto** que aciertes (no acumulativo). Máx 5 por partido.

## Especiales de torneo (provisional, se fijan al inicio)

| Especial | Puntos |
|----------|:------:|
| Campeón | 50 |
| Goleador (Bota de Oro) | 25 |
| Primer eliminado | 20 |
| Sorpresa (a definir) | 15 |

## Modelo de planilla: UNA sola, todo antes de empezar (DECISIÓN 2026-06-07)

**Una única planilla**, llenada completa **antes del primer partido**. NO dos planillas faseadas (eso creaba un problema de sincronización). Es el modelo "bracket challenge" clásico.

El jugador ingresa, de una:
1. **Selección + goles** de los 72 partidos de grupo (marcadores).
2. (auto) De esos 72, el **cuadro se arma solo**: sus posiciones de grupo + sus **8 mejores terceros** (tabla 495) → su R32. El jugador NO calcula la clasificación.
3. **Cascada de ganadores** por desplegable hasta el campeón. Elige ganador; el perdedor queda diferenciado por defecto. **Sin goles en KO, solo quién pasa.** (Listas desplegables dependientes en Excel; los 3 modelos de referencia ya lo hacen.)
4. **Especiales:** campeón y finalistas salen del cuadro; goleador / primer eliminado / sorpresa se eligen aparte.

**Telemetría que habilita (el oro del proyecto):** quién "murió" en primera ronda (su campeón eliminado en grupos), cuáles brackets siguen vivos rumbo a la victoria, hasta dónde sobrevive la predicción de cada uno.

**Costo asumido:** es el enfoque con la lógica pesada (cuadro de cada jugador derivado de SUS grupos vía 495). Mitigado: los 3 modelos Excel lo prueban y la tabla 495 ya está construida.

## Puntaje de avance / bracket (Alcance B, bonus por fase — provisional)

Por equipo que **efectivamente alcanza** esa ronda (el orden no importa, estilo Baum variante 1). Escala creciente = bonus por fase:

| Hito | Puntos por equipo |
|------|:-----------------:|
| Clasifica a R32 (auto-derivado de sus 72) | 2 |
| Avanza a R16 | 4 |
| Avanza a Cuartos | 6 |
| Avanza a Semis | 10 |
| Avanza a la Final | 16 |

→ El **campeón** se puntúa vía el especial (50), no se duplica con el avance. (Ajustable.)
→ **Rebalance 2026-06-07 aplicado** (escala duplicada vs provisional original 1/2/3/5/8): para llevar el reparto a 50% grupos / 35% KO / 15% especiales (ver `referencias/balance-puntaje-disyuntiva.md`).

## Resumen del modelo de puntaje

1. **72 partidos de grupo** — escalonado (exacto 5 / dif 3 / 1X2 2). Máx **360 (50%)**.
2. **Avance KO** — por equipo que alcanza cada ronda (2/4/6/10/16). Máx **248 (35%)**.
3. **Especiales** — campeón 50, goleador 25, primer eliminado 20, sorpresa 15. Máx **110 (15%)**.
4. Sin joker. **Máximo total = 718.**
5. **Jugadores: ~12.** Bajo el umbral de 15 → el multiplicador underdog (Quoten-Regel) NO se implementa (no rinde con <15). El balance intermedio actual es el correcto para 12.

## Tiebreakers del leaderboard (provisional)

Empate de puntos → más marcadores exactos → acierto de campeón → ranking FIFA / sorteo.

## ⚖️ Disyuntiva abierta — volumen vs. apuesta audaz (2026-06-07)

**Problema:** un jugador clava 45/72 de grupos pero su bracket se revienta; otro clava solo 10/72 pero acierta al campeón del mundo. ¿Quién gana? No hay respuesta "correcta" — es elección de valores. Hoy los pesos hacen que grupos domine (71% del máx).

**4 palancas para manejarla:**
1. **Rebalancear pesos** — subir peso del bracket/campeón (directo pero burdo).
2. **Multiplicador de riesgo/underdog** — campeón que casi nadie puso vale más (premia audacia sin matar grupos).
3. **Sub-campeonatos / premios paralelos** ⭐ — "Rey de la fase de grupos" + "El Profeta" (campeón/bracket). Disuelve la disyuntiva: cada perfil gana lo suyo. Encaja con la telemetría de supervivencia.
4. **Supervivencia del bracket** como categoría propia.

**RESUELTA + REBALANCE APLICADO (2026-06-07).** Research (`referencias/balance-puntaje-disyuntiva.md`) trajo la **Paradoja del Torneo de Pronóstico** (Aldous, peer-reviewed): sobre-pesar el campeón → gana la suerte, no la habilidad. Por eso escala KO **intermedia** (no geométrica) + reparto 50/35/15. Pesos finales arriba. **12 jugadores** confirmado.

## 🏁 La "carrera" (leaderboard como narrativa de 2 actos)

El reparto 50/35/15 produce una **carrera de dos actos**, que es justo lo entretenido:
- **Acto 1 — fase de grupos (50%):** el **consistente** toma ventaja temprana (acumula aciertos partido a partido).
- **Acto 2 — eliminatorias + especiales (50%):** el **audaz** remonta si su bracket sobrevive (avance creciente + campeón 50). Como el KO+especiales pesa lo mismo que los grupos, un bracket fuerte **sí** puede dar vuelta una ventaja de grupos.

Esto es exactamente la **telemetría del visor HTML** (RF-7/8 + IDEAS "evolución del ranking fecha a fecha"): se ve quién lidera tras grupos, quién trepa en el KO, head-to-head, y "hasta dónde sobrevive cada bracket". La carrera y sus casuísticas son la vista estrella del visor.
