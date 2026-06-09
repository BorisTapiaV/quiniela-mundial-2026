# Deep Research — Enganche / Retención de la Quiniela

> **Run:** `wf_0d35a9c9-863` (2026-06-09) · 22 fuentes → 90 claims → 25 verificados adversarialmente → **6 confirmados**, 18+ refutados.
> **Prompt optimizado por Leonor v4.5** (modo quirúrgico) antes de lanzar — per rule global `deep-research-leonor-optimization`.
> **Hermano de** `IDEAS_DEEP_RESEARCH.md` (mecánicas de scoring) y `EXPERIENCIA_EN_VIVO_Y_WOW.md` (vistas en vivo).
> **Objetivo:** "que no puedan vivir sin verla" — pool privado ~12 personas, sitio estático + WhatsApp, 5 semanas.

---

## ⚠️ Lo más importante: la verificación adversarial fue dura

De ~25 claims candidatos, **solo 6 sobrevivieron** 3 rondas de refutación. Mucha "sabiduría de growth" NO se pudo validar con fuentes y se trata como **gap, no como hecho**. Esto es bueno: evita construir sobre folclore.

**Las 6 mecánicas validadas se apoyan TODAS en fuentes primarias** (docs/anuncios oficiales de las plataformas + 1 paper). **Caveat transversal:** el copy de plataforma valida que el feature EXISTE y su INTENCIÓN DE DISEÑO, **no su eficacia de retención** — no hay ninguna cifra de retención validada en el set.

---

## ✅ Las 6 mecánicas VALIDADAS (con fuente primaria)

| # | Mecánica | Eje | Implementación | Caso/Fuente |
|:-:|----------|-----|----------------|-------------|
| 1 | **La obsesión/identidad personal manda, no la demografía** — invertir en ganchos nominales y rituales diarios rinde más que features genéricas o rankings anónimos | 1, 5 | principio rector | Paper peer-reviewed NFL (β=0.73, p<0.001) [PMC12301884] |
| 2 | **Chat social con trash-talk** como diferenciador (GIFs/reacciones/pullas) — "the single reason Sleeper leagues are the most active" | 4, 2 | [IMAGEN] cards + WhatsApp (la app no es replicable, el *efecto* sí) | Sleeper oficial |
| 3 | **"Rey de la jornada"** — destacar al máximo anotador de cada día como celebración/premio especial | 3, 7 | [HTML estático] + [IMAGEN] card del día | Kicktipp "Game day winner" |
| 4 | **Delta de posiciones por jornada** (+3 / −2 puestos) — señal visible de movimiento, activa aversión a la pérdida | 1, 3 | [HTML estático] badge en leaderboard + página individual | Kicktipp "Individual ranking" |
| 5 | **Recap de LIGA COMPLETA** (no tu matchup) diseñado para "compartir y vacilar" — cubre a los 12, no a uno | 2, 4 | [IMAGEN] card de recap de jornada de los 12 jugadores | Yahoo Fantasy oficial |
| 6 | **Escalera de consolación** (win-up/lose-down) — el eliminado mantiene stakes y movimiento cada ronda | 7, 3 | [HTML estático] sub-competencia / tabla secundaria (NO tocar el scoring) | ESPN Playoffs oficial |

