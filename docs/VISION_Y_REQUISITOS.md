# Visión y requisitos — Quiniela Mundial 2026

> Captura de los requisitos de Boris (2026-06-07). Documento vivo. **Aún no se construye nada**; esto fija el QUÉ antes del CÓMO.

---

## Concepto

Quiniela entre amigos/familia sobre el Mundial 2026. Cada participante pronostica resultados; se comparan aciertos, se rankea y se siguen estadísticas a lo largo del torneo. Boris administra (recibe predicciones, las relaya a Claude); Claude genera y mantiene el Excel.

## Modelo operativo (cómo fluye)

1. Claude genera un **Excel con los 72 partidos de la fase de grupos**.
2. Se genera además una **plantilla en blanco para compartir** (cada participante la llena con sus pronósticos).
3. El participante llena su plantilla y la devuelve. Boris le dice a Claude: *"estas son las predicciones de Juanito Pérez"*.
4. Claude **guarda** esas predicciones y **genera la pestaña** de ese participante.
5. Claude arma un **panel de comparación arriba**: predicciones de cada uno lado a lado para comparar quién acertó.
6. A medida que pasan los partidos, los **partidos "pasados"** muestran el resultado real y se ve el **histórico**.
7. Al cerrar una fase, **se crean instancias para la(s) siguiente(s)** (octavos, cuartos, …) y se repite el mismo proceso.

## Requisitos funcionales (de Boris)

| # | Requisito |
|---|-----------|
| RF-1 | Excel con los 72 partidos de fase de grupos. |
| RF-2 | Plantilla en blanco compartible para que cada participante llene sus pronósticos. |
| RF-3 | Ingesta de predicciones por participante (Boris relaya; Claude guarda y crea su pestaña). |
| RF-4 | Panel de comparación (arriba): pronósticos de todos lado a lado + aciertos. |
| RF-5 | Vista de partidos jugados (resultado real) e histórico. |
| RF-6 | Generar instancias de las fases siguientes (eliminatorias) y repetir el flujo. |
| RF-7 | **Estadísticas:** quién acertó más partidos (1X2) vs quién acertó más marcadores exactos. |
| RF-8 | Vista individual por participante. |
| RF-9 | "y un largo etc." → ver IDEAS_DEEP_RESEARCH.md para ampliar. |

## Requisitos no funcionales / restricciones

- **Plataforma:** Excel subido a Google Sheets → **fórmulas portables** (evitar arrays dinámicos solo-365).
- **Source of truth = markdown + CSV**; el Excel se genera, no se edita a mano.
- **Operador único (Boris):** los participantes NO editan el archivo maestro; Boris relaya. (Evita el dolor multi-jugador de los modelos analizados, que era copiar-pegar manual y frágil.)
- Determinístico y regenerable (si llega una corrección, se regenera el xlsx).

## Decisiones pendientes (a resolver en pasos siguientes)

- **Qué se predice exactamente:** ¿marcador exacto de cada partido? ¿1X2? ¿clasificados? ¿campeón/goleador? (Los modelos cubren todo el espectro.)
- **Sistema de puntaje:** ¿acumulativo (1X2 + diferencia + exacto)? ¿crédito parcial por diferencia de gol? ¿bonus por fase?
- **Alcance del bracket en la predicción:** ¿el jugador pronostica cruces exactos (necesita lógica de 495 terceros del lado del jugador) o solo "quién avanza"?
- **Deadline / candado:** ¿se cierran pronósticos antes del kickoff? Como Boris relaya, el candado es operativo (no técnico), pero conviene política clara.
- **Premio / objetivo:** ¿es por diversión, hay pozo, etc.? Afecta qué tan robusto debe ser el anti-trampa.

## Ideas adicionales (Claude — borrador, se amplía con deep research)

- **Pronóstico bloqueado por timestamp**: registrar fecha de ingreso de cada predicción (auditoría).
- **Bonus por fase** (octavos valen más que grupos) y **multiplicador de riesgo** (acertar un batacazo da más).
- **"Joker" / doble puntos** en 1-2 partidos que el jugador elige.
- **Pronóstico de posiciones de grupo** (1º/2º/3º) además del marcador.
- **Pronósticos especiales de torneo**: campeón, finalista, goleador, sorpresa, primer eliminado.
- **Leaderboard con evolución temporal** (gráfico de posición fecha a fecha).
- **"Racha"** (aciertos consecutivos) y otras métricas tipo telemetría (igual que el álbum).
- **Tarjeta compartible** por participante (estilo la del álbum) con su % de acierto.
- **Vista "head-to-head"** entre dos participantes.
- **Detección de pronósticos idénticos / copiados** entre participantes.

> Ampliar y priorizar (incl. nice-to-have) con deep research → `IDEAS_DEEP_RESEARCH.md`.

---

## RF-10 — Premios y validación (VITAL · 2026-06-07)

- **Entregar la planilla basta para jugar** y aparecer en el ranking. NO es obligatorio pagar antes del torneo.
- El **premio (pozo)** es solo para quien **valida** (paga). Quien no valida **igual ve lo que pudo haber ganado** → gancho motivacional para que pague.
- **UI — NO usar la palabra "pagado"** (se ve feo). Usar **✓ validado** / "en juego" para los validados, y **atenuar (dimmed)** la fila/monto del que no validó ("sin validar · no lo cobra").
- **Panel de premios:** pozo actual (= nº validados × cuota) + reparto (1º/2º/3º, configurable) + premio proyectado de cada uno según su posición; el de los no-validados se muestra atenuado ("lo que dejaría de ganar").
- **Estado: construido en el demo** (`build/gen_demo_site.py` → `CUOTA`, `NO_VALIDADO`, `DIST` configurables). Caso demostrado: un líder no validado (2º) ve su premio en gris, "no lo cobra".
- **Cuota: $10.000** (fijada por Boris 2026-06-07). Reparto provisional 50/30/20.
- Pendiente real: confirmar reparto definitivo (¿incluir sub-campeonatos en el pozo?) y la regla de redistribución si un no-validado queda en posición de premio.
