# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-24 — Torneo EN VIVO (día 14). 5 jugadores, pozo $50.000. M1–M54 cargados (54/72) — Grupo A completo. 📋 JORGE COMPLETÓ su bracket KO + campeón Francia (planilla de eliminatorias ingestada 24-jun, commit fc719fa → pendiente #2 cerrado). 🔥 BORIS ESTIRA EL 🥇: tras la jornada completa, Boris 101 – Carlos 97 (+4). Boris lidera en los TRES criterios: pts (101-97), exactos (10-8) y ganadores (34-33). En M49–M54 Boris sumó +10, Carlos +5 (Carlos no puntuó en M53/M54). M45–M48 y M49–M54 entraron TODOS AUTOMÁTICO (cron sano). Resultados 24-jun: M49 SUI 2-1 CAN, M50 BIH 3-1 QAT, M51 SCO 0-3 BRA, M52 MAR 4-2 HAI, M53 CZE 0-3 MEX, M54 RSA 1-0 KOR. Recap predicciones 24-jun (6 partidos). Sitio 2026-mundial.netlify.app. | Anterior 2026-06-23 (día 13, 44/72): Boris alcanzó a Carlos 82–82 y lideró por desempate (exactos 9 vs 7); brecha de 5 cerrada en M41–M44 (Boris +12 vs Carlos +7). | Doc de estado vivo — diseño/decisiones en README.md, histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-24 — torneo EN VIVO (fase de grupos, día 14)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **54/72 partidos de grupos cargados** — los 6 de hoy (M49–M54) entraron automático; **Grupo A completo**.

📋 **Jorge completó su bracket KO + campeón (Francia)** — entregó la planilla de fase eliminatoria el 24-jun, ingestada con `build/ingest_plantilla.py` (KO 32/32 ✓ consistente con el motor; especiales opcionales sin llenar). Commit `fc719fa`, desplegada. **Cierra el pendiente #2.**

🔥 **BORIS ESTIRA EL 🥇:** tras la jornada completa de hoy, **Boris 101 – Carlos 97** (+4). Tras M45–M48 iban Carlos 92 – Boris 91 con Carlos arriba; Boris dio vuelta en M49–M52 (99-97) y con M53/M54 estiró a 101-97 (Carlos no puntuó en los dos últimos). Ahora **Boris lidera en los tres criterios**: pts (101-97), exactos (**10 vs 8**) y por primera vez ganadores (**34 vs 33**). El desempate del leaderboard es pts → exactos → campeón → FIFA.

✅ **M45–M48 entraron TODOS AUTOMÁTICO** (cron sano, commit `b813fe3` 05:09Z). La copia local estaba atrás → `git pull` la sincronizó (patrón ya conocido). Resultados: M45 Portugal 5-0 Uzbekistán, M46 Inglaterra 0-0 Ghana, M47 Panamá 0-1 Croacia, M48 Colombia 1-0 RD Congo.

✅ **24-jun (matchday 2): los 6 cargados automático** — M49 SUI 2-1 CAN, M50 BIH 3-1 QAT, M51 SCO 0-3 BRA, M52 MAR 4-2 HAI, M53 CZE 0-3 MEX, M54 RSA 1-0 KOR. **Grupo A completo.** M53/M54 entraron con el lag típico del tier gratis (terminaron 21:00, football-data publicó el score ~30 min después → un `workflow_dispatch` los empujó, commit `e284903` 03:11Z). **Recap predicciones 24-jun a 6** (`recap/predicciones-2026-06-24.html`, incluye M53/M54).

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** **PÚBLICO** `github.com/BorisTapiaV/quiniela-mundial-2026` (Actions ilimitado gratis)
- **Último commit:** `e284903` (Auto: M53/M54, 2026-06-25T03:11Z) sobre `c262fd5` (dashboard) · sitio en vivo 54/72
- **Branding:** "Fisioterapia & Futbolito FC" (grupo WhatsApp 40+) — logo `site/fisio-fc.png`

---

## 👥 Jugadores (5) — pozo $50.000 (cuota $10k, reparto 50/30/20)

| Jugador | Slug | Campeón | Estado |
|---------|------|---------|--------|
| Boris Tapia V (La Casa) | `CASA` | España | ✅ completo (era privada, pública post-cierre) |
| Paulo Salas | `PAULO_SALAS` | España | ✅ completo |
| Carlos Salgado | `CARLOS_SALGADO` | Portugal | ✅ completo |
| Andrés Acosta (Colombia) | `ANDRES_ACOSTA` | Francia | ⚠️ M24 grupo en blanco + M83 KO inconsistente |
| Jorge Vásquez | `JORGE_VASQUEZ` | Francia | ✅ completo (bracket KO + campeón ingestados 24-jun; especiales opcionales sin llenar) |

---

