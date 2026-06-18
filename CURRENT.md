# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-18 — Torneo EN VIVO (día 8). 5 jugadores, pozo $50.000. M1–M24 cargados. VUELCO: Carlos pasó a La Casa, 42-41 (venía 37-35 abajo, remató en M21–M24). FIX OPERATIVO: el cron murió 17-jun 20:00Z por presupuesto agotado de GitHub Actions (repo privado, 2000 min/mes gratis consumidos) → M21–M24 no cargaron + sitio congelado en M20. Solución: repo hecho PÚBLICO (Actions ilimitado gratis, $0, ya no quema budget); cron disparado a mano, cargó M21–M24 + deployó. Snapshot MD2 (día 8) cerrado. Sitio 2026-mundial.netlify.app. | Doc de estado vivo — el diseño/decisiones está en README.md, el detalle histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-18 — torneo EN VIVO (fase de grupos, día 8)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **24/72 partidos de grupos cargados.**

⚠️ **Falla resuelta (18-jun):** el cron murió el **17-jun 20:00Z** porque se agotó el **presupuesto de GitHub Actions** (el repo era privado → solo 2000 min/mes gratis, consumidos por correr cada 15 min). Toda corrida moría al instante con *"Actions budget is preventing further use"* → **M21–M24 no cargaron y el sitio quedó congelado en M20**. **Solución aplicada:** el repo se hizo **PÚBLICO** (repos públicos = Actions ilimitado gratis, $0, no toca el budget de la cuenta; verificado que no hay secretos en el código — los tokens viven en GitHub Secrets, siguen ocultos). Cron disparado a mano → cargó M21–M24 + deployó. **El automático vuelve a correr gratis para siempre.**

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** **PÚBLICO** (desde 18-jun) `github.com/BorisTapiaV/quiniela-mundial-2026`
- **Último commit:** `af6667a` (Auto: resultados nuevos 2026-06-18T11:25Z) · local sincronizado a origin/main
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

## 🏆 Tabla de posiciones (tras 25 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Ganador |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Carlos Salgado** | Portugal | **47** | 6 | 14/25 |
| 🥈 | Boris Tapia V (La Casa) | España | **46** | 5 | 14/25 |
| 🥉 | Andrés Acosta (Colombia) | Francia | 31 | 3 | 9/25 |
| 4 | Jorge Vásquez | — (sin campeón) | 25 | 1 | 10/25 |
| 5 | Paulo Salas | España | 18 | 1 | 7/25 |

**VUELCO en la punta:** La Casa venía 1º (37-35 el 15-jun) pero Carlos remató fuerte en M21–M24 y pasó al frente. Tras M25 (CZE 1-1 RSA, ambos exacto +5) sigue **Carlos 47 – Boris 46, a 1 punto**. Empate en ganador (14-14); Carlos arriba en exactos (6-5). Mano a mano. KO aún sin puntuar. Faltan M26–M28 (18-jun) por entrar.

---

## 📊 Resultados cargados (M1–M24)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
| M13 | España – Cabo Verde | 0-0 | 15-jun |
| M14 | Bélgica – Egipto | 1-1 | 15-jun |
| M15 | Arabia Saudita – Uruguay | 1-1 | 15-jun |
| M16 | Irán – Nueva Zelanda | 2-2 | 15-jun |
| M17 | Francia – Senegal | 3-1 | 16-jun |
| M18 | Irak – Noruega | 1-4 | 16-jun |
| M19 | Argentina – Argelia | 3-0 | 16-jun |
| M20 | Austria – Jordania | 3-1 | 17-jun |
| M21 | Portugal – RD Congo | 1-1 | 17-jun |
| M22 | Inglaterra – Croacia | 4-2 | 17-jun |
| M23 | Ghana – Panamá | 1-0 | 17-jun |
| M24 | Uzbekistán – Colombia | 1-3 | 17-jun |
| M25 | Chequia – Sudáfrica | 1-1 | 18-jun |

**M1–M12 (11–14 jun):** México 2-0 RSA · KOR 2-1 CZE · CAN 1-1 BIH · USA 4-1 PAR · QAT 1-1 SUI · BRA 1-1 MAR · HAI 0-1 SCO · AUS 2-0 TUR · GER 7-1 CUW · NED 2-2 JPN · CIV 1-0 ECU · SWE 5-1 TUN.

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
- ✅ **Repo PÚBLICO (desde 18-jun) = GitHub Actions ilimitado gratis.** Antes era privado → solo 2000 min/mes; correr cada 15 min los agotó y el cron murió 17-jun 20:00Z (*"Actions budget is preventing further use"*), congelando M21–M24. El budget de Actions es **a nivel de cuenta** (compartido por todos los repos privados), no por repo; un repo público no consume nada de esa bolsa. Por eso se hizo público solo este repo. Disparo manual: `gh workflow run actualizar.yml`.
- **3 GitHub Secrets:** `FOOTBALL_DATA_TOKEN` + `NETLIFY_AUTH_TOKEN` + `NETLIFY_SITE_ID`. Nunca en archivos — siguen ocultos aunque el repo sea público (no se exponen al hacer público el repo).
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

*Última actualización: 2026-06-18 — torneo en vivo día 8, 5 jugadores, M1–M25 cargados. VUELCO: Carlos pasó a La Casa, 47-46 tras M25. Falla del cron por presupuesto de Actions agotado (repo privado) → resuelta haciendo el repo PÚBLICO (Actions gratis ilimitado); M21–M25 cargados + deploy. Snapshot MD2 cerrado. Recap predicciones 18-jun generado (recap/predicciones-2026-06-18.html). Faltan M26–M28 (entran solos por el cron). Local sincronizado a origin/main.*
