# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-26 — Torneo EN VIVO (día 16). 5 jugadores, pozo $50.000. M1–M60 cargados (60/72). 🔥 BORIS ESTIRA EL 🥇 a +7: Boris 114 – Carlos 107. M55–M60 entraron TODOS AUTOMÁTICO (cron sano, 25-jun); en esa jornada Boris +13, Carlos +10. Boris sigue líder en los TRES criterios: pts (114-107), exactos (12-9) y ganadores (37-36). Resultados 25-jun: M55 CUW 0-2 CIV, M56 ECU 2-1 GER, M57 JPN 1-1 SWE, M58 TUN 1-3 NED, M59 TUR 3-2 USA, M60 PAR 0-0 AUS. Hoy 26-jun van M61–M66 (Noruega-Francia, Senegal-Irak, Cabo Verde-Arabia, Uruguay-España [campeón de Boris], Egipto-Irán, NZ-Bélgica) — aún sin jugar. Sitio 2026-mundial.netlify.app. | Anterior 2026-06-24 (día 14, 54/72): Jorge completó bracket KO+campeón (commit fc719fa); Boris 101 – Carlos 97 (+4), lidera tres criterios. | Doc de estado vivo — diseño/decisiones en README.md, histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-26 — torneo EN VIVO (fase de grupos, día 16)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **60/72 partidos de grupos cargados** — M55–M60 (25-jun) entraron solos.

🔥 **BORIS ESTIRA EL 🥇 a +7:** **Boris 114 – Carlos 107**. En la jornada del 25-jun (M55–M60) Boris sumó **+13** y Carlos **+10**, ampliando la brecha que venía en +4 (101-97 al M54). **Boris sigue líder en los tres criterios**: pts (114-107), exactos (**12 vs 9**) y ganadores (**37 vs 36**). El desempate del leaderboard es pts → exactos → campeón → FIFA.

✅ **M55–M60 entraron TODOS AUTOMÁTICO** (cron sano, 25-jun). La copia local estaba 3 commits atrás → `git pull` la sincronizó (patrón ya conocido). Resultados: M55 Curazao 0-2 Costa de Marfil, M56 Ecuador 2-1 Alemania, M57 Japón 1-1 Suecia, M58 Túnez 1-3 Países Bajos, M59 Turquía 3-2 EE.UU., M60 Paraguay 0-0 Australia.

⏳ **Hoy 26-jun van M61–M66** (aún sin jugar): Noruega-Francia · Senegal-Irak (15:00) · **Cabo Verde-Arabia · Uruguay-España [M64, campeón de Boris]** (20:00) · Egipto-Irán · NZ-Bélgica (23:00). Deberían cargar solos; si el tier gratis demora → `gh workflow run actualizar.yml`. Tras M66 quedará 66/72 (faltarían M67–M72 del 27-jun para cerrar grupos).

📋 **Jorge completó su bracket KO + campeón (Francia)** el 24-jun (commit `fc719fa`). Especiales opcionales sin llenar. **Pendiente #2 cerrado.**

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** **PÚBLICO** `github.com/BorisTapiaV/quiniela-mundial-2026` (Actions ilimitado gratis)
- **Último commit:** `e281eb7` (Auto: resultados nuevos, 2026-06-26T05:12Z) · sitio en vivo 60/72
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

<!-- AUTO:TABLA inicio — generado por build/refresh_dashboard.py, no editar a mano -->
## 🏆 Tabla de posiciones (tras 60 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Vivo |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Boris Tapia V (La Casa)** | España | **114** | 12 | 🟢 |
| 🥈 | **Carlos Salgado** | Portugal | **107** | 9 | 🟢 |
| 🥉 | Paulo Salas | España | 87 | 8 | 🟢 |
| 4 | Jorge Vásquez | Francia | 85 | 7 | 🟢 |
| 5 | Andrés Acosta (Colombia) | Francia | 82 | 6 | 🟢 |
<!-- AUTO:TABLA fin -->

**Mano a mano arriba:** **Boris 114 – Carlos 107** (Boris +7). En M55–M60 Boris sumó +13 y Carlos +10, ampliando el +4 que traía. **Boris lidera en los tres criterios**: pts, exactos (**12 vs 9**) y ganadores (**37 vs 36**) — desempate del leaderboard pts → exactos → campeón → FIFA (`config/reglas-puntaje.md`). **Paulo trepó al 3º** (87), Jorge 4º (85), Andrés 5º (82) — la pelea por el podio quedó apretada (87-85-82). KO aún sin puntuar (se activa al completar los 72 de grupo). Haití = **primer eliminado** del torneo (especial, se puntúa al definirse).

---

