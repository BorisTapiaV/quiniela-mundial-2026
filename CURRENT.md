# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-27 — Torneo EN VIVO (día 17). 5 jugadores, pozo $50.000. M1–M66 cargados (66/72). 🔥 BORIS DISPARA EL 🥇 a +21: Boris 131 – Carlos 110. M61–M66 entraron TODOS AUTOMÁTICO (cron sano, 26-jun); jornadón de Boris +17 vs Carlos +3. Boris sigue líder en los TRES criterios: pts (131-110), exactos (13-9) y ganadores (43-37). Resultados 26-jun: M61 NOR 1-4 FRA, M62 SEN 5-0 IRQ, M63 CPV 0-0 KSA, M64 URU 0-1 ESP [campeón de Boris ✅], M65 EGY 1-1 IRN, M66 NZL 1-5 BEL. Hoy 27-jun van M67–M72 (Panamá-Inglaterra, Croacia-Ghana, Colombia-Portugal, RD Congo-Uzbekistán, Argelia-Austria, Jordania-Argentina) — cierran fase de grupos → se activa puntaje KO. Sitio 2026-mundial.netlify.app. **FEATURES 27-jun (commits `618c6c9`+`a586995`):** (1) cruces R32 resueltos en calendario + ticker; (2) **"🏆 Cuadro del torneo"** real en la portada (`engine.bracket_partial`, se llena solo: 5 cruces ya formados + placeholders; eliminados en gris, campeón dorado); (3) **archivo plegable "Fase de grupos — cerrada"** (12 tablas finales, aparece al llegar a 72/72); (4) **tarjeta WhatsApp con escudo FC** (logo base64); (5) evolución del ranking ya operativa. Todo se autocompleta esta noche al cerrar grupos. | Anterior 2026-06-26 (día 16, 60/72): Boris 114 – Carlos 107 (+7), lidera tres criterios. | Doc de estado vivo — diseño/decisiones en README.md, histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-27 — torneo EN VIVO (fase de grupos, día 17)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **66/72 partidos de grupos cargados** — M61–M66 (26-jun) entraron solos.

🔥 **BORIS DISPARA EL 🥇 a +21:** **Boris 131 – Carlos 110**. En la jornada del 26-jun (M61–M66) Boris sumó **+17** y Carlos solo **+3**, ampliando la brecha que venía en +7 (114-107 al M60). **Boris sigue líder en los tres criterios**: pts (131-110), exactos (**13 vs 9**) y ganadores (**43 vs 37**). El desempate del leaderboard es pts → exactos → campeón → FIFA.

✅ **M61–M66 entraron TODOS AUTOMÁTICO** (cron sano, 26-jun). La copia local estaba 5 commits atrás → `git pull` la sincronizó (patrón ya conocido). Resultados: M61 Noruega 1-4 Francia, M62 Senegal 5-0 Irak, M63 Cabo Verde 0-0 Arabia Saudita, **M64 Uruguay 0-1 España [campeón de Boris ✅]**, M65 Egipto 1-1 Irán, M66 Nueva Zelanda 1-5 Bélgica.

⏳ **Hoy 27-jun van M67–M72** (aún sin jugar, cierran la fase de grupos): Panamá-Inglaterra · Croacia-Ghana (17:00) · Colombia-Portugal · RD Congo-Uzbekistán (19:30) · Argelia-Austria · Jordania-Argentina (22:00). Deberían cargar solos; si el tier gratis demora → `gh workflow run actualizar.yml`. **Tras M72 (72/72) se activa el puntaje KO** (avance por fase + especiales).

📋 **Jorge completó su bracket KO + campeón (Francia)** el 24-jun (commit `fc719fa`). Especiales opcionales sin llenar. **Pendiente #2 cerrado.**

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** **PÚBLICO** `github.com/BorisTapiaV/quiniela-mundial-2026` (Actions ilimitado gratis)
- **Último commit:** `47320f9` (Auto: resultados nuevos, 2026-06-27T06:23Z) · sitio en vivo 66/72
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
## 🏆 Tabla de posiciones (tras 66 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Vivo |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Boris Tapia V (La Casa)** | España | **131** | 13 | 🟢 |
| 🥈 | **Carlos Salgado** | Portugal | **110** | 9 | 🟢 |
| 🥉 | Paulo Salas | España | 102 | 9 | 🟢 |
| 4 | Andrés Acosta (Colombia) | Francia | 92 | 6 | 🟢 |
| 5 | Jorge Vásquez | Francia | 91 | 7 | 🟢 |
<!-- AUTO:TABLA fin -->

