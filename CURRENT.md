# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-06-28 — 🏁 FASE DE GRUPOS CERRADA (72/72, día 18). 5 jugadores, pozo $50.000. M67–M72 entraron AUTOMÁTICO la noche del 27-jun (cron sano) → se ACTIVÓ EL PUNTAJE KO (avance por fase + especiales). Con el KO sumado: BORIS 🥇 197 – CARLOS 172 (+25). Pero ojo: PAULO 169 se le pegó a Carlos por solo +3 → el 🥈 está en disputa. Boris sigue líder (13 exactos). Resultados 27-jun: M67 PAN 0-2 ENG, M68 CRO 2-1 GHA, M69 COL 0-0 POR, M70 COD 3-1 UZB, M71 ALG 3-3 AUT, M72 JOR 1-3 ARG. Cuadro KO real ya visible en portada (se autocompletó al cerrar grupos). Sitio 2026-mundial.netlify.app. **SESIÓN 28-jun PM (Claude) — TODO DEPLOYADO Y VERIFICADO** (7 commits): (1) **fix M24 Andrés** (160→162, bracket 16/16 con su planilla); (2) **especiales = campeón + goleador** (retirados 'primer eliminado'+'sorpresa' ambiguos; máx 718→683); (3) **goleadores 5/5** (CR7/Messi/Undav/Mbappe×2) — especiales cerrados; (4) **recap AUTOMATIZADO** `python build/gen_recap.py <fecha>` (NO se deploya); (5) **sección goleadores en recap** con foto + goles en vivo (`/scorers` de football-data CONFIRMADO, `fetch_goleadores.py` al cron); (6) **recap KO pick corregido** (el equipo que hace GANAR; "—" si no pasa ninguno — calza con el puntaje); (7) calendario regen en `actualizar.py`; (8) **"Resultados por día" PLEGABLE**; (9) **cuadro KO = marcador en vivo** (banderas + score + "pen X-Y"/"prórroga"; `fetch_resultados` captura fullTime/duration/penalties); (10) marcador verificado (M73 ganó Canadá, +4 legítimo a los 3 que la tenían en octavos). **2 memorias nuevas: Carlos-CFO + no-deploy-cada-cambio (gasta cupo Netlify).** PENDIENTE: el cron carga/puntúa KO conforme se juegan. | Anterior 2026-06-27 (día 17, 66/72): Boris 131 – Carlos 110 (+21) en fase de grupos, antes del KO. | Doc de estado vivo — diseño/decisiones en README.md, histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-06-28 — 🏁 FASE DE GRUPOS CERRADA (72/72, día 18)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **72/72 partidos de grupos cargados** — M67–M72 entraron solos la noche del 27-jun (cron sano). **Con el cierre de grupos se ACTIVÓ EL PUNTAJE KO** (avance por fase + especiales), por eso los puntajes pegaron el salto.

🔥 **BORIS 🥇 197 – CARLOS 172 (+25).** Con el KO sumado Boris mantiene el liderato. **Pero el 🥈 se calentó: Paulo (169, 10 exactos) quedó a solo +3 de Carlos** — la pelea por el segundo lugar (premio 30% del pozo) está abierta. Boris sigue líder por pts y exactos (**13**). Desempate del leaderboard: pts → exactos → campeón → FIFA.

✅ **M67–M72 entraron TODOS AUTOMÁTICO** (noche del 27-jun). Resultados: M67 Panamá 0-2 Inglaterra, M68 Croacia 2-1 Ghana, **M69 Colombia 0-0 Portugal**, M70 RD Congo 3-1 Uzbekistán, M71 Argelia 3-3 Austria, **M72 Jordania 1-3 Argentina**.

⏳ **Arrancan los 16avos (KO).** El cuadro real del torneo ya se autocompletó en la portada al cerrar grupos. Pendiente operativo: **verificar que el cron cargue los partidos KO y puntúe el avance por fase**; si el tier gratis demora → `gh workflow run actualizar.yml`.

