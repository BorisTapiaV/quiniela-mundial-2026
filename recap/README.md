# Tarjetas de predicciones (recap) — diseño reutilizable

Carpeta para las tarjetas HTML compartibles de la quiniela. **Fuera de `site/`** a propósito:
NO se deployan (el cron de Netlify solo publica `site/`). Se abren en local y se les saca screenshot.

## Diseño canónico

- **Plantilla:** `_TEMPLATE.html`
- **Referencia aprobada por Boris:** `predicciones-2026-06-14.html` (14-jun-2026 — "quedó buenísimo")

Características del diseño (no romper sin que Boris lo pida):
- Self-contained: sin imágenes ni fuentes externas → funciona offline, no hay imagen rota en el screenshot.
- Ancho fijo 920px, fondo oscuro con degradado, un bloque por hora de partido.
- Header "Fisioterapia & Futbolito FC" + crest ⚽ + fecha.
- Tarjeta de **Boris / La Casa** resaltada en verde (`.pred.casa`).
- Goleadas/picks llamativos en dorado con 🔥 (`.pred.hot`).
- **Sin emojis de bandera** (en Windows se ven como letras): usar badge con código de 3 letras (`.code`).
- Partidos ya jugados llevan badge `YA JUGADO` (`.played`); los pendientes muestran la sede (`.venue`).

## Regla: las tarjetas de jornada llevan SOLO predicciones

La tabla de posiciones NO va en el recap diario — el sitio
(`2026-mundial.netlify.app`) ya la muestra en vivo, ese es su rol.
El recap es la tarjeta de **pronósticos** para compartir por WhatsApp.

**Excepción — tarjeta de cierre del Mundial:** para el recap final (campeón
definido) sí tiene sentido congelar el podio. El bloque de tabla (CSS + HTML,
diseño aprobado por Boris 23-jun) está guardado listo para pegar en
`_FRAGMENTO_tabla-posiciones.html`.

## Cómo generar una fecha nueva — AUTOMÁTICO (desde 28-jun-2026)

Un solo comando arma la tarjeta completa (partidos del día + picks de los 5 jugadores +
banderas embebidas), tanto en fase de grupos como en KO:

```bash
python build/gen_recap.py 2026-06-29            # tarjeta real de esa fecha
python build/gen_recap.py 2026-07-03 --prueba   # tarjeta marcada como PRUEBA (banner naranjo)
```

Luego abrir y capturar:
```powershell
start recap\predicciones-2026-06-29.html
```

Qué hace `gen_recap.py` (`build/gen_recap.py`):
- Lee los partidos de la fecha del `fixture.csv` (1 o varios, escala solo).
- **Grupos:** marcador `gl-gv` + ganador (nombre país / "Empate") de cada jugador.
- **KO:** el pick = el equipo que el cuadro de cada jugador **hace avanzar más lejos** en ese
  cruce (regla consistente con el puntaje por equipos-que-avanzan); el `.tag` dice hasta dónde
  lo lleva ("pasa a octavos", "hasta semis", "campeón"). Si no tiene a ninguno de los dos → "—".
- Baja las **banderas** (flagcdn w40) y las **embebe en base64** → tarjeta self-contained, el
  screenshot nunca sale con banderas rotas.
- Orden de jugadores: Boris(CASA) · Paulo · Carlos · Andrés · Jorge.

> El proceso manual viejo (copiar `_TEMPLATE.html` y rellenar a mano) quedó obsoleto. El
> `_TEMPLATE.html` se conserva solo como referencia del diseño aprobado.

## Códigos de equipo usados (3 letras → país)

AUS Australia · TUR Turquía · GER Alemania · CUW Curazao · NED Países Bajos · JPN Japón
· CIV Costa de Marfil · ECU Ecuador · SWE Suecia · TUN Túnez · MEX México · RSA Sudáfrica
· KOR Corea del Sur · CZE Chequia · CAN Canadá · BIH Bosnia · USA Estados Unidos · PAR Paraguay
(ver `data/equipos.csv` para el set completo).
