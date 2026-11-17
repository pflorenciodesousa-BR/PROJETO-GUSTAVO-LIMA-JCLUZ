from pathlib import Path
import base64, json, re, html

base=Path(__file__).resolve().parent
content=json.loads((base/'conteudo.json').read_text(encoding='utf-8'))
source=(base/'template_beneficios.html').read_text(encoding='utf-8')
source=source.replace('__VIEWER_CSS__',(base/'viewer.css').read_text(encoding='utf-8'))
icons={
 'travel':'<rect x="110" y="160" width="270" height="300" rx="30"/><path d="M180 160v-70h130v70M180 200v220M310 200v220M150 460v30M340 460v30M45 170l80-60 30-75 25 5-5 65 80 20-10 20-85-5-80 65z"/>',
 'home':'<path d="M50 240L250 70l200 170M95 210v270h310V210M205 480V340h95v140"/><path d="M160 250h65M193 218v65M330 350v-90h50v90c0 50-50 50-50 0zM330 290h50"/>',
 'shield':'<path d="M250 60l175 60v150c0 120-175 220-175 220S75 390 75 270V120zM150 270l65 65 140-145"/>',
 'fitness':'<path d="M60 190h55v170H60zM115 150h65v250h-65zM180 245h140v60H180zM320 150h65v250h-65zM385 190h55v170h-55zM100 475c80-70 220-70 300 0"/>',
 'tooth':'<path d="M250 110c-100-90-205-10-185 110 20 100 35 270 95 270 55 0 45-160 90-160s35 160 90 160c60 0 75-170 95-270 20-120-85-200-185-110zM170 150c25-15 50-10 80 15"/>',
 'map':'<path d="M65 110l120-45 140 50 110-40v380l-110 40-140-50-120 45zM185 65v380M325 115v380"/><path d="M260 145c-55 0-95 40-95 90 0 75 95 170 95 170s95-95 95-170c0-50-40-90-95-90z"/><circle cx="260" cy="235" r="30"/>',
 'receipt':'<path d="M105 65l35 30 35-30 35 30 40-30 35 30 35-30 35 30 35-30v430l-35-30-35 30-35-30-35 30-40-30-35 30-35-30-35 30zM155 160h190M155 220h190M155 280h110M155 395h190M260 340l35 35 70-75"/>'
}
slides=[]
for b in content['beneficios']:
    sketch=f'<svg class="business-sketch" viewBox="0 0 500 550" aria-hidden="true">{icons[b["icon"]]}</svg>'
    slides.append('<template data-slide-template>'+sketch+'<div class="frame"><div class="benefit-header"><span class="ranking">'+str(b['rank'])+'º</span><h2>'+b['name']+'</h2></div><p class="benefit-hook">'+html.escape(b['hook'])+'</p><div class="benefit-rule"></div><p class="benefit-body">'+html.escape(b['body'])+'</p><div class="comp-col comment-card">'+html.escape(b['check'])+'</div></div></template>')
source=source.replace('__BENEFIT_TEMPLATES__','\n'.join(slides))
for token,name,mime in [('__FONT_DATA__','Montserrat-Variable.ttf','font/ttf'),('__COVER_DATA__','capa_urna_votacao.png','image/png')]:
    source=source.replace(token,'data:'+mime+';base64,'+base64.b64encode((base/'assets'/name).read_bytes()).decode())
for token,name in [('__HTML2CANVAS_JS__','html2canvas.min.js'),('__JSPDF_JS__','jspdf.umd.min.js'),('__JSZIP_JS__','jszip.min.js')]:
    source=source.replace(token,(base/'assets'/name).read_text(encoding='utf-8'))
source=source.replace('__CAPTION_JSON__',json.dumps(content['caption'],ensure_ascii=False))
source=source.replace('__ENGINE_JS__',(base/'engine.js').read_text(encoding='utf-8'))
assert not re.search(r'__[A-Z_]+__',source)
(base/'carrossel_beneficios.html').write_text(source,encoding='utf-8')
(base/'legenda.txt').write_text(content['caption']+'\n',encoding='utf-8')
scripts=['BENEFÍCIOS MAIS PROCURADOS','11 slides | 16 de novembro de 2026 | Gustavo Lima']
for i,slide in enumerate(re.findall(r'<template data-slide-template>(.*?)</template>',source,re.S),1):
    slide=re.sub(r'<svg.*?</svg>','',slide,flags=re.S)
    text=re.sub(r'<br\s*/?>',' ',slide)
    text=re.sub(r'</(?:p|h2|div)>','\n',text)
    text=html.unescape(re.sub(r'<[^>]+>',' ',text))
    lines=[re.sub(r'\s+',' ',line).strip() for line in text.splitlines()]
    scripts.extend([f'SLIDE {i}','\n\n'.join(line for line in lines if line),''])
scripts.extend(['LEGENDA',content['caption']])
(base/'roteiro.txt').write_text('\n\n'.join(scripts),encoding='utf-8')
print(base/'carrossel_beneficios.html')
