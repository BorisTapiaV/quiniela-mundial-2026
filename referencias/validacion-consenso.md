# Validación del pronóstico vs consenso externo — Mundial 2026

> 🔒 USO INTERNO. Workflow  (7 agentes, prompts optimizados por Leonor v4.5). Cruza La Casa + Paulo contra apuestas, simuladores, expertos, ganadores de grupo, goleador y la maldición del campeón. 2026-06-07.

## Veredicto
- **Consenso campeón:** España — TOP consenso cruzado: #1 en apuestas (bet365/DraftKings/FanDuel/Kalshi, ~18.2% implícita, 4 fuentes), #1 en Opta (16.1%) y Towards Data Science (16.0%), empate técnico #1 en PELE (18.5%), y favorita editorial (ESPN O'Hanlon la da campeona). Francia es un segundísimo muy pegado (brecha 1-3 décimas de cuota).
- **Finalistas consenso:** España, Francia
- **% coincidencia ponderada:** La Casa **93%** · Paulo 75%
- Método: Coincidencia PONDERADA (no binaria) sobre 15 campos: 12 ganadores de grupo + campeón + finalistas + goleador. Escala por campo: 1.0 = coincide con el #1/consenso exacto; 0.5 = pone al 2º favorito o acierto parcial alto (alineado con la distribución del consenso, no con el pico); 0 = fuera del consenso. La Casa: campeón Francia=0.5 (2º favorito), finalistas=0.5 (acierta Francia, Argentina defendible como 3er nombre), goleador Mbappé=1.0, grupos=12.0 (12/12). Total 14.0/15 = 93%. Paulo: campeón España=1.0, finalistas=0.5 (acierta España, Inglaterra parcial), grupos=9.0 (9/12, falla A/B/K), goleador=[DATA GAP] excluido del denominador. Total 10.5/14 = 75%.

## Outliers de La Casa
- Campeón Francia sobre España: desviación LEVE y DEFENDIBLE — Francia es el #2 del consenso con brecha mínima (1-3 décimas de cuota, prob ~17.4% vs 18.2%); Opta incluso la pone 2ª favorita (13.0%). No es un fallo total sino coincidencia parcial alta.
- Sorpresa Bosnia y Herzegovina: defendible — Bosnia aparece como 2º disputado en Grupo B según Opta ('Canadá y Bosnia pelean el 2º'). Campo sin entrada directa en el consenso (no hay vara explícita de 'sorpresa'), por lo que el outlier no es necesariamente error.
- Primer eliminado Cabo Verde: [DATA GAP] — el consenso no reporta un campo de primer-eliminado, no es comparable contra vara externa.
- Ganadores de grupo: 12/12 idénticos al consenso — La Casa NO presenta ningún outlier de grupo (contraste con Paulo, que desvía en A, B y K).

## Veredicto maldición del campeón
Ambos pronósticos (La Casa y Paulo) ponen a Argentina, defensora 2022, en semifinales. CARA que la respalda (mercado/modelos): cuotas +900/+1000 la sitúan 4ª favorita al título; Opta la da campeona en 10.3% (4ª); CBS recomienda Argentina a semifinal +210 y final +470 como valor; clasificación cómoda y núcleo de Qatar intacto. CARA de riesgo (estudio maldición): 4 de 6 defensores cayeron en fase de grupos desde 2002 (66.6% — Francia 2002, Italia 2010, España 2014, Alemania 2018) y ningún campeón repite desde Brasil 1962; riesgos de edad de Messi (39) y cruces duros (Uruguay 16avos, Suiza/Colombia cuartos). VEREDICTO: evidencia MIXTA, no es ley. Francia 2022 (llegó a la final) rompe el patrón, y el formato de 48 equipos atenúa la salida temprana. El mercado y los modelos NO proyectan caída temprana; la ubican top-4. Por tanto, poner a Argentina en semis es DEFENDIBLE: ambos pronósticos están alineados con el mercado, no con la maldición. No corresponde bajarla solo por el antecedente estadístico.