**Mano a mano arriba:** **Boris 131 – Carlos 110** (Boris +21). En M61–M66 Boris sumó +17 y Carlos solo +3, disparando el +7 que traía. **Boris lidera en los tres criterios**: pts, exactos (**13 vs 9**) y ganadores (**43 vs 37**) — desempate del leaderboard pts → exactos → campeón → FIFA (`config/reglas-puntaje.md`). **Paulo se afirmó 3º** (102, 9 exactos), Andrés 4º (92), Jorge 5º (91) — el podio se despegó pero 4º-5º van pegados (92-91). KO aún sin puntuar (se activa al completar los 72 de grupo). Haití = **primer eliminado** del torneo (especial, se puntúa al definirse).

---

<!-- AUTO:RESULTADOS inicio — generado por build/refresh_dashboard.py, no editar a mano -->
## 📊 Resultados cargados (M1–M66)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
| M66 | Nueva Zelanda – Bélgica | 1-5 | 26-jun |
| M65 | Egipto – Irán | 1-1 | 26-jun |
| M64 | Uruguay – España | 0-1 | 26-jun |
| M63 | Cabo Verde – Arabia Saudita | 0-0 | 26-jun |
| M62 | Senegal – Irak | 5-0 | 26-jun |
| M61 | Noruega – Francia | 1-4 | 26-jun |
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

**M1–M42 (11-jun–22-jun):** MEX 2-0 RSA · KOR 2-1 CZE · CAN 1-1 BIH · USA 4-1 PAR · QAT 1-1 SUI · BRA 1-1 MAR · HAI 0-1 SCO · AUS 2-0 TUR · GER 7-1 CUW · NED 2-2 JPN · CIV 1-0 ECU · SWE 5-1 TUN · ESP 0-0 CPV · BEL 1-1 EGY · KSA 1-1 URU · IRN 2-2 NZL · FRA 3-1 SEN · IRQ 1-4 NOR · ARG 3-0 ALG · AUT 3-1 JOR · POR 1-1 COD · ENG 4-2 CRO · GHA 1-0 PAN · UZB 1-3 COL · CZE 1-1 RSA · SUI 4-1 BIH · CAN 6-0 QAT · MEX 1-0 KOR · USA 2-0 AUS · SCO 0-1 MAR · BRA 3-0 HAI · TUR 0-1 PAR · NED 5-1 SWE · GER 2-1 CIV · ECU 0-0 CUW · TUN 0-4 JPN · ESP 4-0 KSA · BEL 0-0 IRN · URU 2-2 CPV · NZL 1-3 EGY · ARG 2-0 AUT · FRA 3-0 IRQ.
<!-- AUTO:RESULTADOS fin -->

---

## 🔧 Pendientes abiertos