<!-- AUTO:RESULTADOS inicio — generado por build/refresh_dashboard.py, no editar a mano -->
## 📊 Resultados cargados (M1–M60)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
| M60 | Paraguay – Australia | 0-0 | 25-jun |
| M59 | Turquía – Estados Unidos | 3-2 | 25-jun |
| M58 | Túnez – Países Bajos | 1-3 | 25-jun |
| M57 | Japón – Suecia | 1-1 | 25-jun |
| M56 | Ecuador – Alemania | 2-1 | 25-jun |
| M55 | Curazao – Costa de Marfil | 0-2 | 25-jun |
| M54 | Sudáfrica – Corea del Sur | 1-0 | 24-jun |
| M53 | Chequia – México | 0-3 | 24-jun |
| M52 | Marruecos – Haití | 4-2 | 24-jun |
| M51 | Escocia – Brasil | 0-3 | 24-jun |
| M50 | Bosnia y Herzegovina – Catar | 3-1 | 24-jun |
| M49 | Suiza – Canadá | 2-1 | 24-jun |
| M48 | Colombia – RD Congo | 1-0 | 23-jun |
| M47 | Panamá – Croacia | 0-1 | 23-jun |
| M46 | Inglaterra – Ghana | 0-0 | 23-jun |
| M45 | Portugal – Uzbekistán | 5-0 | 23-jun |
| M44 | Jordania – Argelia | 1-2 | 22-jun |
| M43 | Noruega – Senegal | 3-2 | 22-jun |
| M42 | Francia – Irak | 3-0 | 22-jun |
| M41 | Argentina – Austria | 2-0 | 22-jun |
| M40 | Nueva Zelanda – Egipto | 1-3 | 21-jun |
| M39 | Uruguay – Cabo Verde | 2-2 | 21-jun |
| M38 | Bélgica – Irán | 0-0 | 21-jun |
| M37 | España – Arabia Saudita | 4-0 | 21-jun |

**M1–M36 (11-jun–21-jun):** MEX 2-0 RSA · KOR 2-1 CZE · CAN 1-1 BIH · USA 4-1 PAR · QAT 1-1 SUI · BRA 1-1 MAR · HAI 0-1 SCO · AUS 2-0 TUR · GER 7-1 CUW · NED 2-2 JPN · CIV 1-0 ECU · SWE 5-1 TUN · ESP 0-0 CPV · BEL 1-1 EGY · KSA 1-1 URU · IRN 2-2 NZL · FRA 3-1 SEN · IRQ 1-4 NOR · ARG 3-0 ALG · AUT 3-1 JOR · POR 1-1 COD · ENG 4-2 CRO · GHA 1-0 PAN · UZB 1-3 COL · CZE 1-1 RSA · SUI 4-1 BIH · CAN 6-0 QAT · MEX 1-0 KOR · USA 2-0 AUS · SCO 0-1 MAR · BRA 3-0 HAI · TUR 0-1 PAR · NED 5-1 SWE · GER 2-1 CIV · ECU 0-0 CUW · TUN 0-4 JPN.
<!-- AUTO:RESULTADOS fin -->

---

## 🔧 Pendientes abiertos

| # | Pendiente | Tipo |
|:-:|-----------|------|
| 1 | ✅ **25-jun completo: M55–M60 cargados automático** (60/72). **Hoy 26-jun:** M61–M66 — Noruega-Francia + Senegal-Irak (15:00), Cabo Verde-Arabia + **Uruguay-España [campeón de Boris]** (20:00), Egipto-Irán + NZ-Bélgica (23:00) — verificar que carguen solos; si el tier gratis demora, `gh workflow run actualizar.yml`. **27-jun:** M67–M72 cierran la fase de grupos (72/72) → se activa el puntaje KO | vigilar |
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
| **Refrescar tabla + resultados del dashboard (auto, desde datos)** | `python build/refresh_dashboard.py` (reescribe solo los bloques `<!-- AUTO:TABLA -->` y `<!-- AUTO:RESULTADOS -->`; `--check` = dry-run). La narrativa se escribe a mano |
| Histórico completo del proyecto | memoria `project_quiniela_mundial_2026.md` |

---

*Última actualización: 2026-06-26 — torneo en vivo día 16, 5 jugadores, M1–M60 cargados (60/72). 🔥 Boris 114 – Carlos 107: en la jornada del 25-jun (M55–M60) Boris sumó +13 y Carlos +10, ampliando la brecha de +4 a +7. Boris sigue líder en los tres criterios — pts (114-107), exactos (12-9) y ganadores (37-36). M55–M60 entraron todos automático (cron sano): M55 CUW 0-2 CIV, M56 ECU 2-1 GER, M57 JPN 1-1 SWE, M58 TUN 1-3 NED, M59 TUR 3-2 USA, M60 PAR 0-0 AUS. Copia local estaba 3 commits atrás → `git pull` la sincronizó. Hoy 26-jun van M61–M66 (incluye Uruguay-España, campeón de Boris); 27-jun cierran grupos con M67–M72. Sitio en vivo 60/72. **Herramienta nueva: `build/refresh_dashboard.py`** regenera tabla+resultados (bloques AUTO) desde los datos → al retomar: `git pull` → `python build/refresh_dashboard.py` → escribir solo la narrativa. **Fix `snapshot.py` `DENY=set()`** (Boris ya no se cae de la tabla; se reflejará en las páginas de jugador del sitio cuando el cron regenere al cargar los partidos de hoy).*