## Recomendación
La Casa ya está fuertemente calibrada (93% de coincidencia ponderada, con 12/12 ganadores de grupo y goleador idénticos al consenso). Recalibración por impacto en puntaje, priorizada: (1) CAMPEÓN [impacto ALTO, suele valer más puntos] — único campo con upside real: cambiar Francia→España alinearía con el #1 unánime de apuestas (~18.2%) y 2/3 modelos (Opta 16.1%, TDS 16.0%) más empate #1 PELE; PERO la brecha es mínima y Francia es defendible como #2 muy pegado, así que el cambio es OPCIONAL, no obligatorio — depende de si la quiniela premia consenso o diferenciación. (2) FINALISTAS [impacto MEDIO] — La Casa pone Francia+Argentina; el consenso es España+Francia. Sustituir Argentina por España capturaría el par de finalistas-consenso y mantendría Francia ya acertada; mejora esperada si el scoring premia finalistas. (3) GRUPOS y GOLEADOR [impacto: NO tocar] — ya coinciden 100% con el consenso; cualquier cambio resta valor esperado. (4) Sorpresa/primer-eliminado: sin vara de consenso en <data> ([DATA GAP]), no hay base para recalibrar. Conclusión: La Casa no requiere recalibración estructural; las únicas dos jugadas de valor son campeón y finalistas, ambas hacia España, y ambas discrecionales según el apetito de riesgo.