| # | Pendiente | Tipo |
|:-:|-----------|------|
| 1 | ✅ **26-jun completo: M61–M66 cargados automático** (66/72), incl. M64 Uruguay 0-1 España (campeón de Boris). **Hoy 27-jun:** M67–M72 — Panamá-Inglaterra + Croacia-Ghana (17:00), Colombia-Portugal + RD Congo-Uzbekistán (19:30), Argelia-Austria + **Jordania-Argentina** (22:00) — cierran la fase de grupos (72/72); verificar que carguen solos, si el tier gratis demora `gh workflow run actualizar.yml`. **Tras M72 → se activa el puntaje KO** (avance por fase + especiales) | vigilar |
| 2 | ✅ **RESUELTO 24-jun** — Jorge entregó planilla de eliminatorias: bracket KO 32/32 + campeón Francia ingestados (commit `fc719fa`). Solo faltan especiales opcionales | hecho |
| 3 | **Andrés** — M24 grupo en blanco + M83 KO inconsistente (llave deriva UZB-CRO, eligió Colombia) | esperar/arreglar |
| 4 | ✅ **Tarjeta WhatsApp de liga completa CON escudo FC** (27-jun, commit `a586995`) — logo embebido base64 + tagline. Se genera **local** (`python build/gen_tarjeta.py`), no en CI. Nota: el "rey de la jornada" toma todo el acumulado hasta tomar un snapshot fresco con `python build/actualizar.py --cierre "tras grupos"` (el previo no incluía a La Casa) | hecho |
| 5 | ✅ **Cuadro real del torneo en la portada + archivo plegable de grupos** (27-jun) — `engine.bracket_partial`; el cuadro se llena solo (16avos ya con los 5 cruces formados), y al cerrar los 72 aparece el `<details>` "Fase de grupos — cerrada" con las 12 tablas finales. Cruces KO también resueltos en el calendario. Evolución del ranking ya operativa. **Se completa solo esta noche al cerrar grupos** | hecho |
| 6 | `og.png` con logo FC | opcional cosmético |
| 7 | Más planillas que lleguen al pool | esperar |

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
| **Cuadro KO parcial (se llena solo)** | `engine.r32_partial` (16avos) · `engine.bracket_partial` (cuadro completo) — usados por `gen_galeria.build_real_bracket` (portada) + `gen_calendar` (calendario) |
| **Archivo plegable fase de grupos** | `gen_galeria.build_groups_archive` (aparece solo al llegar a 72/72) |
| **Tarjeta WhatsApp liga completa (con escudo FC)** | `python build/gen_tarjeta.py` → `tarjetas/tarjeta-dia.png` (logo base64; toma snapshot con `actualizar.py --cierre` para el "rey de la jornada") |
| Ingesta de planillas nuevas | `build/ingest_plantilla.py` |
| Fetch resultados + cron | `build/fetch_resultados.py` · `.github/workflows/actualizar.yml` |
| Predicciones por jugador | `data/predicciones/<SLUG>.csv` (+`_ko`, +`_especiales`) |
| Resultados | `data/resultados.csv` · `data/resultados_ko.csv` · `data/resultados_especiales.csv` |
| Visiones live + wow pendientes | `docs/EXPERIENCIA_EN_VIVO_Y_WOW.md` |
| Recap predicciones compartible (no deploya, screenshot local) | `recap/predicciones-AAAA-MM-DD.html` (+`_TEMPLATE.html` · `README.md`) |
| **Refrescar tabla + resultados del dashboard (auto, desde datos)** | `python build/refresh_dashboard.py` (reescribe solo los bloques `<!-- AUTO:TABLA -->` y `<!-- AUTO:RESULTADOS -->`; `--check` = dry-run). La narrativa se escribe a mano |
| Histórico completo del proyecto | memoria `project_quiniela_mundial_2026.md` |

---

*Última actualización: 2026-06-27 — torneo en vivo día 17, 5 jugadores, M1–M66 cargados (66/72). 🔥 Boris 131 – Carlos 110: en la jornada del 26-jun (M61–M66) Boris sumó +17 y Carlos solo +3, disparando la brecha de +7 a +21. Boris sigue líder en los tres criterios — pts (131-110), exactos (13-9) y ganadores (43-37). M61–M66 entraron todos automático (cron sano): M61 NOR 1-4 FRA, M62 SEN 5-0 IRQ, M63 CPV 0-0 KSA, M64 URU 0-1 ESP (campeón de Boris ✅), M65 EGY 1-1 IRN, M66 NZL 1-5 BEL. Copia local estaba 5 commits atrás → `git pull` la sincronizó. Hoy 27-jun van M67–M72 y cierran la fase de grupos (72/72) → se activa el puntaje KO. Sitio en vivo 66/72. Al retomar: `git pull` → `python build/refresh_dashboard.py` → escribir solo la narrativa. **Sesión 27-jun también construyó 5 features de portada/marca** (commits `618c6c9` cuadro real KO + archivo grupos plegable + R32 en calendario; `a586995` escudo FC en la tarjeta) — ver README §Pipeline y Pendientes #4/#5. `engine.bracket_partial` resuelve el cuadro parcial sin exigir los 72 → todo se autocompleta al cerrar grupos esta noche.*
