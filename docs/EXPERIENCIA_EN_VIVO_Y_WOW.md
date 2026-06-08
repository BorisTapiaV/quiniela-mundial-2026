# Experiencia en vivo y visual — el "efecto wow"

> Consolida la dimensión **en vivo + visual** de la quiniela, que estaba dispersa: datos en vivo en `../referencias/datos-imagenes-apis.md`, ideas de gráficas en `IDEAS_DEEP_RESEARCH.md`, soporte de resultados parciales en `../build/README.md`. Documento creado 2026-06-07 (Boris flaggeó que faltaba juntarla).

## El principio

La quiniela **no es un leaderboard final** — su gracia es **vivir el torneo en vivo**: ver los partidos actualizarse, el ranking moverse jornada a jornada, los brackets sobrevivir o caer, todo bien visual. Ese seguimiento diario es lo que mantiene al grupo enganchado las ~5 semanas. El motor ya está pensado para esto (puntúa con resultados parciales), pero las **vistas en vivo y las gráficas** son lo que queda por construir y donde está el efecto wow.

---

## 1. Actualización de partidos / resultados

| Capa | Qué | Cómo (ver `referencias/datos-imagenes-apis.md`) |
|------|-----|------|
| **Resultado final** (puntúa) | marcador definitivo de cada partido | carga diaria/por jornada → `data/resultados.csv` parcial → motor recalcula. Manual o `football-data.org` + regeneración programada |
| **Marcador en vivo** (adorno) | minuto, goles, tarjetas, **expulsados** | `API-Football` vía **Netlify Function proxy** o fetch JS client-side; refresco ~60s durante partidos |
| **Vistas temporales** | partidos **de hoy / en vivo / próximos / jugados (histórico)** | derivado del fixture + resultados parciales |

El motor **ya soporta puntuar "al día de hoy"** — cada estado del torneo (pre / grupos en curso / fin grupos / KO en curso / cerrado) sale sin tocarlo.

## 2. El leaderboard que se mueve (la carrera)

- Ranking **parcial** actualizado tras cada partido/jornada.
- Indicadores de **cambio de posición** (▲▼ subió/bajó respecto a la jornada anterior).
- "Movimiento del día" / "remontada de la jornada".
- Ya hecho: leaderboard + barras de 2 actos (grupos vs bracket).

## 3. Brackets en vivo

- **Cuadro real** de eliminatorias actualizándose: equipos avanzando, eliminados atenuados.
- **Bracket de cada jugador**: cuáles siguen en pie vs reventados.
- Momento clave: **"tu campeón fue eliminado" 💀** (ya está la grilla de supervivencia).

## 4. Gráficas — el wow

| Gráfica | Qué muestra | Esfuerzo | Estado |
|---------|-------------|:--------:|:------:|
| **Evolución del ranking fecha a fecha** ⭐ | línea por jugador a lo largo del torneo (la carrera de verdad) | Medio | ⏳ pendiente — LA estrella |
| Desglose por componente | barras apiladas grupos/KO/especiales | Bajo | ✅ hecho (2 actos) |
| **Head-to-head** | dos jugadores comparados | Bajo-Medio | ⏳ |
| Distribución de campeones | cuántos van con cada selección | Bajo | ⏳ |
| Aciertos 1X2 vs marcador exacto | perfil de cada jugador | Bajo | parcial (sub-campeonatos) |
| Racha | aciertos consecutivos | Medio | ⏳ |
| Mapa de calor de aciertos por jornada | quién achuntó qué día | Medio | ⏳ |

## 5. Polish / efecto wow

- **Animaciones/transiciones** suaves al actualizar el ranking y el bracket.
- **Narrativa con badges**: "quién murió hoy", "el profeta", "remontada", "rey de la jornada".
- **Tarjeta compartible** por jugador (estilo la del ala álbum) para mandar al grupo de WhatsApp — alto valor de difusión.
- Tema visual del Mundial, banderas oficiales, micro-interacciones, momentos celebratorios (campeón, sub-campeonatos).

## 6. Cómo se entrega en un sitio estático (Netlify)

- **Gráficas:** librería JS liviana client-side (uPlot / Chart.js / ApexCharts) **o** SVG generado en Python — ambas compatibles con static.
- **Live:** fetch client-side a la API, o **Netlify Function proxy** para ocultar la API key (ver research de APIs).
- **Regeneración:** al cargar resultados → regenerar HTML → redeploy (o cron programado). Para el marcador minuto-a-minuto, fetch JS en el navegador.
- Todo respeta el principio del proyecto: **estático, solo lectura, cero backend propio**.

## 7. Requisito técnico nuevo: snapshots históricos

Para la **evolución del ranking fecha a fecha** (la gráfica estrella) hay que **persistir el puntaje de cada jugador por jornada** — el motor calcula el puntaje a cualquier corte, pero la serie temporal hay que guardarla:

- Proponer `data/historico/<fecha>.csv` (o un acumulado `data/historico.csv`) con `fecha, jugador, total` por jornada.
- Se llena re-corriendo el motor con los resultados disponibles a cada fecha de cierre de jornada.
- Alimenta la línea de evolución + los indicadores ▲▼ + "movimiento del día".

---

## Resumen — qué falta para el "en vivo + wow"

| | Estado |
|---|---|
| Motor con resultados parciales (estados intermedios) | ✅ |
| Leaderboard + barras 2-actos + supervivencia + calendario | ✅ |
| `data/resultados.csv` + orquestación de carga | ⏳ |
| Snapshots históricos por jornada | ⏳ (nuevo requisito) |
| Evolución del ranking (line chart) ⭐ | ⏳ |
| Marcador en vivo (minuto/eventos) vía API | ⏳ |
| Head-to-head, racha, mapa de calor, distribución | ⏳ |
| Animaciones + tarjeta compartible + narrativa de badges | ⏳ |

*Cross-ref: `IDEAS_DEEP_RESEARCH.md` (catálogo de features) · `referencias/datos-imagenes-apis.md` (APIs + integración) · `build/README.md` (motor + generadores) · `config/reglas-puntaje.md` (la carrera).*
