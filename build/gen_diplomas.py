#!/usr/bin/env python
"""Diplomas de cierre de la Quiniela Mundial 2026 — uno por jugador (5).

Podio (Boris/Paulo/Andres): tono elegante con guinos. Fuera del podio
(Jorge/Carlos): humor de la liga. SIN mencion de montos: puro honor.

Cada diploma se genera en dos formatos (Boris pidio ambos):
  - PNG A4 horizontal 2x (crisp, para el WhatsApp del grupo)
  - PDF A4 horizontal (imprimible)

Diseno self-contained: escudo FC embebido base64, banderas via flagcdn.
Render por Edge --headless (misma receta que gen_tarjeta/gen_cierre).

Uso:
  python build/gen_diplomas.py            # los 5
  python build/gen_diplomas.py boris      # solo uno (por slug corto)
  python build/gen_diplomas.py --v2       # sufijo -v2 en la salida (no pisa los actuales)
"""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from gen_tarjeta import logo_data_uri, SITE_URL, HERE

OUTDIR = os.path.join(HERE, 'diplomas')

ISO = {'ESP': 'es', 'ARG': 'ar', 'FRA': 'fr', 'POR': 'pt'}
NOMBRE_PAIS = {'ESP': 'España', 'ARG': 'Argentina', 'FRA': 'Francia', 'POR': 'Portugal'}
CAMP_MUERTO = {'FRA', 'POR'}  # campeones ya eliminados; ESP/ARG siguen vivos


def fl(code, w=40):
    return f'<img class="fl" src="https://flagcdn.com/w{w}/{ISO[code]}.png" alt="">'


# --- Los 5 diplomas. accent = (claro, oscuro) para sello/cinta ---
GOLD   = ('#e8c14e', '#b8902f')
SILVER = ('#cbd3e2', '#8a94a8')
BRONZE = ('#d69256', '#a9702f')
VERDE  = ('#5fae83', '#3f7d5a')
TERRA  = ('#d98a56', '#b5622f')

DIPLOMAS = [
    dict(
        slug='1-boris', rank='🥇', pos='Campeón de la Quiniela', accent=GOLD,
        name='Boris Tapia V.', champ='ESP', pts=424, exactos=13, humor=False,
        title='Primer Lugar',
        cuerpo='Por dominar el torneo de principio a fin, clavar <b>13 resultados '
               'exactos</b> —más que ningún otro—, coronar a España campeona y '
               'quedarse con la Bota de Oro. Liderato de punta a punta, sin apelación.',
        sello='CAMPEÓN',
    ),
    dict(
        slug='2-paulo', rank='🥈', pos='Subcampeón', accent=SILVER,
        name='Paulo Salas', champ='ESP', pts=349, exactos=10, humor=False,
        title='Segundo Lugar',
        cuerpo='Por una campaña sólida de comienzo a fin, <b>10 aciertos exactos</b> '
               'y el temple para blindar el segundo puesto cuando más apretaba. '
               'Escolta de lujo, España campeona hasta el final.',
        sello='SUBCAMPEÓN',
    ),
    dict(
        slug='3-andres', rank='🥉', pos='Tercer Lugar', accent=BRONZE,
        name='Andrés Acosta', champ='FRA', pts=289, exactos=9, humor=False,
        title='Tercer Lugar',
        cuerpo='Por sostener el podio hasta el final con <b>9 aciertos exactos</b> '
               'y buen ojo para el cuadro. Ni la caída de Francia en semifinales '
               'lo bajó del cajón; la Bota de Mbappé le selló el bronce.',
        sello='PODIO',
    ),
    dict(
        slug='4-carlos', rank='🎖️', pos='Mención Especial', accent=TERRA,
        name='Carlos Salgado', champ='POR', pts=253, exactos=9, humor=True,
        title='El Líder que Cayó y Resucitó',
        cuerpo='Por comandar la pelea por el podio durante semanas… hasta que '
               'Portugal se despidió y lo mandó al fondo. Pero en el último día '
               'la Bota de Oro le devolvió el guiño: su apuesta por <b>Mbappé</b> '
               'le sumó 25 puntos y lo trepó de vuelta al cuarto lugar. Cerró con '
               '<b>9 aciertos exactos</b>: cayó con su campeón, se levantó para el final.',
        sello='LA LIGA',
    ),
    dict(
        slug='5-jorge', rank='🎖️', pos='Mención de Honor', accent=VERDE,
        name='Jorge Vásquez', champ='FRA', pts=253, exactos=8, humor=True,
        title='El que Remó desde el Fondo',
        cuerpo='Por escalar desde el último lugar de la tabla hasta pelear el podio, '
               'y por ser el más certero de todos leyendo las llaves de eliminatorias. '
               'Confió el título de goleador a <b>Deniz Undav</b> — acto de fe que el '
               'fútbol, cruelmente, no premió 💀. Rey de los cruces, paciencia de santo.',
        sello='CORAZÓN',
    ),
]


