# Quiniela Mundial 2026 — Dashboard (CURRENT)

<!-- Updated: 2026-07-07 PM (día 27) — FEATURE "campeón muerto" 💀 en el recap + FIX bug UnicodeEncodeError. Boris (mirando el recap del día): "¿no habría que agregar abajo el primer campeón muerto?" → **nueva sección 🏆 Campeones en `gen_recap.py`**, espejo de la de goleadores: una tarjeta por jugador (bandera + país) y el campeón eliminado sale muerto (gris + tachado + 💀 + ✗, mismas clases CSS de picks-muertos). Muerto si `campeón ∈ set(equipos) − E.teams_alive(...)`; candado `PICKS_MUERTOS_DESDE=2026-07-01`; la sección solo aparece si hay campeón elegido. **Primer campeón caído: Portugal (Carlos)** tras M93. Nuevo `load_campeon()` + `champsec` + CSS `.champflag`/`.golgoals.st`. **+ FIX:** blindado el `UnicodeEncodeError` del print final (cp1252 Windows) con `sys.stdout/stderr.reconfigure(utf-8)` — el print ya sale limpio (`✓ … · 2 partido(s) · banderas 7/7`); cierra el pendiente "blindar" del 05-jul. Documentado en README §Picks muertos (goleadores + campeones). Recap 07-jul regenerado con la sección. Sin deploy (recap no deploya). 0 voseo. -->
<!-- Updated: 2026-07-07 (día 27, OCTAVOS 6/8) — SYNC + REFRESH. Retomé: local 2 commits atrás → `git pull` (HEAD fd2c86c, cron sano). Entraron por cron: **M93 España 1-0 Portugal (🚨 PORTUGAL ELIMINADO = campeón de Carlos muerto)** + **M94 Bélgica 4-1 USA**. `refresh_dashboard.py` → tabla: **BORIS 🥇 271 (13 ex) +33 · ANDRÉS 🥈 238 · PAULO 🥉 237 · CARLOS 4º 222 (💀 +0) · JORGE 217**. Terremoto en el podio: **Carlos se hundió al 4º** (Portugal out, 0 en la jornada) y la pelea por el 🥈 (30% pozo) quedó **Andrés 238 vs Paulo 237 = 1 PUNTO**. España (Boris+Paulo) y Francia (Andrés+Jorge) a cuartos. **HOY 07-jul cierran octavos: M95 Argentina-Egipto 12:00 · M96 Suiza-Colombia 16:00** (cron auto, no tocan campeones). **Cuartos con cruces de campeón definidos: M97 Francia-Marruecos 09-jul · M98 España-Bélgica 10-jul.** Narrativa + estado reescritos, sin deploy (no gasta Netlify). Recap del día pendiente de decidir (predicciones M95/M96). 0 voseo. -->
<!-- Updated: 2026-07-05 (día 25, OCTAVOS 2/8) — SYNC + REFRESH DASHBOARD. Retomé la quiniela: local venía 2 commits atrás → `git pull` (HEAD 95deb71, cron sano; los 2 Auto del 04-jul PM eran re-fetches sin partido nuevo). 16avos 16/16 cerrados (M73-M88); octavos 2/8 (M89 FRA 1-0 PAR · M90 MAR 3-0 CAN, 04-jul). `refresh_dashboard.py` → tabla al día: **BORIS 🥇 253 (13 ex) +27 · ANDRÉS 🥈 226 (subió, campeón Francia YA EN CUARTOS por M89) · PAULO 🥉 219 · CARLOS 4º 216 (cayó del 🥈) · JORGE 205**. Pelea por el 🥈 (30% pozo) entre Andrés/Paulo/Carlos en franja de 10 pts. **2 storylines:** Francia (Andrés+Jorge) clasificada a cuartos M97 (09-jul) · **M93 Portugal-España 06-jul = choque directo de campeones** (Carlos vs Boris+Paulo, uno muere). Hoy en juego: M91 Brasil-Noruega 16:00 · M92 México-Inglaterra 20:00 (cron los carga solo). **Recap 05-jul generado** (`recap/predicciones-2026-07-05.html`, M91/M92) — recordatorio: el recap es de PREDICCIONES (se hace ANTES del partido para el screenshot de WhatsApp), no de resultados. Bug cosmético: `gen_recap.py` tira `UnicodeEncodeError` en el print final (✓/· en consola cp1252 Windows) — el HTML se escribe completo igual; pendiente blindar. Narrativa + estado reescritos, sin deploy (no gasta Netlify). 0 voseo. -->
<!-- Updated: 2026-07-01 (día 21, 16avos M80-82) — RECAP KO: FIX display "Cae por casillero" + verde ganador + CUADRO-LEYENDA + doc. Boris pidió el recap de hoy → generado (M80 Ing-RDC, M81 USA-Bosnia, M82 Bel-Sen). (1) Boris flaggeó Jorge: aclaró "16avos" (no octavos) — Jorge SÍ tiene a Inglaterra en el cruce M80 pero la ingesta la hace perder (elige Noruega); el recap ponía "—" (se leía "no existe") → debía decir "pierde". Fix inicial por profundidad (`depth_of`) generó otro error: "Bélgica Senegal" para Jorge en el cruce Bélgica-Senegal (juntaba a Senegal, que en su bracket cae en OTRO casillero M78). (2) FIX CORRECTO por CASILLERO: "Cae"/"pierde" solo muestra el equipo real que está en el MISMO casillero `mn` del jugador y que no eligió ganar; "—" solo si ninguno de los 2 equipos reales está en su casillero. **Regla: "Avanza" por conjunto (calza con el puntaje, puede avanzar por otra llave) · "Cae"/"—" por casillero.** Verificados los 5 jugadores en los 3 cruces. (3) Ganador ahora en VERDE en las tarjetas (antes blanco) + tag "Avanza". (4) CUADRO-LEYENDA "Cómo leer cada predicción" (verde/tachado rojo/gris) automático en fases KO (elección de Boris; escala a octavos→final). (5) Documentado en README.md (sección "Recap diario" con la lógica + anti-pattern) + este dashboard. `recap/` NO deploya. Pendiente: commit de `gen_recap.py` + README + CURRENT. 0 voseo. -->
<!-- Updated: 2026-06-30 PM (día 20) — FEATURE "picks muertos" 💀 (ACTIVA 1-JUL). Boris aprobó un mock y pidió incorporarlo "a partir de mañana". Cuando un pick ya no puede ganar — campeón eliminado o goleador inalcanzable (su selección fuera + alguien ya tiene MÁS goles) — la tarjeta se apaga: gris + nombre tachado + ✗ + 💀. Superficies: páginas de jugador (`gen_jugador.py`, hero campeón + tarjeta goleador) y recap (`gen_recap.py`, sección goleadores). NO la tarjeta de WhatsApp (Boris saca la foto del HTML). Helpers compartidos en `engine.py` (`teams_alive`/`load_scorers`/`goleador_dead`) + candado `PICKS_MUERTOS_DESDE=2026-07-01`. NO toca el puntaje. Caso real: Jorge/Undav (Alemania fuera, 3 vs Messi 6) = muerto; los otros 4 vivos. Push `d654e4a` SIN deploy (gate off hoy; entra cuando el cron regenere mañana). 0 voseo. -->
<!-- Updated: 2026-06-30 (día 20, 16avos en curso) — FIX COSMÉTICO RECAP + INSIGHT MOTOR 2030. Recuperación de ventana caída (recap 30-jun ya generado, nada perdido). Boris flaggeó que en M78 (real Costa de Marfil vs Noruega) Paulo/Carlos/Andrés salían "tenía a Ecuador" → se leía como fallo pese a que ECUADOR CLASIFICÓ (juega M79). VERIFICADO que el puntaje NO se afecta: `engine.py:355` puntúa avance POR CONJUNTO (no por casillero) → los 5 ya sumaron +2 por Ecuador; bug solo de display. Fix en `gen_recap.py`: si el jugador no tiene a ninguno de los 2 que juegan el cruce → simple `—` sin etiqueta (rechazado el intermedio "va en M79": nadie piensa en llaves). Commit `f72e3a7` (sin deploy; recap/ se versiona pero vive fuera de site/). **INSIGHT (Boris): la quiniela es un MOTOR REUTILIZABLE para 2030** — mismo formato (48 selecciones), ~85-90% se reusa (engine/generadores/cron/correcciones acumuladas); solo cambian CSVs (equipos/fixture/jugadores) + 2 puntos a re-verificar: bracket FIFA 2030 (`terceros_495.csv`) y fuente API. ~3 semanas este año → 2-3 días en 2030. 0 voseo. -->
<!-- Updated: 2026-06-29 noche (día 19, 16avos) — 🔧 CARGA MANUAL M74 + BLINDAJE DEL FETCH. Boris: la página no reflejaba Alemania-Paraguay (jugado 16:30, terminó ~3 h antes). Diagnóstico real (no era display): el cron estaba SANO y corriendo (~cada 30 min), pero football-data tier GRATIS daba M74 `FINISHED` **con `winner: null`** porque se definió en PENALES → el log mostraba "KO: 3 terminados · 2 mapeados" y `fetch_resultados.py` lo OMITÍA por diseño (nunca escribe un resultado dudoso). El bracket calculaba bien el par (M74 = Alemania vs Paraguay), no era ese el problema. RESULTADO REAL (verificado por WebSearch, ESPN/Al Jazeera): **Alemania 1-1 Paraguay, PARAGUAY 4-3 en penales** (Enciso 42'; Havertz empató; Tah falló el penal decisivo — 1ª vez que Alemania pierde una tanda en un Mundial). Cargado a mano: `74,PAR,1,1,PENALTY_SHOOTOUT,4,3`. **FIX DURABLE en el fetch:** ahora FUSIONA en vez de sobrescribir `resultados_ko.csv` → NUNCA borra un ganador ya conocido aunque la API se atrase (antes, si el cron resolvía M75 con M74 aún null, habría borrado mi M74). Verificado en vivo: el cron volvió a correr y preservó M74. **Luego M75 Países Bajos 1-1 Marruecos (MAR 3-2 pen, Saibari; Marruecos avanza) cargado igual a mano** → cierra la jornada 29-jun (KO 4/32: M73-M76). Marcador final del día: **BORIS 🥇 205 – CARLOS 184 – ANDRÉS 178 – PAULO 177 – JORGE 165** (Andrés pasó a Paulo por 1 pt y entró al podio; Boris +21). Commits `fc1d153` (M74) + `5589b28` (M75) + deploy live verificado (badges `pen 3-4` y `pen 2-3` rendientan). **Gotcha de deploy:** pushear y disparar `gh workflow run` muy seguido → el dispatch corrió sobre el SHA viejo (carrera push↔dispatch); re-disparar tras confirmar `origin/main` lo arregló. **LECCIÓN (no repetir el bucle): cuando un KO no aparezca y el log diga "X terminados · X-1 mapeados", es la API gratis con `winner:null` en un partido de PENALES → buscar el resultado real en la web y cargarlo a mano; el fetch ya no lo borra.** **+ FEATURE Precisión de eliminatorias:** la tabla `🎯 Precisión` ahora trae dos bloques (Grupos 1X2+🎯exactos · ⚔️ Eliminatorias = acertó ganador de la llave, ACUMULADO sobre las KO jugadas) + subcampeonato nuevo **⚔️ Rey de las eliminatorias** (Jorge 3/4, último en pts pero el más certero). Reutiliza `pb['win']` del jugador vs ganador real, 0 lógica de puntaje nueva. Commit `0751db1`. **+ ACLARACIÓN ARQUITECTURA (Boris preguntó por dualidad):** NO hay dualidad real calendario↔portada — los cruces del R32 salen de UNA función `build_r32`; `r32_partial` (calendario) la devuelve tal cual con 72 grupos cerrados y `full_bracket` (portada+puntaje) la llama directo. Capas sobre la misma base, no pueden divergir en las pairings. El "bug" del calendario del 29-jun fue caché del navegador, no divergencia de código. 0 voseo. -->
<!-- Anterior 2026-06-29 (día 19, KO en curso) — 🛠️ SESIÓN DE CALENDARIO + RECAP. Boris detectó que el recap mostraba Brasil-Japón a las 21:00 cuando juega 13:00. Raíz: el `fixture.csv` tenía fecha/hora/sede pegadas al match_no equivocado a lo largo de TODO el KO (los cruces `local`/`visita` y los W-links SIEMPRE estuvieron bien → el árbol y el puntaje nunca se afectaron; verificado contra el bracket oficial: Brasil→Noruega y Alemania→Francia en octavos calzan, y la numeración FIFA coincide con los W-links). Fix display-only contra el calendario real de FIFA (hora Chile): 16avos 16/16 corregidos (M85 además tenía la fecha mal 3-jul→2-jul) + swap octavos M89/M90 (Houston↔Filadelfia). Cuartos/semis/final ya estaban bien (M102/103/104 sin hora fina publicada, quedaron en la estándar). Recap KO: etiqueta por cruce "Ganador" (antes "hasta cuartos", confuso) + "tenía a X" cuando el equipo que el jugador puso no juega el cruce real. Goleadores: `scorers?limit=30`→`100` (Cristiano Ronaldo 2 goles quedaba fuera del corte → mostraba 0) + fila manual de Ronaldo. Commit `a27ac85` + deploy manual OK (regeneró site/ desde el fixture nuevo). SIN resultados nuevos: M74/75/76 (Alemania-Paraguay 16:30, P.Bajos-Marruecos 21:00, Brasil-Japón 13:00) se juegan HOY → el cron los carga solo. Marcador sin cambios: BORIS 🥇 197 – CARLOS 172 – PAULO 169. 0 voseo. -->
<!-- Anterior 2026-06-28 — 🏁 FASE DE GRUPOS CERRADA (72/72, día 18). 5 jugadores, pozo $50.000. M67–M72 entraron AUTOMÁTICO la noche del 27-jun (cron sano) → se ACTIVÓ EL PUNTAJE KO (avance por fase + especiales). Con el KO sumado: BORIS 🥇 197 – CARLOS 172 (+25). Pero ojo: PAULO 169 se le pegó a Carlos por solo +3 → el 🥈 está en disputa. Boris sigue líder (13 exactos). Resultados 27-jun: M67 PAN 0-2 ENG, M68 CRO 2-1 GHA, M69 COL 0-0 POR, M70 COD 3-1 UZB, M71 ALG 3-3 AUT, M72 JOR 1-3 ARG. Cuadro KO real ya visible en portada (se autocompletó al cerrar grupos). Sitio 2026-mundial.netlify.app. **SESIÓN 28-jun PM (Claude) — TODO DEPLOYADO Y VERIFICADO** (7 commits): (1) **fix M24 Andrés** (160→162, bracket 16/16 con su planilla); (2) **especiales = campeón + goleador** (retirados 'primer eliminado'+'sorpresa' ambiguos; máx 718→683); (3) **goleadores 5/5** (CR7/Messi/Undav/Mbappe×2) — especiales cerrados; (4) **recap AUTOMATIZADO** `python build/gen_recap.py <fecha>` (NO se deploya); (5) **sección goleadores en recap** con foto + goles en vivo (`/scorers` de football-data CONFIRMADO, `fetch_goleadores.py` al cron); (6) **recap KO pick corregido** (el equipo que hace GANAR; "—" si no pasa ninguno — calza con el puntaje); (7) calendario regen en `actualizar.py`; (8) **"Resultados por día" PLEGABLE**; (9) **cuadro KO = marcador en vivo** (banderas + score + "pen X-Y"/"prórroga"; `fetch_resultados` captura fullTime/duration/penalties); (10) marcador verificado (M73 ganó Canadá, +4 legítimo a los 3 que la tenían en octavos). **2 memorias nuevas: Carlos-CFO + no-deploy-cada-cambio (gasta cupo Netlify).** PENDIENTE: el cron carga/puntúa KO conforme se juegan. | Anterior 2026-06-27 (día 17, 66/72): Boris 131 – Carlos 110 (+21) en fase de grupos, antes del KO. | Doc de estado vivo — diseño/decisiones en README.md, histórico en la memoria project_quiniela_mundial_2026.md -->
<!-- Mantener: dashboard puro. Estado + pendientes + datos operativos + puntos de entrada. -->

---

## Estado al 2026-07-07 — 🔥 OCTAVOS EN CURSO (6/8, día 27)

El Mundial arrancó el **11-jun**. El sistema corre **en automático**: cron GitHub Actions → fetch resultados (football-data tier gratis) → deploy-on-change a Netlify. **16avos 16/16 cerrados** (M73–M88) y **octavos 6/8** jugados (M89 Francia 1-0 Paraguay · M90 Marruecos 3-0 Canadá · M91 Noruega 2-1 Brasil 🚨 · M92 Inglaterra 3-2 México · **M93 España 1-0 Portugal** 🚨 · **M94 Bélgica 4-1 USA**). El KO se puntúa por avance de fase — cada ronda superada por un equipo del jugador suma.

🚨 **Terremoto en el podio — Portugal ELIMINADO (España 1-0):** el campeón de **Carlos** murió en octavos → Carlos **no sumó nada** en la jornada (💀 +0) y **cayó del 🥈 al 4º**. España (Boris + Paulo) avanza a cuartos. Antes, Brasil ya había caído (M91) y Bélgica goleó a USA (M94).

🔥 **BORIS 🥇 271 (13 exactos) — líder firme, +33 sobre el 2º.** España a cuartos le dio +12. Detrás, el podio se sacudió: **Andrés 🥈 (238, Francia)** y **Paulo 🥉 (237, España)** quedaron **empatados a 1 punto** por el 🥈 (30% del pozo); **Carlos 4º (222, Portugal out)** y Jorge 5º (217, Francia). Desempate del leaderboard: pts → exactos → campeón → FIFA.

🔴 **Hoy 07-jul — cierran octavos (2 partidos, sin campeones en juego):** **M95 Argentina–Egipto** (12:00, Atlanta) · **M96 Suiza–Colombia** (16:00, Vancouver). El cron los carga solo. **Cuartos ya con cruces de campeón definidos:** **M97 Francia–Marruecos** (09-jul, sostiene a Andrés+Jorge) · **M98 España–Bélgica** (10-jul, el de Boris+Paulo) · M99 Noruega–Inglaterra (11-jul) · M100 (11-jul, W95 vs W96).

⚠️ **Recordatorio operativo:** si un octavo se define por **penales**, football-data tier gratis lo da `FINISHED` con `winner:null` y el fetch lo omite (síntoma en log: `KO: N terminados · N-1 mapeados`) → buscar resultado real en la web y cargarlo a mano en `data/resultados_ko.csv`. No es bug, es la API. Ya pasó en 16avos (M74/M75/M88).

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
- (11) **Fix banderas del Cuadro del torneo** (Screenshot_588): el bracket usaba `flagcdn.com/w30/` → **w30 NO existe en flagcdn (404)** → banderas invisibles solo en el cuadro KO. Corregido a **w40**. (Lección: flagcdn solo acepta w20/w40/w80/w160/w320…, NO cualquier ancho.) Commit `208f637`.
- (12) **Calendario — KO jugados ahora muestran marcador + ganador** (antes solo los de grupo se actualizaban; los KO quedaban como pendientes). `gen_calendar.py` lee `resultados_ko.csv` y muestra score orientado al cruce + ganador resaltado + badge `pen X-Y`/`prór`. Commit `ab43827`.
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
| 🥇 | **Boris Tapia V (La Casa)** | España | **271** | 13 | 🟢 |
| 🥈 | **Andrés Acosta (Colombia)** | Francia | **238** | 9 | 🟢 |
| 🥉 | Paulo Salas | España | 237 | 10 | 🟢 |
| 4 | Carlos Salgado | Portugal | 222 | 9 | 🟢 |
| 5 | Jorge Vásquez | Francia | 217 | 8 | 🟢 |
<!-- AUTO:TABLA fin -->

**La carrera en octavos (6/8):** **Boris 271 (13 exactos)** manda con **+33** sobre el 2º — liderato sólido, desempate pts → exactos → campeón → FIFA (`config/reglas-puntaje.md`). **El baile por el 🥈 (30% del pozo) se apretó a muerte:** **Andrés 🥈 (238, Francia)** vs **Paulo 🥉 (237, España)** separados por **1 solo punto**. **Carlos se hundió al 4º (222, Portugal eliminado)** — su campeón murió en el M93 y no sumó en la jornada. Jorge 5º (217). **Dos campeones vivos, cara a cara la próxima ronda:** (1) **Francia (Andrés + Jorge)** juega M97 vs Marruecos el 09-jul. (2) **España (Boris + Paulo)** juega **M98 vs Bélgica el 10-jul** — donde Boris y Paulo suben o caen juntos, así que ese cruce no rompe el empate Andrés/Paulo, pero sí define si Boris estira aún más la ventaja.

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
- ⚠️ **KO definido por PENALES = `winner: null` en el tier gratis** (caso M74, 29-jun). La API da el partido `FINISHED` pero sin ganador resuelto, así que el fetch lo OMITE (no adivina). Síntoma en el log: `KO: N terminados · N-1 mapeados al bracket`. **No es bug ni bracket — es la API.** Solución: buscar el resultado real en la web → cargar a mano en `data/resultados_ko.csv` (`match_no,ganador,g_gan,g_per,PENALTY_SHOOTOUT,pen_gan,pen_per`) → `python build/actualizar.py` → commit + `gh workflow run actualizar.yml`. El fetch **FUSIONA** (no sobrescribe): una vez cargado a mano, el cron ya **no lo borra** aunque la API siga sin el winner.
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

*Última actualización: 2026-07-07 — día 27, OCTAVOS EN CURSO (6/8). Sync `git pull` (HEAD fd2c86c) + `refresh_dashboard.py`. Entraron M93 España 1-0 Portugal (🚨 Portugal eliminado = campeón de Carlos muerto) + M94 Bélgica 4-1 USA (cron 06-jul PM). Tabla: BORIS 🥇 271 (13 ex) +33 · ANDRÉS 🥈 238 · PAULO 🥉 237 · CARLOS 4º 222 (💀 +0) · JORGE 217. Terremoto: Carlos cae al 4º (Portugal out), el 🥈 (30% pozo) queda Andrés 238 vs Paulo 237 = 1 punto. España y Francia a cuartos. HOY 07-jul cierran octavos: M95 Argentina-Egipto 12:00 · M96 Suiza-Colombia 16:00 (cron auto, sin campeones). Cuartos: M97 Francia-Marruecos 09-jul · M98 España-Bélgica 10-jul. Sin deploy. Al retomar: `git pull` → `refresh_dashboard.py` → narrativa a mano. **+ PM: feature "campeón muerto" 💀 en el recap (nueva sección 🏆 Campeones, espejo de goleadores; Portugal/Carlos = primer campeón caído) + fix del UnicodeEncodeError del print (reconfigure utf-8). README actualizado.** Histórico previo abajo.*

*Histórico: 2026-06-27 — torneo en vivo día 17, 5 jugadores, M1–M66 cargados (66/72). 🔥 Boris 131 – Carlos 110: en la jornada del 26-jun (M61–M66) Boris sumó +17 y Carlos solo +3, disparando la brecha de +7 a +21. Boris sigue líder en los tres criterios — pts (131-110), exactos (13-9) y ganadores (43-37). M61–M66 entraron todos automático (cron sano): M61 NOR 1-4 FRA, M62 SEN 5-0 IRQ, M63 CPV 0-0 KSA, M64 URU 0-1 ESP (campeón de Boris ✅), M65 EGY 1-1 IRN, M66 NZL 1-5 BEL. Copia local estaba 5 commits atrás → `git pull` la sincronizó. Hoy 27-jun van M67–M72 y cierran la fase de grupos (72/72) → se activa el puntaje KO. Sitio en vivo 66/72. Al retomar: `git pull` → `python build/refresh_dashboard.py` → escribir solo la narrativa. **Sesión 27-jun también construyó 5 features de portada/marca** (commits `618c6c9` cuadro real KO + archivo grupos plegable + R32 en calendario; `a586995` escudo FC en la tarjeta) — ver README §Pipeline y Pendientes #4/#5. `engine.bracket_partial` resuelve el cuadro parcial sin exigir los 72 → todo se autocompleta al cerrar grupos esta noche.*
