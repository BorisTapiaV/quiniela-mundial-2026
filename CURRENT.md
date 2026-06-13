# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-12 — Torneo EN VIVO (día 2). 5 jugadores, pozo $50.000. M1+M2 cargados. Cron auto-resultados andando solo. Sitio 2026-mundial.netlify.app. Git limpio (commit f271fb8). | Doc de estado vivo — el diseño/decisiones está en README.md, el detalle histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-12 — torneo EN VIVO (fase de grupos, día 2)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. No requiere intervención salvo cargar jugadores nuevos o arreglar pendientes.

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** privado `github.com/BorisTapiaV/quiniela-mundial-2026`
- **Último commit:** `f271fb8` (Auto: resultados nuevos 2026-06-12T04:08Z) · git limpio
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

## 📊 Resultados cargados

| Match | Partido | Marcador | Cómo |
|:-----:|---------|:--------:|------|
| M1 | México – Sudáfrica | 2-0 | manual 11-jun (tier gratis dio FINISHED sin score) |
| M2 | Corea del Sur – Chequia | 2-1 | auto |
| M3 | Canadá – Bosnia | — | hoy 12-jun 15:00 |
| M4 | Estados Unidos – Paraguay | — | hoy 12-jun 21:00 |

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
| Histórico completo del proyecto | memoria `project_quiniela_mundial_2026.md` |

---

*Última actualización: 2026-06-12 — torneo en vivo día 2, 5 jugadores, M1+M2 cargados, automatización andando sola.*
