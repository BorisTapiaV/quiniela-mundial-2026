# Datos en vivo e imágenes — opciones para el visor estático (Netlify)

> Research 2026-06-07 (agente web, 16 fuentes). Cómo alimentar de resultados/datos en vivo e imágenes un sitio HTML estático de solo lectura en Netlify, para la quiniela del Mundial 2026.

---

## A. APIs de fútbol con cobertura Mundial 2026

| API | ¿WC2026? | Free tier | Datos en vivo (minuto/eventos) | CORS navegador | Pagado básico |
|-----|:--------:|-----------|--------------------------------|----------------|---------------|
| **API-Football** (api-sports.io) | Sí (104 partidos + 48 equipos ya cargados) | **100 req/día** | **Sí** — `/fixtures?live=all` (~15s), eventos: goles/tarjetas/expulsados/sustituciones con minuto, alineaciones | Problemático (expone key; restringible por dominio) | €19/mes (75k/día) |
| **football-data.org** | Sí (incluido en free) | **10 req/min** | **No** (solo fixtures/resultados/standings/alineaciones) | Sí (header token, pero key visible) | €18-50/mes |
| **openfootball/worldcup.json** (GitHub) | Sí (dominio público, incl. 2026) | **Gratis total, sin key** | No (JSON estático: calendario, equipos) | Es solo JSON en CDN | Gratis |
| **balldontlie FIFA** | Sí (dedicado al Mundial) | Free generoso | Resultados (verificar granularidad live) | API pública | Bajo |
| **TheSportsDB** | Sí | 30 req/min | No en free (live desde $9/mes, 2 min retraso) | n/d | $9/mes |
| **LiveScore API** | Sí | Trial 14d (1.500/día) | Sí (comentarios, goleadores, tarjetas) | server-side | €11/mes |
| **SportMonks** | Sí (no en free real) | Trial 14d | Sí en pagado (live, xG, bracket) | server-side | €69/mes World Cup |
| **Sportradar** | Sí (grado oficial) | No free real | Sí (push pro) | enterprise | Caro / sobredimensionado |

**Clave sobre CORS:** ninguna API comercial es "segura" para llamada directa desde el navegador, porque **la key queda expuesta** en el código del cliente. Para un sitio estático: o aceptas exponer una key gratuita de bajo valor, o usas proxy/regeneración para ocultarla.

## B. Patrones de integración con Netlify estático

| Patrón | Esfuerzo | Trade-offs |
|--------|:--------:|------------|
| **1. Fetch client-side** (JS llama directo) | Bajo | Solo si hay CORS. **Key expuesta**. Mitigar: restringir por dominio + key gratuita. Sin servidor. |
| **2. Regeneración programada** (GitHub Actions / Netlify Scheduled Functions cada X min → fetch → regenera HTML → redeploy) | Medio | **Key oculta** (secrets). Sitio 100% estático. Latencia = intervalo del cron. Ideal para resultados finales. **No da "minuto a minuto" real**. |
| **3. Netlify Function proxy** (serverless oculta key + resuelve CORS) | Medio | Cliente llama a `/.netlify/functions/scores`. Key oculta, CORS resuelto, refresco frecuente. Free tier de Functions alcanza para uso familiar. **Mejor opción para live**. |
| **4. Carga manual** (sin API) | Bajo | Editas JSON/HTML y commit. Cero costo/dependencia/riesgo legal. Tedioso en vivo; perfecto para resultado final 1×/día. |

**Por caso de uso:**
- **Resultado final para puntuar:** patrón **2** (cron 30-60 min) o **4** (manual 1×/día). Suficiente y key segura.
- **Marcador en vivo minuto a minuto:** patrón **3** (Netlify Function proxy) + fetch cliente cada 30-60s. Única forma de live sin exponer la key.

## C. Imágenes

**Banderas — uso libre ✅ (recomendado):**
- **flagcdn.com** — 254 banderas SVG/PNG/WebP por CDN, gratis. Enlace directo: `https://flagcdn.com/w320/{codigo}.png`. Ideal para estático.
- **flagpedia.net/download** y **GitHub hampusborgos/country-flags** (SVG+PNG, dominio público, auto-hospedable en el repo).
- Las banderas de países son **dominio público**, sin problema legal.

**🚫 Escudos / logos / arte oficial — EVITAR en el sitio público:**
- **Crests de federaciones** (ANFP, AFA, CBF…): marca registrada + copyright. NO son de uso libre.
- **Emblema/logo FIFA "World Cup 2026", mascotas:** protegidos mundialmente; FIFA los defiende agresivamente (cese y desistimiento).
- **Arte/láminas Panini:** copyright de Panini bajo licencia FIFA. **NO reutilizar escaneos de láminas** en el sitio (Netlify es público por defecto, aunque sea "familiar").
- **Regla práctica 100% segura:** identificar selecciones con **bandera (dominio público) + nombre del país en texto**. Nada de escudos/logos/arte FIFA-Panini.

---

## 🎯 Recomendación concreta

**Para empezar (gratis, seguro, simple):**
1. **Fixtures + equipos:** precargar desde **openfootball/worldcup.json** (gratis, sin key) en el build.
2. **Banderas:** **flagcdn.com** por enlace directo (o auto-hospedadas). Solo bandera + nombre.
3. **Resultados finales:** **football-data.org** (free) vía **patrón 2 (regeneración programada, GitHub Actions cada 30-60 min)** con key en GitHub Secrets — o **carga manual** 1×/día. Costo cero.

**Si la familia quiere marcador en vivo durante los partidos (fase 2, opcional):**
- Migrar a **API-Football** (eventos con minuto, expulsados) detrás de **Netlify Function proxy (patrón 3)**, fetch cada ~60s. Free 100 req/día alcanza si polleas solo durante partidos; €19/mes si se queda corto.

> En resumen: arrancar sin live (manual o cron + football-data.org) es lo más simple y fiel al "cero mantención". El live minuto-a-minuto es una fase 2 bien acotada (Netlify Function + API-Football) que NO compromete el resto.