### Insight clave que cruza todo
**El contenido compartible debe ser de LIGA COMPLETA, no individual** (hallazgo #5). Una tarjeta que cubre a los 12 jugadores genera conversación grupal y reenvío; una que cubre solo a uno, no. Esto define cómo diseñar las cards de WhatsApp.

### Detalle por hallazgo

1. **Obsesión personal (β=0.73)** — N=439 apostadores NFL; único predictor significativo de engagement repetido, sobre edad/género. *Caveat:* obsesión medida con 1 ítem Likert, R²=0.198 (~20% varianza), transversal (no causal), población US ≠ familia chilena → **inferencial**. Fundamenta priorizar EJE 1 (ritual) + EJE 5 (ganchos nominales "tu campeón juega hoy") sobre gamificación genérica.
2. **Sleeper chat/trash-talk** — feature oficial + triangulado con reviews 2026. La app+chat NO es replicable (requiere backend); el *efecto* sí: cards estáticas con pullas que el organizador manda al grupo.
3. **Rey de la jornada (Kicktipp)** — "The top scorer of every game day will be highlighted... perhaps give away a special prize." Anti-abandono: cualquiera puede ganar UNA jornada aunque vaya último en el general.
4. **Delta de posiciones (Kicktipp)** — "see how many places he has won or lost each match day." Aversión a la pérdida (Kahneman-Tversky) visible y diaria, sin push, porque el sitio cambia cada día (vector permitido).
5. **Recap Yahoo** — "covers the *entire* league... share and talk about it... brag a little." Incluye top performers / biggest letdowns / most benched. *Refutado:* que se auto-entregue al chat sin acción manual.
6. **Consolación ESPN** — "each game's winner moves up, while the loser moves down." Adaptable como narrativa/sub-competencia para el matemáticamente eliminado (ej. "mejor pronosticador de eliminatorias", "duelo entre los últimos"). El scoring NO se toca.

---

## ❌ REFUTADO — NO asumir como validado

- **Modelo Hooked de Eyal** (Trigger→Action→Variable Reward→Investment) y "recompensas variables liberan dopamina/crean hábito" — única fuente blog secundario, insuficiente.
- **Narrativa de viralidad de Wordle** (share button emoji-grid, scarcity 1 puzzle/día, no-login como driver) — fuentes secundarias, no sobrevivió.
- **Recap de Yahoo auto-entregado al chat cada martes** sin acción manual — refutado.
- **Superbru ligas privadas por link para ~12** — plausible pero NO verificado (merece 2ª ronda, ver gaps).
- **KeepTradeCut / screenshot-trash-talk** como mecánica diseñada — refutado.
- **Outcome uncertainty como driver en brackets** — voto 0-1.

> Implicación: el marco teórico "Hooked/variable rewards" que yo había puesto en la síntesis inicial **no tiene respaldo validado aquí**. Las mecánicas concretas (rey de jornada, delta, recap de liga, consolación) sí.

---

## 🕳️ GAPS (lo que el research NO pudo validar)

- **EJE 5 (FOMO sin push):** no hay mecánica validada específica para el canal WhatsApp manual. El principio se infiere del hallazgo de obsesión personal, pero ninguna fuente documenta el "cómo".
- **EJE 6 (cadencia de drops mapeada al calendario):** **cero fuentes validadas** sobre ritmo óptimo. Cualquier calendario de contenido propuesto es **ESPECULATIVO** (criterio propio, no investigado).
- **Casos sin aporte validado:** Superbru (refutado por falta de verificación, no por evidencia en contra → 2ª ronda), Sky Super6, Footy Tipping, apps LATAM, literatura Eyal/Duolingo.

---

## 🎯 Síntesis → plan priorizado (cruce con lo ya construido)

Cruzando los 6 hallazgos validados con lo que ya existe en la quiniela:

| Prioridad | Acción | Hallazgo | Estado actual |
|:--------:|--------|:--------:|---------------|
| **1** | **Tarjeta diaria de LIGA COMPLETA para WhatsApp** (recap de la jornada cubriendo a los 12: líder, "rey del día", el que más cayó, supervivencias) | #5 + #2 + #3 | ⏳ no existe — es la palanca #1 |
| **2** | **Delta de posiciones ▲▼ por jornada** en leaderboard + página individual | #4 | parcial (hay leaderboard; falta el delta + histórico) |
| **3** | **"Rey de la jornada"** como sección/badge + card | #3 | parcial (hay sub-campeonatos; falta el de "día") |
| **4** | **Sub-competencia de consolación** para el eliminado (mejor pronosticador KO / duelo de últimos) | #6 | ⏳ no existe |
| **5** | **Ganchos nominales personales** en las cards ("tu campeón juega hoy", apodos) | #1 + #2 | ⏳ no existe |

**Lo que el research dice NO hacer:** no apoyarse en la teoría Hooked/variable-rewards como justificación (no validada); no asumir auto-entrega al chat (todo es reenvío manual del organizador); no inventar una cadencia "óptima" como si fuera dato.

**Pendiente de decidir (gaps):** la cadencia de drops (EJE 6) la tendremos que diseñar por criterio propio, marcada como tal. Opción: 2ª ronda de research enfocada solo en Superbru + apps LATAM de quiniela (lo único que quedó sin verificar por falta de búsqueda, no por evidencia en contra).

---

*Generado 2026-06-09 · DR optimizado por Leonor · verificación adversarial estricta (6/25 claims sobrevivieron).*
