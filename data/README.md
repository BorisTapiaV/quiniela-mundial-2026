# Data layer — source of truth de la quiniela

Datos estructurales del Mundial 2026. Una vez generados (bootstrap), estos CSV son la **verdad**; se editan a mano o se regeneran. Los scripts de bootstrap viven en `../build/`.

| Archivo | Filas | Qué es | Fuente | Confianza |
|---------|:-----:|--------|--------|-----------|
| `equipos.csv` | 48 | code, grupo, pos, nombre_es/en, iso_bandera, anfitrion | **Álbum** (Boris verificó físicamente las láminas) + ISO/EN agregados | **Alta** |
| `fixture_grupos.csv` | 72 | partidos de grupo en slots + códigos | Generado de la **plantilla FIFA** (Art 12.4) + equipos.csv | **Alta** (determinístico) |
| `fixture.csv` | 104 | calendario completo: nº, fase, grupo, matchday, **fecha, hora, sede**, local, visita | Fechas/sedes de **ClasesExcel** (`tDatos`); cruces KO del **reglamento** (Art 12.6-12.11) | Media ⚠️ |
| `terceros_495.csv` | 495 | combo de 8 grupos con 3º → a qué partido R32 va cada uno | **AssignThird** (WCup, "FIFA 23.06.2025") | **Alta** (495 verificadas) |

## Esquemas

**equipos.csv** — `code,grupo,pos,nombre_es,nombre_en,iso_bandera,anfitrion`
- `code` = código FIFA 3 letras (MEX, POR…). `iso_bandera` = código flagcdn (`mx`, `gb-sct`, `gb-eng`…). `anfitrion` = `si` para A1/B1/D1.

**fixture.csv** — `match_no,fase,grupo,matchday,fecha,hora_local,sede,local,visita`
- `fase` ∈ {grupos, R32, R16, QF, SF, 3P, Final}. `matchday` ∈ {1,2,3} solo en grupos.
- En grupos `local`/`visita` = códigos de equipo. En KO = **slots**: `1A`=ganador grupo A, `2B`=segundo grupo B, `3-ABCDF`=mejor 3º de esos grupos, `W74`=ganador del M74, `L101`=perdedor del M101.

**terceros_495.csv** — `combo,m74,m77,m79,m80,m81,m82,m85,m87`
- `combo` = string ordenado de los 8 grupos cuyo 3º clasifica (ej. `ABCDEFGH`).
- `m74…m87` = letra del grupo cuyo 3º juega ese partido de R32. (Los 8 partidos de R32 que enfrentan a un 3º.)

## ⚠️ Caveats de verificación

- **`fixture.csv` fechas/horas/sedes** vienen de un modelo de terceros (ClasesExcel), **NO de FIFA primario**. Verificar contra el calendario oficial FIFA antes de dar por buenas las fechas/sedes exactas. Los **cruces** (estructura del bracket) sí son del reglamento y están verificados.
- **`equipos.csv` grupos** vienen del álbum (Boris verificó las láminas físicas reales). Alta confianza, pero si hubiera un error de sorteo, se corrige aquí.
- Las **horas** están en hora local de cada sede (columna `Q` original de ClasesExcel ya convertía; aquí se tomó la hora local cruda).
