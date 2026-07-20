# 🕐 ARRANQUE 2030 — cómo re-correr esto en 4 años

> **Este es el ÚNICO documento que hay que leer para arrancar el Mundial 2030.** No re-leas los archivos dispersos: acá está el método destilado y los punteros. Profundiza en un artefacto solo si el paso lo pide.
> Escrito 2026-07-19, al cerrar el Mundial 2026 (Boris campeón de su propia quiniela). Próximo Mundial: 2030 (España-Portugal-Marruecos + 3 sudamericanos, formato aún por confirmar por FIFA).

---

## 0. Qué es esto (30 segundos)

Dos piezas que ya funcionaron en 2026:

1. **El motor de la quiniela** — visor HTML estático (Netlify) generado desde CSVs versionados; cron de GitHub Actions hace fetch de resultados → deploy-on-change. Modelo "bracket challenge": cada jugador pronostica todo antes de empezar y la gracia es ver *la carrera*. **~85-90% se reusa**; solo cambian datos.
2. **El experimento de pronóstico ("La Casa")** — la planilla de Boris NO es corazonada: la genera un pipeline de Deep Research + validación de consenso. En 2026 **ganó el pool (+75)** y acertó 11/12 grupos · 4/4 semis · 2/2 finalistas · campeón · goleador. El método ya está refinado (§3).

---

## 1. Lo que se REUSA vs lo que CAMBIA

| ♻️ Se reusa tal cual | 🔄 Cambia (datos, no código) |
|---|---|
| `build/engine.py` (standings, terceros, bracket, scoring) | `data/equipos.csv` — las 48 selecciones 2030 + grupo + FIFA rank + pos |
| Todos los `build/gen_*.py` (portada, jugador, calendario, tarjeta, recap, diplomas) | `data/fixture.csv` — 104 partidos (fechas/sedes/cruces) → regenerar con `build/bootstrap_fixture.py` |
| `build/refresh_dashboard.py`, `build/snapshot.py` | `data/terceros_495.csv` — bracket FIFA de mejores terceros → `build/bootstrap_terceros.py` |
| Cron `.github/workflows/actualizar.yml` (deploy-on-change) | `data/predicciones/<JUGADOR>*.csv` — planillas nuevas (`.csv` grupos, `_ko.csv`, `_especiales.csv`) |
| Mecánica de scoring `config/reglas-puntaje.md` | Fuente de resultados + token (football-data.org tier gratis, o lo que exista en 2030) |
| **Los 6 refinamientos del predict** (§3) | Netlify site id + 3 GitHub Secrets nuevos |
| Correcciones acumuladas (§5 gotchas) | |

---

## 2. Checklist de arranque 2030

```
[ ] equipos.csv: 48 selecciones 2030 (código, nombre, grupo A-L, FIFA rank, pos de bombo)
[ ] fixture.csv: python build/bootstrap_fixture.py  →  RE-VERIFICAR sedes/horas/número FIFA 2030
[ ] terceros_495.csv: python build/bootstrap_terceros.py
    ⚠️ CRÍTICO: FIFA puede cambiar la asignación 3º→slot, y el FORMATO 2030 podría no ser 48
       equipos / 12 grupos. Si cambia el formato, esta tabla y build_r32 se rehacen. Verificar
       el reglamento FIFA 2030 (Annexe C equivalente) ANTES de confiar en el bracket.
[ ] predicciones/: una planilla por jugador (grupos + _ko + _especiales). CASA = La Casa (§3)
[ ] API/token: 3 GitHub Secrets (FOOTBALL_DATA_TOKEN + NETLIFY_AUTH_TOKEN + NETLIFY_SITE_ID)
[ ] Netlify: crear site nuevo, repo PÚBLICO (Actions ilimitado — clave, ver §5)
[ ] Smoke test: python build/actualizar.py  →  revisar site/index.html local antes de deployar
```

---

## 3. El experimento de pronóstico — MÉTODO REFINADO (pipeline de 2 etapas)

> Esto es lo que en 2026 hicimos ad-hoc y ahora está destilado con los 6 refinamientos ya incorporados. **No hace falta re-leer la retrospectiva** — está todo acá. (Detalle y evidencia: `referencias/RETROSPECTIVA_EXPERIMENTO_PRONOSTICO_2026-07.md`.)

**Etapa A — Consenso PRIMERO (barato, alto acierto) → binarios de cabeza.**
Cruzar apuestas (bet365/DraftKings/FanDuel/Kalshi) + simuladores (Opta/PELE/sucesor) + expertos.
De acá salen directo: **campeón, finalistas, ganadores de grupo.** En 2026 esto solo ya daba casi todo gratis. *(R4, R5)*