## 🏆 Tabla de posiciones (tras 54 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Vivo |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Boris Tapia V (La Casa)** | España | **101** | 10 | 🟢 |
| 🥈 | **Carlos Salgado** | Portugal | **97** | 8 | 🟢 |
| 🥉 | Jorge Vásquez | Francia | 80 | 7 | 🟢 |
| 4 | Andrés Acosta (Colombia) | Francia | 78 | 6 | 🟢 |
| 5 | Paulo Salas | España | 75 | 7 | 🟢 |

**Mano a mano arriba:** **Boris 101 – Carlos 97** (Boris +4). Boris dio vuelta el 🥇 en M49–M52 y lo estiró con M53/M54 (Carlos no puntuó en los dos últimos). Por primera vez **Boris lidera en los tres criterios**: pts, exactos (**10 vs 8**) y ganadores (**34 vs 33**) — desempate del leaderboard pts → exactos → campeón → FIFA (`config/reglas-puntaje.md`). **Jorge se afirma 3º** (80 pts), Andrés 4º (78), Paulo 5º (75). KO aún sin puntuar (se activa al completar los 72 de grupo). Haití = **primer eliminado** del torneo (especial, se puntúa al definirse).

---

## 📊 Resultados cargados (M1–M54)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
| M53 | Chequia – México | 0-3 | 24-jun (auto) |
| M54 | Sudáfrica – Corea del Sur | 1-0 | 24-jun (auto) |
| M49 | Suiza – Canadá | 2-1 | 24-jun (auto) |
| M50 | Bosnia – Catar | 3-1 | 24-jun (auto) |
| M51 | Escocia – Brasil | 0-3 | 24-jun (auto) |
| M52 | Marruecos – Haití | 4-2 | 24-jun (auto) |
| M45 | Portugal – Uzbekistán | 5-0 | 23-jun (auto) |
| M46 | Inglaterra – Ghana | 0-0 | 23-jun (auto) |
| M47 | Panamá – Croacia | 0-1 | 23-jun (auto) |
| M48 | Colombia – RD Congo | 1-0 | 23-jun (auto) |
| M41 | Argentina – Austria | 2-0 | 22-jun (auto) |
| M42 | Francia – Irak | 3-0 | 22-jun (auto) |
| M43 | Noruega – Senegal | 3-2 | 22-jun (auto) |
| M44 | Jordania – Argelia | 1-2 | 22-jun (auto) |
| M37 | España – Arabia Saudita | 4-0 | 21-jun (auto) |
| M38 | Bélgica – Irán | 0-0 | 21-jun (auto) |
| M39 | Uruguay – Cabo Verde | 2-2 | 21-jun (auto) |
| M40 | Nueva Zelanda – Egipto | 1-3 | 21-jun (auto) |
| M33 | Países Bajos – Suecia | 5-1 | 20-jun (auto) |
| M34 | Alemania – Costa de Marfil | 2-1 | 20-jun (auto) |
| M35 | Ecuador – Curazao | 0-0 | 20-jun (auto) |
| M36 | Túnez – Japón | 0-4 | 21-jun (auto) |
| M21 | Portugal – RD Congo | 1-1 | 17-jun |
| M22 | Inglaterra – Croacia | 4-2 | 17-jun |
| M23 | Ghana – Panamá | 1-0 | 17-jun |
| M24 | Uzbekistán – Colombia | 1-3 | 17-jun |
| M25 | Chequia – Sudáfrica | 1-1 | 18-jun |
| M26 | Suiza – Bosnia | 4-1 | 18-jun |
| M27 | Canadá – Catar | 6-0 | 18-jun |
| M28 | México – Corea del Sur | 1-0 | 18-jun |
| M29 | Estados Unidos – Australia | 2-0 | 19-jun |
| M30 | Escocia – Marruecos | 0-1 | 19-jun |
| M31 | Brasil – Haití | 3-0 | 19-jun (manual) |
| M32 | Turquía – Paraguay | 0-1 | 19-jun (auto) |

**M1–M20 (11–17 jun):** MEX 2-0 RSA · KOR 2-1 CZE · CAN 1-1 BIH · USA 4-1 PAR · QAT 1-1 SUI · BRA 1-1 MAR · HAI 0-1 SCO · AUS 2-0 TUR · GER 7-1 CUW · NED 2-2 JPN · CIV 1-0 ECU · SWE 5-1 TUN · ESP 0-0 CPV · BEL 1-1 EGY · KSA 1-1 URU · IRN 2-2 NZL · FRA 3-1 SEN · IRQ 1-4 NOR · ARG 3-0 ALG · AUT 3-1 JOR.

---

## 🔧 Pendientes abiertos

