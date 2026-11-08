from pathlib import Path
import base64, json, re, html

base = Path(__file__).resolve().parent
source = (base / 'template_sextou.html').read_text(encoding='utf-8')
caption = (base / 'legenda.txt').read_text(encoding='utf-8').strip()
assets = {
    '__FONT_DATA__': ('Montserrat-Variable.ttf', 'font/ttf'),
    '__COVER_DATA__': ('capa-original.jpg', 'image/jpeg'),
    '__TEAM_DATA__': ('equipe-original.jpg', 'image/jpeg'),
    '__PARTY_DATA__': ('festa-original.jpg', 'image/jpeg'),
}
for token, (name, mime) in assets.items():
    source = source.replace(token, 'data:' + mime + ';base64,' + base64.b64encode((base / 'assets' / name).read_bytes()).decode('ascii'))
for token, name in [('__HTML2CANVAS_JS__', 'html2canvas.min.js'), ('__JSPDF_JS__', 'jspdf.umd.min.js'), ('__JSZIP_JS__', 'jszip.min.js')]:
    source = source.replace(token, (base / 'assets' / name).read_text(encoding='utf-8'))
source = source.replace('__CAPTION_JSON__', json.dumps(caption, ensure_ascii=False))
source = source.replace('__ENGINE_JS__', (base / 'engine.js').read_text(encoding='utf-8'))
assert not re.search(r'__[A-Z_]+__', source), 'Unresolved placeholder'
(base / 'carrossel_sextou.html').write_text(source, encoding='utf-8')
scripts = ['SEXTOU: A SEXTA QUE MOVIMENTA O SALÃO', '7 slides | 6 de novembro de 2026 | Gustavo Lima', '']
for i, slide in enumerate(re.findall(r'<template data-slide-template>(.*?)</template>', source, re.S), 1):
    text = re.sub(r'<br\s*/?>', ' ', slide)
    text = re.sub(r'</(?:p|h2|div)>', '\n', text)
    text = html.unescape(re.sub(r'<[^>]+>', '', text))
    lines = [re.sub(r'\s+', ' ', line).strip() for line in text.splitlines()]
    scripts.extend([f'SLIDE {i}', '\n\n'.join(line for line in lines if line), ''])
scripts.extend(['LEGENDA', caption])
(base / 'roteiro.txt').write_text('\n\n'.join(scripts), encoding='utf-8')
print(base / 'carrossel_sextou.html')
