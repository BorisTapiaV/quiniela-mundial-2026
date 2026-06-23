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

## Cómo generar una fecha nueva

1. Identificar los partidos de la fecha y su hora:
   ```bash
   grep "AAAA-MM-DD" data/fixture.csv
   # columnas: match_no,fase,grupo,matchday,fecha,hora_chile,sede,local,visita
   ```

2. Extraer los pronósticos de los 5 jugadores para esos match_no (ajustar el rango `>=N && <=M`):
   ```bash
   cd data/predicciones
   for f in CASA PAULO_SALAS CARLOS_SALGADO ANDRES_ACOSTA JORGE_VASQUEZ; do
     echo "=== $f ==="
     awk -F, '$1>=8 && $1<=12 {print $1": "$2" "$4"-"$5" "$3}' $f.csv
   done
   # salida por jugador: match_no: LOCAL gl-gv VISITA
   ```
   Orden de jugadores en la tarjeta: Boris(CASA) · Paulo · Carlos · Andrés · Jorge.
   El `.tag` bajo cada marcador dice quién gana (nombre país) o "Empate".

3. Revisar si algún partido ya se jugó (badge `YA JUGADO`) según la hora vs. el momento actual.
   Marcador real: `data/resultados.csv` (vacío = aún no ingestado por el cron).

4. Copiar `_TEMPLATE.html` → `predicciones-AAAA-MM-DD.html`, reemplazar fecha, partidos y los 5×N marcadores.

5. Abrir y capturar:
   ```powershell
   start recap\predicciones-AAAA-MM-DD.html
   ```

## Códigos de equipo usados (3 letras → país)

AUS Australia · TUR Turquía · GER Alemania · CUW Curazao · NED Países Bajos · JPN Japón
· CIV Costa de Marfil · ECU Ecuador · SWE Suecia · TUN Túnez · MEX México · RSA Sudáfrica
· KOR Corea del Sur · CZE Chequia · CAN Canadá · BIH Bosnia · USA Estados Unidos · PAR Paraguay
(ver `data/equipos.csv` para el set completo).