| # | Pendiente | Tipo |
|:-:|-----------|------|
| 1 | ✅ **24-jun completo: M49–M54 cargados** (Grupo A cerrado, 54/72). **Próxima fecha 25-jun:** M55–M60 — Curazao-Costa de Marfil + Ecuador-Alemania (16:00), Japón-Suecia + Túnez-Países Bajos (19:00), Turquía-EE.UU. + Paraguay-Australia (22:00) — verificar que carguen solos; si el tier gratis demora, `gh workflow run actualizar.yml` | vigilar |
| 2 | ✅ **RESUELTO 24-jun** — Jorge entregó planilla de eliminatorias: bracket KO 32/32 + campeón Francia ingestados (commit `fc719fa`). Solo faltan especiales opcionales | hecho |
| 3 | **Andrés** — M24 grupo en blanco + M83 KO inconsistente (llave deriva UZB-CRO, eligió Colombia) | esperar/arreglar |
| 4 | Recap tarjeta WhatsApp compartible (se genera **local**, no en CI) | opcional |
| 5 | `og.png` con logo FC | opcional cosmético |
| 6 | Más planillas que lleguen al pool | esperar |

---

## ⚙️ Datos operativos (deploy + automatización)

- **Netlify:** site id `3ca883c4-5ee1-4606-9062-2922a1810df9` · cuenta `boris.tapia@veridia.green` · plan Free (reinicia 11-jul)
- **Deploy:** 100% por CLI (`netlify deploy --dir=site --prod --site <id> --auth $NETLIFY_TOKEN`). **NO Git-auto.** Vía preferida: `gh workflow run actualizar.yml` (usa los Secrets correctos + fuerza deploy).
- ⚠️ **Gotcha:** el sitio Netlify quedó conectado por error al repo `album-mundial-2026` → `stop_builds:true` vía API para que el álbum no lo pise.
- **Cron:** `.github/workflows/actualizar.yml` — cada 15 min SOLO en ventana de partidos (`*/15 18-23` + `*/15 0-6` UTC = 14:00–02:00 Chile), **deploy-on-change** (solo si entra resultado nuevo) o forzado por `workflow_dispatch`. **Los schedules de GitHub se atrasan/saltan** → si urge, disparar manual.
- ✅ **Repo PÚBLICO (desde 18-jun) = GitHub Actions ilimitado gratis.** Antes privado → 2000 min/mes (compartidos a nivel de cuenta); correr cada 15 min los agotó y mató el cron 17-jun. Público no consume esa bolsa.
- **3 GitHub Secrets:** `FOOTBALL_DATA_TOKEN` + `NETLIFY_AUTH_TOKEN` + `NETLIFY_SITE_ID`. Nunca en archivos — siguen ocultos aunque el repo sea público.
- **Tier gratis football-data:** cubre todo el WC (1 llamada/run), puntúa con resultado FINAL. **NO** da live; el status puede ir por delante del score → caso M1/M31 (fetch ignora FINISHED-sin-marcador) → carga manual cuando demora.
- **Cargar un partido a mano:** editar `data/resultados.csv` (cols `gl,gv` de la fila `match_no`) → `python build/gen_galeria.py && python build/gen_jugador.py && python build/gen_calendar.py` → commit + push → `gh workflow run actualizar.yml`.

---

## 🗂️ Puntos de entrada

| Necesito | Archivo |
|----------|---------|
| Diseño + decisiones + estructura | `README.md` |
| Modelo de puntaje + "la carrera" | `config/reglas-puntaje.md` |
| Reglamento FIFA modularizado (Art 11-14) | `reglas/INDEX.md` |
| Motor (posiciones, 8 terceros, R32 vía 495, KO, scoring) | `build/engine.py` |
| Ingesta de planillas nuevas | `build/ingest_plantilla.py` |
| Fetch resultados + cron | `build/fetch_resultados.py` · `.github/workflows/actualizar.yml` |
| Predicciones por jugador | `data/predicciones/<SLUG>.csv` (+`_ko`, +`_especiales`) |
| Resultados | `data/resultados.csv` · `data/resultados_ko.csv` · `data/resultados_especiales.csv` |
| Visiones live + wow pendientes | `docs/EXPERIENCIA_EN_VIVO_Y_WOW.md` |
| Recap predicciones compartible (no deploya, screenshot local) | `recap/predicciones-AAAA-MM-DD.html` (+`_TEMPLATE.html` · `README.md`) |
| Histórico completo del proyecto | memoria `project_quiniela_mundial_2026.md` |

---

*Última actualización: 2026-06-24 — torneo en vivo día 14, 5 jugadores, M1–M54 cargados (54/72, Grupo A completo). 📋 Jorge completó su bracket KO + campeón (Francia): planilla de eliminatorias ingestada (`build/ingest_plantilla.py`, KO 32/32 ✓ motor), commit `fc719fa`, desplegada → cierra pendiente #2. 🔥 Boris 101 – Carlos 97: Boris dio vuelta el 🥇 en M49–M52 y lo estiró con M53/M54 (Carlos no puntuó); ahora lidera en los tres criterios — pts (101-97), exactos (10-8) y ganadores (34-33). Los 6 de hoy automático: M49 SUI 2-1 CAN, M50 BIH 3-1 QAT, M51 SCO 0-3 BRA, M52 MAR 4-2 HAI, M53 CZE 0-3 MEX, M54 RSA 1-0 KOR (M53/M54 con lag tier gratis, empujados por workflow_dispatch → commit `e284903`). Sitio en vivo 54/72.*
