#!/usr/bin/env python
"""Tarjeta de CIERRE del Mundial 2026 para WhatsApp.

No es un recap de partido: la quiniela ya quedó decidida (Boris campeón, reparto
congelado). Esta tarjeta cuenta el cierre y lo único que sigue vivo (que NO cambia
el sobre): el especial de campeon (+50, Espana en la final) y la Bota de Oro (+25,
Mbappe vs Messi 8-8). El 3er puesto no da puntos de bracket; entra solo por la Bota
(es el ultimo partido de Mbappe).

Uso: python build/gen_cierre.py
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from gen_tarjeta import logo_data_uri, SITE_URL, OUTDIR

ISO = {'ESP': 'es', 'ARG': 'ar', 'FRA': 'fr', 'POR': 'pt', 'ENG': 'gb-eng'}


def fl(code, w=40):
    return f'<img class="fl" src="https://flagcdn.com/w{w}/{ISO[code]}.png" alt="">'


# Tabla final (72 grupos + KO hasta semis). Reparto 50/30/20 del pozo $50.000.
ROWS = [
    ('🥇', 'Boris Tapia V', 'ESP', 349, '$25.000', False),
    ('🥈', 'Paulo Salas',   'ESP', 299, '$15.000', False),
    ('🥉', 'Andrés Acosta', 'FRA', 264, '$10.000', True),
    ('4',  'Jorge Vásquez', 'FRA', 253, '—',       True),
    ('5',  'Carlos Salgado','POR', 228, '—',       True),
]


def row_html(rk, name, champ, pts, prize, dead):
    dc = ' dead' if dead else ''
    skull = ' 💀' if dead else ''
    prize_cls = 'prize' if prize != '—' else 'prize no'
    return (f'<tr class="{dc}"><td class="rk">{rk}</td>'
            f'<td class="nm">{fl(champ,40)}{name}{skull}</td>'
            f'<td class="tot">{pts}</td>'
            f'<td class="{prize_cls}">{prize}</td></tr>')


TRS = '\n'.join(row_html(*r) for r in ROWS)

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
*{{margin:0;box-sizing:border-box}}
html,body{{width:1000px;background:#0b1020;font:16px system-ui,'Segoe UI',Roboto,sans-serif}}
.card{{width:1000px;background:linear-gradient(170deg,#0b1020,#101a3a 60%,#0e1530);
color:#e8ecf7;padding:44px 48px 36px}}
.brand{{display:flex;align-items:center;justify-content:center;gap:15px;margin-bottom:12px}}
.brand img{{width:66px;height:66px;object-fit:contain;border-radius:12px;box-shadow:0 4px 14px #0007;background:#0e1530;padding:3px}}
.brand .bn{{font-size:25px;font-weight:800;letter-spacing:.01em;line-height:1.05;text-align:left}}
.brand .bn small{{display:block;font-size:13px;font-weight:600;color:#8d97bf;margin-top:3px}}
.kick{{color:#ffd24a;letter-spacing:.22em;font-size:17px;text-transform:uppercase;text-align:center}}
.h1{{font-size:48px;font-weight:800;text-align:center;margin:6px 0 2px}}
.sub{{text-align:center;color:#8d97bf;font-size:21px;margin-bottom:24px}}
.champ{{display:flex;align-items:center;gap:22px;background:linear-gradient(150deg,#2a2140,#3a2c1a);
border:1px solid #6a5220;border-radius:20px;padding:24px 30px;margin-bottom:24px;box-shadow:0 6px 22px #0006}}
.champ .fl{{width:88px;border-radius:7px;box-shadow:0 4px 14px #0009}}
.champ .lbl{{color:#ffd24a;font-size:16px;letter-spacing:.14em;text-transform:uppercase}}
.champ .who{{font-size:38px;font-weight:800;line-height:1.1}}
.champ .note{{color:#c7cef0;font-size:16px;margin-top:3px}}
.champ .pts{{margin-left:auto;text-align:right}}
.champ .pts b{{font-size:40px;color:#ffd24a;display:block}}
.champ .pts span{{color:#16d97b;font-size:22px;font-weight:800}}
table{{width:100%;border-collapse:collapse;font-size:21px;margin-bottom:24px}}
td{{padding:11px 10px;border-bottom:1px solid #222c52}}
.rk{{width:54px;text-align:center;font-size:23px}}
.nm{{font-weight:700}}
.nm .fl{{width:26px;border-radius:4px;vertical-align:-5px;margin-right:11px;box-shadow:0 1px 3px #0008}}
.tot{{text-align:right;font-weight:800;color:#ffd24a;width:80px}}
.prize{{text-align:right;width:120px;font-weight:800;color:#16d97b}}
.prize.no{{color:#5a648c;font-weight:600}}
tr.dead .nm{{opacity:.62}}
.live-h{{text-align:center;color:#ffd24a;font-size:19px;font-weight:800;letter-spacing:.03em;margin-bottom:4px}}
.live-s{{text-align:center;color:#8d97bf;font-size:15px;margin-bottom:16px}}
.tiles{{display:flex;gap:16px;margin-bottom:8px}}
.tile{{flex:1;background:#151c34;border:1px solid #2a3358;border-radius:16px;padding:18px 20px}}
.tile .tt{{font-size:16px;color:#ffd24a;font-weight:800;margin-bottom:8px}}
.tile .big{{font-size:22px;font-weight:800;line-height:1.25;margin-bottom:8px}}
.tile .big .fl{{width:30px;border-radius:4px;vertical-align:-6px;margin:0 6px;box-shadow:0 1px 3px #0008}}
.tile .who{{font-size:15px;color:#c7cef0;line-height:1.4}}
.tile .when{{font-size:14px;color:#8d97bf;margin-top:8px}}
.foot{{display:flex;align-items:center;justify-content:space-between;margin-top:24px;padding-top:18px;border-top:1px solid #2a3358}}
.foot .cta{{font-size:22px;font-weight:800}}
.foot .url{{color:#ffd24a;font-size:20px;font-weight:800}}
.foot .date{{color:#5a648c;font-size:14px;margin-top:2px}}
</style></head><body>
<div class="card">
  {f'<div class="brand"><img src="{logo_data_uri()}" alt=""><div class="bn">Fisioterapia &amp; Futbolito FC<small>⚽ el fútbol lo ponemos nosotros, la fisioterapia la pone la edad</small></div></div>' if logo_data_uri() else ''}
  <div class="kick">Quiniela Mundial 2026 · Cierre</div>
  <div class="h1">🏆 ¡Ya hay campeón!</div>
  <div class="sub">Y no depende de la final: la polla ya está ganada.</div>

  <div class="champ">
    {fl('ESP', 160)}
    <div>
      <div class="lbl">🥇 Campeón de la quiniela</div>
      <div class="who">Boris Tapia V</div>
      <div class="note">Campeón: España · líder de punta a punta (13 exactos)</div>
    </div>
    <div class="pts"><b>349 pts</b><span>$25.000</span></div>
  </div>

  <table>{TRS}</table>

  <div class="live-h">🔥 Lo único que aún se juega (no cambia el sobre)</div>
  <div class="live-s">La final y el 3er puesto solo definen puntos finales y la Bota de Oro.</div>
  <div class="tiles">
    <div class="tile">
      <div class="tt">👑 Especial de campeón · +50</div>
      <div class="big">{fl('ESP',40)}España en la final</div>
      <div class="who">Si España es campeón → <b>Boris</b> y <b>Paulo</b> +50.<br>Rival: {fl('ARG',40)}Argentina (nadie la eligió campeón).</div>
      <div class="when">🗓️ Final · dom 19-jul</div>
    </div>
    <div class="tile">
      <div class="tt">⚽ Bota de Oro · +25</div>
      <div class="big">{fl('FRA',40)}Mbappé 8 · vs · 8 Messi{fl('ARG',40)}</div>
      <div class="who"><b>Mbappé</b>: Boris · Carlos · Andrés<br><b>Messi</b>: Paulo</div>
      <div class="when">🗓️ Mbappé juega el 3er puesto (18-jul) · Messi la final (19-jul)</div>
    </div>
  </div>

  <div class="foot">
    <div><div class="cta">Gracias por jugar 🍻</div><div class="date">Cierre · 16-jul-2026</div></div>
    <div class="url">{SITE_URL}</div>
  </div>
</div></body></html>"""


def render(slug='cierre-mundial', h=1200):
    os.makedirs(OUTDIR, exist_ok=True)
    htmlpath = os.path.join(OUTDIR, f'{slug}.html')
    pngpath = os.path.join(OUTDIR, f'{slug}.png')
    with open(htmlpath, 'w', encoding='utf-8') as f:
        f.write(HTML)
    edges = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
             r'C:\Program Files\Microsoft\Edge\Application\msedge.exe']
    edge = next((e for e in edges if os.path.exists(e)), None)
    if not edge:
        print(f'HTML generado: {htmlpath} (Edge no encontrado)')
        return
    url = 'file:///' + htmlpath.replace('\\', '/')
    subprocess.run([edge, '--headless', '--disable-gpu', '--hide-scrollbars',
                    f'--window-size=1000,{h}', '--virtual-time-budget=9000',
                    f'--screenshot={pngpath}', url], check=False)
    print(f'PNG: {pngpath}')


if __name__ == '__main__':
    render()
