from pathlib import Path
import base64, json, re, html

base = Path(__file__).resolve().parent
source = (base / 'template_bom_salao.html').read_text(encoding='utf-8')
source = source.replace('__VIEWER_CSS__', (base / 'viewer.css').read_text(encoding='utf-8'))
caption = (base / 'legenda.txt').read_text(encoding='utf-8').strip()
assets = {
    '__FONT_DATA__': ('Montserrat-Variable.ttf', 'font/ttf'),
    '__COVER_DATA__': ('capa_atendimento_contra_plonge_v2.png', 'image/png'),
    '__SCENE_DATA__': ('cena_atendimento_vertical.png', 'image/png'),
}
for token, (name, mime) in assets.items():
    source = source.replace(token, 'data:' + mime + ';base64,' + base64.b64encode((base / 'assets' / name).read_bytes()).decode('ascii'))
for token, name in [('__HTML2CANVAS_JS__', 'html2canvas.min.js'), ('__JSPDF_JS__', 'jspdf.umd.min.js'), ('__JSZIP_JS__', 'jszip.min.js')]:
    source = source.replace(token, (base / 'assets' / name).read_text(encoding='utf-8'))
source = source.replace('__CAPTION_JSON__', json.dumps(caption, ensure_ascii=False))
source = source.replace('__ENGINE_JS__', (base / 'engine.js').read_text(encoding='utf-8'))
assert not re.search(r'__[A-Z_]+__', source), 'Unresolved placeholder'
(base / 'carrossel_bom_salao.html').write_text(source, encoding='utf-8')
scripts = ['UM BOM SALÃO DE VENDAS', '7 slides | 13 de novembro de 2026 | Gustavo Lima', 'Imagens geradas para cenas ilustrativas.']
for i, slide in enumerate(re.findall(r'<template data-slide-template>(.*?)</template>', source, re.S), 1):
    text = re.sub(r'<br\s*/?>', ' ', slide)
    text = re.sub(r'</(?:p|h2|div)>', '\n', text)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', text))
    lines = [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines()]
    scripts.extend([f'SLIDE {i}', '\n\n'.join(line for line in lines if line), ''])
scripts.extend(['LEGENDA', caption])
(base / 'roteiro.txt').write_text('\n\n'.join(scripts), encoding='utf-8')
print(base / 'carrossel_bom_salao.html')
