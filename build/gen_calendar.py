#!/usr/bin/env python
"""Calendario mensual (junio + julio 2026) con todos los partidos y horas.
Salida: site/calendario.html. Banderas de flagcdn para los partidos de grupo;
las eliminatorias muestran la ronda (los equipos se definen al avanzar el torneo).
"""
import csv, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOW = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
MESNOM = {6: 'Junio', 7: 'Julio'}
FASE_LBL = {'R32': '16avos', 'R16': 'Octavos', 'QF': 'Cuartos', 'SF': 'Semis', '3P': '3er puesto', 'Final': 'Final'}

def main():
    eq = engine.load_equipos(); fixture = engine.load_fixture()
    ISO = {c: eq[c]['iso'] for c in eq}
    def flag(c): return f'<img src="https://flagcdn.com/w20/{ISO[c]}.png" alt="">'

    by_day = {}
    for m in fixture:
        by_day.setdefault(m['fecha'], []).append(m)
    for d in by_day:
        by_day[d].sort(key=lambda m: m['hora_local'])

    months_html = ''
    for mes in (6, 7):
        # primer y último día del mes con partidos
        days = sorted(d for d in by_day if int(d.split('-')[1]) == mes)
        if not days:
            continue
        first = datetime.date(2026, mes, 1)
        ndays = (datetime.date(2026, mes + 1, 1) - first).days if mes < 12 else 31
        lead = first.weekday()  # 0=Lun
        cells = '<div class="cell pad"></div>' * lead
        for dd in range(1, ndays + 1):
            iso = f'2026-{mes:02d}-{dd:02d}'
            evs = ''
            for m in by_day.get(iso, []):
                if m['fase'] == 'grupos':
                    a, b = m['local'], m['visita']
                    evs += (f'<div class="ev"><span class="h">{m["hora_local"]}</span>'
                            f'{flag(a)}<b>{a}</b><i>vs</i>{flag(b)}<b>{b}</b></div>')
                else:
                    evs += (f'<div class="ev ko"><span class="h">{m["hora_local"]}</span>'
                            f'<b>{FASE_LBL.get(m["fase"], m["fase"])}</b></div>')
            cls = 'cell' + ('' if evs else ' empty')
            n = len(by_day.get(iso, []))
            tag = f'<span class="cnt">{n}</span>' if n else ''
            cells += f'<div class="{cls}"><div class="dnum">{dd}{tag}</div>{evs}</div>'
        grid = ''.join(f'<div class="dow">{d}</div>' for d in DOW) + cells
        months_html += f'<h2 class="sec">{MESNOM[mes]} 2026</h2><div class="cal">{grid}</div>'

    html = HEAD + f"""
<header><div class="kick">Copa Mundial FIFA · Canadá · México · EE.UU.</div>
<h1>Quiniela 2026</h1>
<nav><a href="index.html">Posiciones</a><a class="on" href="calendario.html">Calendario</a><a href="la-casa.html">La Casa</a></nav></header>
<div class="legend">🕐 horas en hora local de cada sede · banderas: grupos · las eliminatorias muestran la ronda</div>
{months_html}
<footer>104 partidos · 11 jun → 19 jul 2026 · datos de fixture.csv · gen_calendar.py</footer>
</div></body></html>"""
    os.makedirs(os.path.join(HERE, 'site'), exist_ok=True)
    with open(os.path.join(HERE, 'site', 'calendario.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    print('site/calendario.html generado:', len(html), 'bytes ·', sum(len(v) for v in by_day.values()), 'partidos')


HEAD = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Quiniela Mundial 2026 · Calendario</title>
<style>
:root{--bg:#0b1020;--card:#151c34;--line:#2a3358;--txt:#e8ecf7;--mut:#8d97bf;--green:#16d97b;--gold:#ffd24a;}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(180deg,#0b1020,#0e1530);color:var(--txt);font:15px/1.4 system-ui,'Segoe UI',Roboto,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:24px}
header{text-align:center;padding:24px 0 6px}.kick{color:var(--gold);letter-spacing:.18em;font-size:12px;text-transform:uppercase}
h1{margin:6px 0 4px;font-size:30px}
nav{display:flex;gap:8px;justify-content:center;margin:8px 0}
nav a{color:var(--mut);text-decoration:none;font-size:13px;padding:5px 14px;border:1px solid var(--line);border-radius:20px}
nav a.on{color:#06210f;background:var(--gold);border-color:var(--gold);font-weight:700}
.legend{text-align:center;color:var(--mut);font-size:12px;margin:8px 0 4px}
h2.sec{font-size:15px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin:28px 0 12px}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}
.dow{text-align:center;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.06em;padding-bottom:2px}
.cell{background:var(--card);border:1px solid var(--line);border-radius:8px;min-height:74px;padding:5px 6px}
.cell.pad{background:transparent;border:none}.cell.empty{opacity:.45}
.dnum{font-size:12px;color:var(--mut);font-weight:700;display:flex;justify-content:space-between;margin-bottom:3px}
.cnt{background:var(--line);color:var(--txt);border-radius:10px;font-size:10px;padding:0 6px;font-weight:600}
.ev{display:flex;align-items:center;gap:3px;font-size:11px;background:#0e1738;border-radius:5px;padding:2px 4px;margin-bottom:3px;white-space:nowrap;overflow:hidden}
.ev .h{color:var(--gold);font-weight:700;margin-right:2px}
.ev img{width:15px;border-radius:2px;flex:0 0 auto}.ev b{font-weight:600}.ev i{color:var(--mut);font-style:normal;margin:0 1px}
.ev.ko{background:#241a33}.ev.ko b{color:var(--gold)}
footer{text-align:center;color:var(--mut);font-size:12px;margin:30px 0 10px}
@media(max-width:760px){.ev{font-size:10px}.cell{min-height:60px}}
</style></head><body><div class="wrap">"""

if __name__ == '__main__':
    main()