**Etapa B — Scouting profundo (workflow ~61 agentes, prompt Leonor) → SOLO marcadores.**
Rúbrica de fuerza 0-100 + GF/GC por selección. **Su valor único son los marcadores exactos** (los 13/72 que ganaron el pozo en 2026); el mercado da "quién gana", no "2-1". No lo gastes en los binarios que la Etapa A ya resolvió. *(R4)*

**🚪 Gate de recalibración — el paso que ganó 2026.** *(R1, R6)*
En el vértice del bracket, si el top de fuerza está en **cuasi-empate (Δ ≤ ~3 pts)**, el modelo NO tiene poder resolutivo → **usa el #1 del consenso** para campeón/finalistas. En 2026 la rúbrica daba Francia 95 = Argentina 95 = España 94 (irresoluble); el consenso marcó España; Boris envió España + mantuvo Argentina → clavó la final exacta. Decide **binario por binario** y documenta la decisión (mismo instinto que el loop de calibración de Profiler: reference class + consenso + Brier).

**Ajustes finos:**
- **R2 — descuento por bandera cualitativa:** si la nota de scouting de una selección dice *dependencia de estrella + fragilidad defensiva + "se queda corto"*, bájala a mano. En 2026 esa bandera era Portugal — el único fallo de grupo y encima eliminado temprano.
- **R3 — no apostar la cola:** "primer eliminado" y "sorpresa" entre minnows no tienen señal (Cabo Verde, el "primer eliminado" predicho, terminó 2º y avanzó). Mantenerlos retirados del scoring.
- **R5 — estrategia de pool:** en un pool de humanos casuales, **alinear con el consenso gana**; diferenciarse solo paga con edge real (a N=1, el único edge demostrado fue la granularidad de los marcadores).

> ⚠️ **Todo esto es N=1** (un solo Mundial). Son la mejor hipótesis disponible, no leyes. La amplitud de aciertos de 2026 (11/12 grupos + 4/4 semis + 2/2 finalistas) es lo que da confianza en el método estructural; la Etapa A + el gate son lo replicable.

---

## 4. Punteros a los artefactos (profundizar solo si hace falta)

| Necesito | Archivo |
|---|---|
| Estado/dashboard del torneo | `CURRENT.md` |
| Diseño, mecánica, pipeline | `README.md` · `docs/ARQUITECTURA.md` |
| Modelo de puntaje | `config/reglas-puntaje.md` |
| **El pronóstico 2026 (referencia de formato)** | `referencias/scouting-48-pronostico-casa.md` (48 perfiles + tabla de fuerza) |
| **La validación de consenso 2026** | `referencias/validacion-consenso.md` |
| **La retrospectiva + los 6 refinamientos con evidencia** | `referencias/RETROSPECTIVA_EXPERIMENTO_PRONOSTICO_2026-07.md` |
| **Recomputar el scorecard predicho-vs-real** | `python build/retro_experimento.py` |
| Diseño de la mecánica (robado de 3 Excels) | `referencias/analisis-3-modelos.md` |
| Mecánicas de enganche/retención (DR) | `docs/ENGANCHE_DEEP_RESEARCH.md` · `docs/IDEAS_DEEP_RESEARCH.md` |
| Motor de bracket y scoring | `build/engine.py` |

---

## 5. Gotchas operativos durables (esto costó horas en 2026 — no repetir)

- **KO por penales → `winner:null` en el tier gratis.** football-data lo da `FINISHED` sin ganador (log: `KO: N terminados · N-1 mapeados`). NO es bug: buscar el resultado en la web y cargar a mano en `data/resultados_ko.csv` (el fetch **fusiona**, no borra la carga manual).
- **NO deployar a cada cambio** — gasta el cupo Netlify. Batchear o `gh workflow run actualizar.yml` una vez. `recap/` y `diplomas/` NO deployan (viven fuera de `site/`).
- **Cron falla en 4-6s con conclusión `failure`** = bloqueo de facturación de la cuenta GitHub, NO código ni API. Revisar billing primero.
- **flagcdn solo acepta w20/w40/w80/w160/w320** — `w30` da 404 (banderas invisibles).
- **Render HTML→PNG: Edge `--headless` (viejo), NO `--headless=new`** (este último falla siempre).
- **Repo PÚBLICO = GitHub Actions ilimitado gratis.** Privado agota 2000 min/mes corriendo cada 15 min y mata el cron.
- **El especial de goleador es CARGA MANUAL** (`data/resultados_especiales.csv`) — el campeón sí se deriva solo del bracket.

---

*Punto de entrada único para 2030. Mantener este archivo como el "léeme primero"; si algo cambia estructuralmente (formato FIFA, fuente de datos), actualizar acá, no en un archivo nuevo.*
*Cierre Mundial 2026 · 2026-07-19 · 0 voseo.*
