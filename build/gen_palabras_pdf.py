#!/usr/bin/env python
"""PDF de las 'Palabras de Entrega' de la quiniela, a partir del .md fuente.

Convierte diplomas/palabras-entrega.md -> HTML pergamino (mismo look que los
diplomas) -> PDF A4 vertical via Edge --print-to-pdf. Una pagina por seccion
(portada+apertura juntas; luego un homenajeado por pagina) para leer en voz alta.

Uso: python build/gen_palabras_pdf.py [diplomas/palabras-entrega-vN.md]
     (sin argumento usa palabras-entrega.md; con argumento deriva los nombres
      de salida .html/.pdf del mismo stem, para versiones que no pisen la actual)
"""
import os, re, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from gen_tarjeta import logo_data_uri, HERE

MD = os.path.join(HERE, 'diplomas', 'palabras-entrega.md')
OUT_HTML = os.path.join(HERE, 'diplomas', 'palabras-entrega.html')
OUT_PDF = os.path.join(HERE, 'diplomas', 'palabras-entrega.pdf')


def inline(t):
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t


def md_to_body(md):
    parts, para, quote = [], [], []
    sec = 0

    def flush_para():
        if para:
            parts.append('<p>' + ' '.join(para) + '</p>')
            para.clear()

    def flush_quote():
        if quote:
            parts.append('<blockquote>' + '<br>'.join(quote) + '</blockquote>')
            quote.clear()

    for raw in md.split('\n'):
        s = raw.strip()
        if s.startswith('> '):
            flush_para()
            quote.append(inline(s[2:]))
            continue
        flush_quote()
        if not s:
            flush_para()
        elif s.startswith('### '):
            flush_para(); parts.append('<h3>' + inline(s[4:]) + '</h3>')
        elif s.startswith('## '):
            flush_para()
            if sec:
                parts.append('</section>')
            cls = ' class="first"' if sec == 0 else ''
            parts.append(f'<section{cls}>')
            sec += 1
            parts.append('<h2>' + inline(s[3:]) + '</h2>')
        elif s.startswith('# '):
            flush_para(); parts.append('<h1>' + inline(s[2:]) + '</h1>')
        elif s == '---':
            flush_para()
        else:
            para.append(inline(s))
    flush_para(); flush_quote()
    if sec:
        parts.append('</section>')
    return '\n'.join(parts)


def build_html(md):
    logo = logo_data_uri()
    crest = f'<img class="crest" src="{logo}" alt="">' if logo else ''
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 22mm 22mm 20mm; }}
*{{margin:0;box-sizing:border-box}}
html{{background:radial-gradient(130% 90% at 50% 0%,#fbf6e8 0%,#f3e9d0 70%,#ecdfbf 100%);
  -webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:Cambria,Georgia,'Times New Roman',serif;color:#20263c;
  font-size:16.5px;line-height:1.62}}
.crest{{display:block;width:74px;height:74px;object-fit:contain;margin:0 auto 10px}}
h1{{font-size:31px;font-weight:700;text-align:center;letter-spacing:.01em;
  line-height:1.15;margin-bottom:6px}}
h1+h3{{text-align:center;font-weight:400;font-style:italic;color:#8a7130;
  font-size:15px;letter-spacing:.02em;border:0;margin:0 0 14px;padding:0}}
h2{{font-size:25px;font-weight:700;color:#1a2340;margin:0 0 2px;
  border-bottom:2px solid #cbb867;padding-bottom:8px}}
h3{{font-size:15.5px;font-weight:400;font-style:italic;color:#b8902f;
  letter-spacing:.03em;margin:4px 0 16px}}
p{{margin:0 0 13px;text-align:justify;break-inside:avoid}}
strong{{color:#8a6a1f}}
blockquote{{background:#f6efdb;border-left:3px solid #cbb867;border-radius:0 8px 8px 0;
  padding:14px 20px;margin:0 0 20px;font-size:13.5px;line-height:1.6;color:#4a4636;
  font-style:italic;break-inside:avoid}}
blockquote strong{{font-style:normal;color:#8a6a1f}}
section{{break-before:page}}
section.first{{break-before:auto}}
section h2{{break-after:avoid}}
.close{{text-align:center;font-style:italic;color:#6a6048;margin-top:8px}}
</style></head><body>
{crest}
{md_to_body(md)}
</body></html>"""


def main():
    md_path = MD
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        md_path = arg if os.path.isabs(arg) else os.path.join(HERE, arg)
    stem = os.path.splitext(md_path)[0]
    out_html, out_pdf = stem + '.html', stem + '.pdf'
    if not os.path.exists(md_path):
        print(f'No existe {md_path}')
        return
    with open(md_path, encoding='utf-8') as f:
        md = f.read()
    html = build_html(md)
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html)
    edge = next((e for e in (
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe') if os.path.exists(e)), None)
    if not edge:
        print(f'HTML: {out_html} (Edge no encontrado — sin PDF)')
        return
    url = 'file:///' + out_html.replace('\\', '/')
    subprocess.run([edge, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                    '--virtual-time-budget=9000', f'--print-to-pdf={out_pdf}', url],
                   check=False)
    print(f'PDF: {out_pdf}')


if __name__ == '__main__':
    main()