def diploma_html(d):
    ac_l, ac_d = d['accent']
    muerto = d['champ'] in CAMP_MUERTO
    champ_html = f'{fl(d["champ"],40)} {NOMBRE_PAIS[d["champ"]]}{" 💀" if muerto else ""}'
    eyebrow_extra = ' · con todo el cariño de la liga' if d['humor'] else ''
    logo = logo_data_uri()
    brand = (f'<img class="crest" src="{logo}" alt="">' if logo else '')
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
@page {{ size: A4 landscape; margin: 0; }}
*{{margin:0;box-sizing:border-box}}
html,body{{width:1123px;height:794px}}
body{{-webkit-print-color-adjust:exact;print-color-adjust:exact;
  font-family:Cambria,Georgia,'Times New Roman',serif}}
.page{{position:relative;width:1123px;height:794px;overflow:hidden;
  background:radial-gradient(120% 120% at 50% 0%,#fbf6e8 0%,#f3e9d0 62%,#ecdfbf 100%);
  color:#1a2340}}
.frame{{position:absolute;inset:26px;border:3px solid #1a2340;border-radius:6px}}
.frame::after{{content:'';position:absolute;inset:7px;border:1.5px solid {ac_d};border-radius:4px}}
.corner{{position:absolute;font-size:30px;color:{ac_d};line-height:1;z-index:3}}
.corner.tl{{top:40px;left:44px}} .corner.tr{{top:40px;right:44px;transform:scaleX(-1)}}
.corner.bl{{bottom:40px;left:44px;transform:scaleY(-1)}}
.corner.br{{bottom:40px;right:44px;transform:scale(-1,-1)}}
.inner{{position:absolute;inset:26px;display:flex;flex-direction:column;
  align-items:center;text-align:center;padding:44px 92px 34px}}
.crest{{width:64px;height:64px;object-fit:contain}}
.club{{font-family:'Segoe UI',system-ui,sans-serif;font-size:13px;font-weight:700;
  letter-spacing:.16em;text-transform:uppercase;color:#5a4a22;margin-top:8px}}
.torneo{{font-family:'Segoe UI',system-ui,sans-serif;font-size:11px;letter-spacing:.28em;
  text-transform:uppercase;color:#9a8a5a;margin-top:3px}}
.rule{{width:120px;height:2px;margin:14px 0 8px;
  background:linear-gradient(90deg,transparent,{ac_d},transparent)}}
.diploma{{font-size:15px;letter-spacing:.42em;text-transform:uppercase;
  color:{ac_d};font-weight:700;font-family:'Segoe UI',system-ui,sans-serif}}
.pos{{font-size:34px;font-weight:700;margin-top:2px;font-style:italic}}
.otorga{{font-size:15px;color:#4a4636;margin-top:14px;font-style:italic}}
.name{{font-size:52px;font-weight:700;letter-spacing:.01em;line-height:1.05;margin:4px 0 2px}}
.name-underline{{width:340px;height:1.5px;background:#1a2340;opacity:.35;margin:6px 0 16px}}
.cuerpo{{font-size:17.5px;line-height:1.62;color:#2a2c3a;max-width:760px}}
.cuerpo b{{color:{ac_d}}}
.stats{{display:flex;gap:0;margin-top:20px}}
.stat{{padding:0 30px;border-right:1px solid #c9bd9a}}
.stat:last-child{{border-right:0}}
.stat .v{{font-size:26px;font-weight:700;line-height:1}}
.stat .v .fl{{width:30px;border-radius:3px;vertical-align:-5px;margin-right:7px;
  box-shadow:0 1px 3px #0006}}
.stat .k{{font-family:'Segoe UI',system-ui,sans-serif;font-size:11px;letter-spacing:.14em;
  text-transform:uppercase;color:#8a7d54;margin-top:6px}}
.foot{{position:absolute;left:118px;right:118px;bottom:56px;display:flex;
  align-items:flex-end;justify-content:space-between}}
.sig{{text-align:center}}
.sig .line{{width:210px;border-top:1.3px solid #1a2340;opacity:.55;margin-bottom:5px}}
.sig .rol{{font-family:'Segoe UI',system-ui,sans-serif;font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:#6a6048}}
.sig .whom{{font-size:15px;font-style:italic;margin-top:1px}}
.when{{font-family:'Segoe UI',system-ui,sans-serif;font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;color:#8a7d54}}
/* sello circular */
.seal{{position:absolute;right:128px;bottom:120px;width:118px;height:118px;z-index:4}}
.seal .disc{{width:118px;height:118px;border-radius:50%;
  background:radial-gradient(circle at 38% 32%,{ac_l},{ac_d});
  border:3px solid #fff8;box-shadow:0 6px 16px #0004,inset 0 0 0 5px {ac_d};
  display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff}}
.seal .disc .em{{font-size:30px;line-height:1}}
.seal .disc .txt{{font-family:'Segoe UI',system-ui,sans-serif;font-size:11px;font-weight:800;
  letter-spacing:.08em;margin-top:2px;text-shadow:0 1px 2px #0006}}
.seal .rib{{position:absolute;top:96px;left:50%;width:0;height:0}}
.seal .rib::before,.seal .rib::after{{content:'';position:absolute;top:0;
  border:14px solid {ac_d};border-bottom-color:transparent;width:0;height:22px}}
.seal .rib::before{{left:-26px;transform:skewX(8deg)}}
.seal .rib::after{{left:-2px;transform:skewX(-8deg)}}
</style></head><body>
<div class="page">
  <div class="frame"></div>
  <span class="corner tl">❧</span><span class="corner tr">❧</span>
  <span class="corner bl">❧</span><span class="corner br">❧</span>
  <div class="inner">
    {brand}
    <div class="club">Fisioterapia &amp; Futbolito FC</div>
    <div class="torneo">Quiniela · Mundial 2026</div>
    <div class="rule"></div>
    <div class="diploma">Diploma{eyebrow_extra}</div>
    <div class="pos">{d['pos']}</div>
    <div class="otorga">se otorga a</div>
    <div class="name">{d['name']}</div>
    <div class="name-underline"></div>
    <div class="cuerpo">{d['cuerpo']}</div>
    <div class="stats">
      <div class="stat"><div class="v">{d['pts']}</div><div class="k">Puntos</div></div>
      <div class="stat"><div class="v">{d['exactos']}</div><div class="k">Aciertos exactos</div></div>
      <div class="stat"><div class="v">{champ_html}</div><div class="k">Su campeón</div></div>
    </div>
  </div>
  <div class="seal">
    <div class="disc"><span class="em">{d['rank']}</span><span class="txt">{d['sello']}</span></div>
    <div class="rib"></div>
  </div>
  <div class="foot">
    <div class="sig">
      <div class="line"></div>
      <div class="rol">La Casa · Comisión de la Quiniela</div>
      <div class="whom">Boris Tapia V.</div>
    </div>
    <div class="when">Copa Mundial 2026 · {SITE_URL}</div>
  </div>
</div></body></html>"""


def edge_bin():
    for e in (r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
              r'C:\Program Files\Microsoft\Edge\Application\msedge.exe'):
        if os.path.exists(e):
            return e
    return None


def render_one(d, suffix=''):
    os.makedirs(OUTDIR, exist_ok=True)
    slug = f'diploma-{d["slug"]}{suffix}'
    htmlpath = os.path.join(OUTDIR, f'{slug}.html')
    pngpath = os.path.join(OUTDIR, f'{slug}.png')
    pdfpath = os.path.join(OUTDIR, f'{slug}.pdf')
    with open(htmlpath, 'w', encoding='utf-8') as f:
        f.write(diploma_html(d))
    edge = edge_bin()
    if not edge:
        print(f'HTML: {htmlpath} (Edge no encontrado — sin PNG/PDF)')
        return
    url = 'file:///' + htmlpath.replace('\\', '/')
    # PNG 2x (crisp para WhatsApp)
    subprocess.run([edge, '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--force-device-scale-factor=2', '--window-size=1123,794',
                    '--virtual-time-budget=9000', f'--screenshot={pngpath}', url],
                   check=False)
    # PDF A4 horizontal (imprimible)
    subprocess.run([edge, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    '--virtual-time-budget=9000', f'--print-to-pdf={pdfpath}', url],
                   check=False)
    print(f'✓ {d["name"]:<18} → {slug}.png + .pdf')


def main():
    args = sys.argv[1:]
    suffix = '-v2' if '--v2' in args else ''
    args = [a for a in args if a != '--v2']
    sel = args[0].lower() if args else None
    picked = [d for d in DIPLOMAS if not sel or sel in d['slug'] or sel in d['name'].lower()]
    if not picked:
        print(f'Sin match para "{sel}". Slugs: {[d["slug"] for d in DIPLOMAS]}')
        return
    for d in picked:
        render_one(d, suffix)
    print(f'\n{len(picked)} diploma(s){" (v2)" if suffix else ""} en {OUTDIR}')


if __name__ == '__main__':
    main()