📋 **Jorge completó su bracket KO + campeón (Francia)** el 24-jun. Especiales opcionales sin llenar. **Pendiente #2 cerrado.**

🛠️ **Sesión 28-jun PM — TODO DEPLOYADO Y VERIFICADO EN VIVO** (commits `3414bd0`·`16eed61`·`02041e3`·`75e27a9`·`8db9a4c`·`52b2fae`·`8b68d22` + fix recap `…`):
- (1) **M24 de Andrés corregido** (transcripción UZB↔COL invertida → Colombia 2ª como en su planilla; **total 160→162**; bracket 16/16 con su Excel).
- (2) **Especiales reducidos a campeón + goleador** — retirados *primer eliminado* y *sorpresa* (ambiguos: deducibles cerrados los grupos = ventaja si se completan ahora). `engine.py` W_ESP={campeón 50, gol 25}, máx 718→683. No movió posiciones.
- (3) **Goleadores COMPLETOS (5/5):** Andrés=Cristiano Ronaldo · Paulo=Lionel Messi · Jorge=Deniz Undav · Carlos=Kylian Mbappe · Casa=Mbappe. Especiales cerrados.
- (4) **Recap diario AUTOMATIZADO:** `python build/gen_recap.py <fecha>` (grupos o KO, banderas embebidas). **NO se deploya** (vive en `recap/`, es para screenshot WhatsApp).
- (5) **Sección de goleadores en el recap:** figura + **foto** (headshot Wikimedia base64) + **goles en vivo**. Los goles salen del **`/scorers` de football-data.org** (CONFIRMADO que el tier lo permite) vía `fetch_goleadores.py` enganchado al cron → `data/goleadores.csv`. Fotos en `data/figuras_fotos.json`. Puntero resaltado (Messi 6).
- (6) **Recap KO — regla de pick CORREGIDA:** el pick = el equipo que el jugador hace GANAR el cruce (en el set de la ronda siguiente); si no hace pasar a ninguno → **"—"**. Antes decía "la hace pasar" aunque cayera ahí (caso Casa/Canadá: confuso, ya no). Calza 1:1 con el puntaje.
- (7) **Calendario** se regenera en `actualizar.py` (estaba congelado).
- (8) **"Resultados por día" ahora PLEGABLE** (`<details>`, cumplió su función).
- (9) **Cuadro KO = marcador en vivo:** banderas (ya estaban) + **marcador del partido** + **"pen X-Y"** si penales / **"prórroga"** si alargue. `fetch_resultados.py` captura `fullTime`+`duration`+`penalties`; esquema ampliado en `resultados_ko.csv` (g_gan,g_per,duracion,pen_gan,pen_per). Minutos: no hay en vivo para terminados.
- (10) **Marcador verificado:** el salto (Carlos/Andrés/Jorge +4) fue legítimo = **entró el M73 (ganó Canadá)**, +4 a quienes la tenían en octavos. Boris/Paulo 0 (no la hacían avanzar). Auto-goleadores del cron funcionando.
- 📌 **Memorias nuevas:** `project_carlos_cfo_precision_signal.md` (Carlos CFO confundió V-MYCEL/VERA + aseveraciones inexistentes; la quiniela fue la sonda) · `quiniela_no_deploy_cada_cambio.md` (**NO deployar a cada rato — gasta cupo Netlify de Boris; batchear/preguntar; recap no gasta**).

- **Sitio público:** https://2026-mundial.netlify.app
- **Repo:** **PÚBLICO** `github.com/BorisTapiaV/quiniela-mundial-2026` (Actions ilimitado gratis)
- **Último commit:** `20e6776` (Auto: resultados nuevos, 2026-06-28T05:14Z) · sitio en vivo 72/72
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
## 🏆 Tabla de posiciones (tras 72 partidos)