## Tabla de comparación (campo por campo)
| Campo | La Casa | Paulo | Consenso | Coincide |
|---|---|---|---|:-:|
| Campeón | Francia | España | España (TOP en apuestas 4 fuentes + 2/3 modelos + empate #1 PELE) | ❌ |
| Finalistas | Francia, Argentina | España, Inglaterra | España y Francia (Argentina 3er nombre fuerte en expertos O'Hanlon) | ❌ |
| Semifinalistas (top-4) | Francia, España, Inglaterra, Argentina | Francia, España, Inglaterra, Argentina | España, Francia, Argentina + Inglaterra/Portugal 4º cupo | ✅ |
| Grupo A | México | Chequia | México (unánime, ESPN -125 + Al Jazeera) | ✅ |
| Grupo B | Suiza | Bosnia y Herzegovina | Suiza (ESPN -135 + Opta 42.1%) | ✅ |
| Grupo C | Brasil | Brasil | Brasil (ESPN -350 dominante) | ✅ |
| Grupo D | Estados Unidos | Estados Unidos | Estados Unidos (ESPN +140, anfitrión, parejo con Turquía) | ✅ |
| Grupo E | Alemania | Alemania | Alemania (ESPN -250 + Opta 59.9%) | ✅ |
| Grupo F | Países Bajos | Países Bajos | Países Bajos (ESPN -125) | ✅ |
| Grupo G | Bélgica | Bélgica | Bélgica (ESPN -220) | ✅ |
| Grupo H | España | España | España (ESPN -475 favoritísima) | ✅ |
| Grupo I | Francia | Francia | Francia (ESPN -215) | ✅ |
| Grupo J | Argentina | Argentina | Argentina (campeona vigente, ESPN -265) | ✅ |
| Grupo K | Portugal | Colombia | Portugal (ESPN -200) | ✅ |
| Grupo L | Inglaterra | Inglaterra | Inglaterra (ESPN -280) | ✅ |
| Goleador | Kylian Mbappé | [DATA GAP - falta input] | Kylian Mbappé (Francia, DraftKings +600 / Kalshi +525, favorito triangulado) | ✅ |

## Datos de consenso (resumen por clase)
### campeon_apuestas
TOP: Spain — favorito TOP del mercado. [HECHO] Lidera en bet365 (9/2 = 5.50 dec, 05-jun-2026), DraftKings (+450 = 5.50 dec, 07-jun-2026), FanDuel (+475 = 5.75 dec, 02-jun-2026) y el mercado de predicciones Kalshi (16.5%, 05-jun-2026). Prob implícita cruda ~18.2% (100/5.50). CONSENSO FUERTE: mismo top en >=4 fuentes (4 casas/mercados). Francia es un segundísimo muy pegado (+475/+500/5.00-6.00 dec, prob ~16-20%) — la brecha Spain-France es mínima (1-3 décimas de cuota), por lo que es un consenso fuerte en el #1 pero con Francia disputándolo. Inglaterra consolidada como #3 con clara separación del resto.
- **España**: prob 18.2% [CALCULO 100/5.50] · cuota 5.50 dec (+450 / 9-2) (DraftKings 07-jun-2026 / bet365 05-jun-2026 [HECHO]. TOP consenso.)
- **Francia**: prob 17.4% [CALCULO 100/5.75] · cuota 5.75 dec (+475 / 5-1) (FanDuel 02-jun-2026 / DraftKings +475 / bet365 5-1=6.00. [HECHO] #2 muy pegado al #1.)
- **Inglaterra**: prob 13.3% [CALCULO 100/7.50] · cuota 7.50 dec (+650 / 13-2) (FanDuel 02-jun (+650) / DraftKings +700=8.00 / bet365 13-2. [HECHO] #3 estable.)
- **Brasil**: prob 11.1% [CALCULO 100/9.00] · cuota 9.00 dec (+800 a +900 / 8-1) (bet365 8-1=9.00 (05-jun) / FanDuel +850 / DraftKings +900. [HECHO])
- **Portugal**: prob 11.8% [CALCULO 100/8.50] · cuota 8.50 dec (+850 / 8-1 a 10-1) (DraftKings +850 (07-jun) / FanDuel +1000=11.0 / bet365 8-1. [HECHO] dispersión casa a casa.)
- **Argentina**: prob 10.0% [CALCULO 100/10.0] · cuota 10.0 dec (+900 / 9-1) (DraftKings/FanDuel +900 (02-07 jun) / bet365 9-1. [HECHO])
- **Alemania**: prob 6.7% [CALCULO 100/15.0] · cuota 15.0 dec (+1400 / 14-1) (FanDuel/DraftKings +1400 (jun-2026). [HECHO])
- **Países Bajos**: prob 4.5% [CALCULO 100/22.0] · cuota 22.0 dec (+2000 a +2200 / 20-1) (DraftKings +2000=21.0 / FanDuel +2200=23.0 (jun-2026). [HECHO])

### campeon_simulador
TOP: Espana (consenso de campeon mas probable). 3 de 3 modelos estadisticos transparentes la situan #1 o empatada #1: Opta 16,1% (#1), Elo+Poisson Towards Data Science 16,0% (#1), PELE/Silver Bulletin 18,5% (empate tecnico #1, fraccionalmente bajo Argentina 18,7%). [HECHO] Consenso solido en Espana como favorita. [CONFLICTO DE MODELOS en el #2: Opta -> Francia 13,0%; Elo+Poisson TDS -> Argentina 11,9%; PELE -> Argentina 18,7% (nominalmente #1, empatada con Espana)]. Francia es la mayor discrepancia: va de 7,9% (TDS) a 13,0% (Opta); PELE la castiga (11,7%) por su grupo dificil (Noruega/Senegal). NOTA: FiveThirtyEight/ESPN SPI original esta DISCONTINUADO desde 2023-2025; PELE de Nate Silver es su sucesor [DATA GAP en SPI clasico, cubierto por PELE].
- **Espana**: 16,1% (Opta Supercomputer) | 16,0% (Elo+Poisson+MonteCarlo, Towards Data Science) | 18,5% (PELE/Silver Bulletin) (Opta corrida 2026-06-01; TDS 2026-06-06; PELE 2026-06-05. CAMPEON MAS PROBABLE por consenso (#1 en Opta y TDS, empate #1 en PELE))
- **Argentina**: 10,4% (Opta) | 11,9% (Elo+Poisson TDS, #2) | 18,7% (PELE, nominalmente #1) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05. PELE la pone fraccionalmente sobre Espana; los otros dos modelos la ubican mas abajo. Discrepancia fuerte)
- **Francia**: 13,0% (Opta, #2) | 7,9% (TDS, #3) | 11,7% (PELE) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05. CONFLICTO: Opta la hace 2da favorita, PELE la castiga por grupo dificil (Noruega/Senegal))
- **Inglaterra**: 11,2% (Opta, #3) | 7,0% (TDS) | 10,4% (PELE) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05. Consistente top-4 en los tres modelos)
- **Brasil**: 6,6% (Opta) | 5,4% (TDS) | 6,1% (PELE) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05. Notable coincidencia entre modelos (~6%))
- **Portugal**: 7,0% (Opta) | 4,3% (TDS) | 4,9% (PELE) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05)
- **Alemania**: 5,1% (Opta) | 3,7% (TDS) | 6,6% (PELE) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05)
- **Paises Bajos**: 3,6% (Opta) | 4,7% (TDS) | 2,9% (PELE) (Opta 2026-06-01; TDS 2026-06-06; PELE 2026-06-05)
