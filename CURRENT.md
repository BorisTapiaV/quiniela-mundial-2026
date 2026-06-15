# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-15 — Torneo EN VIVO (día 5). 5 jugadores, pozo $50.000. M1–M12 cargados (cron auto, sin intervención). La Casa 1º con 27 pts, pero Carlos cerró a 24 (la ventaja pasó de 10 a 3 pts). Sitio 2026-mundial.netlify.app. Local sincronizado a origin/main (commit 3f71456). Recap predicciones 15-jun generado (recap/predicciones-2026-06-15.html). | Doc de estado vivo — el diseño/decisiones está en README.md, el detalle histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-15 — torneo EN VIVO (fase de grupos, día 5)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. No requiere intervención salvo cargar jugadores nuevos o arreglar pendientes. **12/72 partidos de grupos cargados** sin tocar nada (commits auto hasta el 15-jun). **Hoy 15-jun se juegan M13–M16** (ESP-CPV, BEL-EGY, KSA-URU, IRN-NZL).

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** privado `github.com/BorisTapiaV/quiniela-mundial-2026`
- **Último commit:** `3f71456` (Auto: resultados nuevos 2026-06-15T04:08Z) · local sincronizado a origin/main
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

## 🏆 Tabla de posiciones (tras 12 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Δ desde M9 |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Boris Tapia V (La Casa)** | España | **27** | 4 | +0 |
| 🥈 | Carlos Salgado | Portugal | **24** | 3 | **+7** |
| 🥉 | Andrés Acosta (Colombia) | Francia | 18 | 2 | +5 |
| 4 | Jorge Vásquez | — (sin campeón) | 14 | 1 | +0 |
| 5 | Paulo Salas | España | 9 | 1 | +0 |

La Casa sigue 1º pero **la ventaja se achicó de 27-17 (10 pts) a 27-24 (3 pts)**: los 3 partidos nuevos (M10 NED 2-2 JPN · M11 CIV 1-0 ECU · M12 SWE 5-1 TUN) le dieron **+7 a Carlos** y **+5 a Andrés**, y **0 a La Casa**. KO aún sin puntuar (faltan grupos).

---

## 📊 Resultados cargados (M1–M12)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
| M1 | México – Sudáfrica | 2-0 | 11-jun (manual; tier gratis dio FINISHED sin score) |
| M2 | Corea del Sur – Chequia | 2-1 | 11-jun (auto) |
| M3 | Canadá – Bosnia | 1-1 | 12-jun |
| M4 | Estados Unidos – Paraguay | 4-1 | 12-jun |
| M5 | Catar – Suiza | 1-1 | 13-jun |
| M6 | Brasil – Marruecos | 1-1 | 13-jun |
| M7 | Haití – Escocia | 0-1 | 13-jun |
| M8 | Australia – Turquía | 2-0 | 14-jun |
| M9 | Alemania – Curazao | 7-1 | 14-jun |
| M10 | Países Bajos – Japón | 2-2 | 14-jun |
| M11 | Costa de Marfil – Ecuador | 1-0 | 14-jun |
| M12 | Suecia – Túnez | 5-1 | 14-jun |

**Scoring M1 verificado:** Carlos + La Casa 5 (exacto 2-0) · Andrés 3 (dif +2) · Jorge + Paulo 2 (1X2).

---

## 🔧 Pendientes abiertos

| # | Pendiente | Tipo |
|:-:|-----------|------|
| 1 | **Jorge** completa bracket KO + campeón (hoy vacío; compite igual en grupos) | esperar jugador |
| 2 | **Andrés** — M24 grupo en blanco + M83 KO inconsistente (llave deriva UZB-CRO, eligió Colombia) | esperar/arreglar |
| 3 | Recap tarjeta WhatsApp compartible (se genera **local**, no en CI) | opcional |
| 4 | `og.png` con logo FC | opcional cosmético |
| 5 | Más planillas que lleguen al pool | esperar |

---

## ⚙️ Datos operativos (deploy + automatización)

- **Netlify:** site id `3ca883c4-5ee1-4606-9062-2922a1810df9` · cuenta `boris.tapia@veridia.green` · plan Free (reinicia 11-jul)
- **Deploy:** 100% por CLI (`netlify deploy --dir=site --prod --site <id> --auth $NETLIFY_TOKEN`). **NO Git-auto.**
- ⚠️ **Gotcha:** el sitio Netlify quedó conectado por error al repo `album-mundial-2026` → `stop_builds:true` vía API para que el álbum no lo pise.
- **Cron:** `.github/workflows/actualizar.yml` — cada 15 min SOLO en ventana de partidos (`*/15 18-23` + `*/15 0-6` UTC = 14:00–02:00 Chile), **deploy-on-change** (solo si entra resultado nuevo). Ahorra créditos.
- **3 GitHub Secrets:** `FOOTBALL_DATA_TOKEN` + `NETLIFY_AUTH_TOKEN` + `NETLIFY_SITE_ID`. Nunca en archivos.
- **Tier gratis football-data:** cubre todo el WC (1 llamada/run), puntúa con resultado FINAL. **NO** da live minuto-a-minuto; status puede ir por delante del score (de ahí el caso M1 → fetch ignora FINISHED-sin-marcador).

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

*Última actualización: 2026-06-15 — torneo en vivo día 5, 5 jugadores, M1–M12 cargados (cron auto). La Casa 1º con 27 pts pero Carlos cerró a 24 (ventaja 10→3). Recap predicciones 15-jun generado. Local sincronizado a origin/main (commit 3f71456).*