| Pos | Jugador | Campeón | Pts | Exactos | Vivo |
|:---:|---------|---------|:---:|:---:|:---:|
| 🥇 | **Boris Tapia V (La Casa)** | España | **197** | 13 | 🟢 |
| 🥈 | **Carlos Salgado** | Portugal | **172** | 9 | 🟢 |
| 🥉 | Paulo Salas | España | 169 | 10 | 🟢 |
| 4 | Andrés Acosta (Colombia) | Francia | 160 | 9 | 🟢 |
| 5 | Jorge Vásquez | Francia | 153 | 8 | 🟢 |
<!-- AUTO:TABLA fin -->

**La carrera tras cerrar grupos + activar KO:** **Boris 197 – Carlos 172** (Boris **+25**), con Boris líder por pts y exactos (**13**) — desempate del leaderboard pts → exactos → campeón → FIFA (`config/reglas-puntaje.md`). **El foco se movió al 🥈: Paulo (169, 10 exactos) quedó a +3 de Carlos** y le pelea el segundo lugar (30% del pozo). Andrés 4º (160, 9 exactos) y Jorge 5º (153, 8) siguen vivos pero más lejos del podio. El salto de puntaje (≈+65 a todos) viene del **avance por fase del KO** que se acaba de puntuar. Haití = primer eliminado (especial, ya puntuable).

---

<!-- AUTO:RESULTADOS inicio — generado por build/refresh_dashboard.py, no editar a mano -->
## 📊 Resultados cargados (M1–M72)

| Match | Partido | Marcador | Fecha |
|:-----:|---------|:--------:|------|
| M72 | Jordania – Argentina | 1-3 | 27-jun |
| M71 | Argelia – Austria | 3-3 | 27-jun |
| M70 | RD Congo – Uzbekistán | 3-1 | 27-jun |
| M69 | Colombia – Portugal | 0-0 | 27-jun |
| M68 | Croacia – Ghana | 2-1 | 27-jun |
| M67 | Panamá – Inglaterra | 0-2 | 27-jun |
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

**M1–M48 (11-jun–23-jun):** MEX 2-0 RSA · KOR 2-1 CZE · CAN 1-1 BIH · USA 4-1 PAR · QAT 1-1 SUI · BRA 1-1 MAR · HAI 0-1 SCO · AUS 2-0 TUR · GER 7-1 CUW · NED 2-2 JPN · CIV 1-0 ECU · SWE 5-1 TUN · ESP 0-0 CPV · BEL 1-1 EGY · KSA 1-1 URU · IRN 2-2 NZL · FRA 3-1 SEN · IRQ 1-4 NOR · ARG 3-0 ALG · AUT 3-1 JOR · POR 1-1 COD · ENG 4-2 CRO · GHA 1-0 PAN · UZB 1-3 COL · CZE 1-1 RSA · SUI 4-1 BIH · CAN 6-0 QAT · MEX 1-0 KOR · USA 2-0 AUS · SCO 0-1 MAR · BRA 3-0 HAI · TUR 0-1 PAR · NED 5-1 SWE · GER 2-1 CIV · ECU 0-0 CUW · TUN 0-4 JPN · ESP 4-0 KSA · BEL 0-0 IRN · URU 2-2 CPV · NZL 1-3 EGY · ARG 2-0 AUT · FRA 3-0 IRQ · NOR 3-2 SEN · JOR 1-2 ALG · POR 5-0 UZB · ENG 0-0 GHA · PAN 0-1 CRO · COL 1-0 COD.
<!-- AUTO:RESULTADOS fin -->

---

## 🔧 Pendientes abiertos

| # | Pendiente | Tipo |
|:-:|-----------|------|
| 1 | 🏁 **27-jun completo: M67–M72 cargados automático → fase de grupos CERRADA 72/72 + puntaje KO ACTIVADO.** Ahora arrancan los **16avos**. Próximo a vigilar: que el cron cargue los **partidos KO** y puntúe el avance por fase; si el tier gratis demora `gh workflow run actualizar.yml`. Verificar también que `resultados_ko.csv` se vaya poblando | vigilar |
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
