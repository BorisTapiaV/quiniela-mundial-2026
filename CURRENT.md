# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-23 — Torneo EN VIVO (día 13). 5 jugadores, pozo $50.000. M1–M44 cargados (44/72). 🔥 CAMBIO DE LÍDER: Boris alcanzó a Carlos 82–82 y pasa al 🥇 por desempate (más exactos: Boris 9 – Carlos 7). La brecha que llevaba 12 días clavada en 5 se cerró en M41–M44 (Boris +12 vs Carlos +7, mejor jornada de La Casa, 3 exactos: ARG 2-0, FRA 3-0, JOR 1-2). M41–M44 entraron TODOS AUTOMÁTICO (cron sano; commits 02:16Z+05:11Z, copia local estaba atrás → git pull). M41 ARG 2-0 AUT, M42 FRA 3-0 IRQ, M43 NOR 3-2 SEN, M44 JOR 1-2 ALG. Hoy 23-jun: M45 Portugal-Uzbekistán (13:00), M46 Inglaterra-Ghana (16:00), M47 Panamá-Croacia (19:00), M48 Colombia-RD Congo (22:00). Sitio 2026-mundial.netlify.app. | Doc de estado vivo — diseño/decisiones en README.md, histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-23 — torneo EN VIVO (fase de grupos, día 13)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **44/72 partidos de grupos cargados.**

🔥 **CAMBIO DE LÍDER:** tras M41–M44, **Boris alcanzó a Carlos 82–82 y pasó al 🥇** por el desempate de **marcadores exactos (Boris 9 – Carlos 7)**. La brecha que llevaba 12 días clavada en 5 se cerró: en M41–M44 Boris sumó **+12** vs Carlos **+7** (mejor jornada de La Casa, 3 exactos: ARG 2-0, FRA 3-0, JOR 1-2).

✅ **M41–M44 entraron TODOS AUTOMÁTICO** (cron sano, commits 02:16Z + 05:11Z). La copia local estaba atrás → `git pull` la sincronizó (patrón ya conocido). Resultados: M41 Argentina 2-0 Austria, M42 Francia 3-0 Irak, M43 Noruega 3-2 Senegal, M44 Jordania 1-2 Argelia.

🗓️ **Hoy 23-jun se juegan 4** (Grupos H, E, F, F matchday 2): M45 Portugal–Uzbekistán (13:00), M46 Inglaterra–Ghana (16:00), M47 Panamá–Croacia (19:00), M48 Colombia–RD Congo (22:00). Vigilar que carguen solos; si algún partido "no actualiza el puntaje", casi siempre es el lag del plan gratis (status adelanta al score, caso M1/M31), no el cron → cargar a mano.

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** **PÚBLICO** `github.com/BorisTapiaV/quiniela-mundial-2026` (Actions ilimitado gratis)
- **Último commit:** `ee7c973` (Auto: 2026-06-23T05:11Z, M44) · sitio en vivo 44/72
- **Branding:** "Fisioterapia & Futbolito FC" (grupo WhatsApp 40+) — logo `site/fisio-fc.png`

---

## 👥 Jugadores (5) — pozo $50.000 (cuota $10k, reparto 50/30/20)

| Jugador | Slug | Campeón | Estado |
|---------|------|---------|--------|
| Boris Tapia V (La Casa) | `CASA` | España | ✅ completo (era privada, pública post-cierre) |
| Paulo Salas | `PAULO_SALAS` | España | ✅ completo |
| Carlos Salgado | `CARLOS_SALGADO` | Portugal | ✅ completo |
| Andrés Acosta (Colombia) | `ANDRES_ACOSTA` | Francia | ⚠️ M24 grupo en blanco + M83 KO inconsistente |
| Jorge Vásquez | `JORGE_VASQUEZ` | — | ⚠️ 72/72 grupos pero bracket KO vacío |

---

## 🏆 Tabla de posiciones (tras 44 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Vivo |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Boris Tapia V (La Casa)** | España | **82** | 9 | 🟢 |
| 🥈 | Carlos Salgado | Portugal | **82** | 7 | 🟢 |
| 🥉 | Andrés Acosta (Colombia) | Francia | 62 | 6 | 🟢 |
| 4 | Jorge Vásquez | — (sin campeón) | 62 | 5 | — |
| 5 | Paulo Salas | España | 55 | 6 | 🟢 |

**Mano a mano arriba:** **Boris 82 – Carlos 82** (empate en puntos). **Boris lidera por desempate** = más marcadores exactos (9 vs 7), 2º criterio del leaderboard (`config/reglas-puntaje.md`: pts → exactos → campeón → FIFA). Nota: Carlos acertó más ganadores (28 vs 26) pero Boris clavó más exactos. KO aún sin puntuar (se activa al completar los 72 de grupo). 3º/4º también empatan (Andrés/Jorge 62, Andrés arriba por exactos 6 vs 5). Haití = **primer eliminado** del torneo (especial, se puntúa al definirse).

---

## 📊 Resultados cargados (M1–M44)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
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
| 1 | **Hoy 23-jun: M45 Portugal–Uzbekistán (13:00), M46 Inglaterra–Ghana (16:00), M47 Panamá–Croacia (19:00), M48 Colombia–RD Congo (22:00)** — verificar que carguen solos; si el tier gratis demora, cargar manual | vigilar |
| 2 | **Jorge** completa bracket KO + campeón (hoy vacío; compite igual en grupos) | esperar jugador |
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

*Última actualización: 2026-06-23 — torneo en vivo día 13, 5 jugadores, M1–M44 cargados (44/72). 🔥 Boris 82 – Carlos 82: Boris pasa al 🥇 por desempate (exactos 9 vs 7); brecha de 5 cerrada en M41–M44 (Boris +12 vs Carlos +7). M41–M44 entraron TODOS AUTOMÁTICO (cron sano; git pull sincronizó copia local atrasada). Hoy 23-jun: M45/M46/M47/M48. Commit `ee7c973`, sitio en vivo 44/72.*
