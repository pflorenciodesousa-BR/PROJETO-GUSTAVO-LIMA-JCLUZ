from pathlib import Path
import html, json, subprocess, zipfile

base = Path(__file__).resolve().parent
root = base.parent
probe = r'C:\Users\Jcluz\AppData\Local\CapCut\Apps\9.7.1.4203\ffprobe.exe'
ffmpeg = r'C:\Users\Jcluz\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe'
durations = [8, 17, 21, 22, 27, 23, 12]
labels = ['Capa', 'Segundo gancho', 'Convivência', 'O nosso Sextou', 'União e afinidade', 'Cultura', 'Convite']
manifest = []
cards = []
for i, (duration, label) in enumerate(zip(durations, labels), 1):
    video = base / 'videos' / f'sextou_slide_{i:02}.mp4'
    command = [probe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)]
    metadata = json.loads(subprocess.check_output(command))
    streams = metadata['streams']
    assert len(streams) == 1 and streams[0]['codec_type'] == 'video'
    stream = streams[0]
    assert stream['codec_name'] == 'h264'
    assert (stream['width'], stream['height']) == (1080, 1350)
    assert stream['pix_fmt'] == 'yuv420p' and stream['r_frame_rate'] == '30/1'
    assert stream['sample_aspect_ratio'] == '1:1'
    assert abs(float(metadata['format']['duration']) - duration) < .05
    raw = video.read_bytes()
    assert raw.find(b'moov') < raw.find(b'mdat'), 'Faststart ausente'
    decode = subprocess.run([ffmpeg, '-v', 'error', '-xerror', '-i', str(video), '-f', 'null', '-'], capture_output=True)
    assert decode.returncode == 0, decode.stderr.decode(errors='replace')
    subprocess.run([ffmpeg, '-y', '-v', 'error', '-ss', '2.5', '-i', str(video), '-frames:v', '1', str(base / 'qa' / f'encoded_{i:02}.png')], check=True)
    manifest.append({'slide': i, 'file': video.name, 'duration': duration, 'dimensions': [1080, 1350], 'fps': 30, 'codec': stream['codec_name'], 'pix_fmt': stream['pix_fmt'], 'audio': False, 'faststart': True, 'size_bytes': video.stat().st_size, 'decoded_without_errors': True})
    cards.append(f'''<article><div class="label"><strong>SLIDE {i:02}</strong><span>{label} · {duration}s</span></div><video controls muted playsinline preload="metadata" poster="pngs/slide_{i:02}.png"><source src="animado/videos/{video.name}" type="video/mp4"></video><div class="buttons"><button type="button" onclick="replay(this)">Rever animação</button><a href="animado/videos/{video.name}" download>Baixar MP4</a></div></article>''')
    print(f'Slide {i:02}: validado ({duration}s).', flush=True)

with zipfile.ZipFile(root / 'sextou_animado_7_videos.zip', 'w', compression=zipfile.ZIP_STORED) as z:
    for row in manifest:
        z.write(base / 'videos' / row['file'], row['file'])
(base / 'validation.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

caption = html.escape((root / 'legenda.txt').read_text(encoding='utf-8'))
gallery = '''<!doctype html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sextou · Carrossel animado</title><style>
@font-face{font-family:Montserrat;src:url('assets/Montserrat-Variable.ttf');font-weight:100 900}*{box-sizing:border-box}body{margin:0;background:#f0ebe3;color:#0b1d3a;font-family:Montserrat,Arial,sans-serif}header{padding:30px max(24px,calc((100vw - 1320px)/2));background:#0b1d3a;color:#fff}h1{font-size:28px;letter-spacing:-.8px;margin:0 0 10px}header p{font-size:14px;line-height:1.5;margin:0 0 18px;color:#d1dce8}a,button{font:700 13px Montserrat,Arial,sans-serif;text-decoration:none;border:0;cursor:pointer;border-radius:10px;padding:12px 16px;display:inline-block;background:#0b1d3a;color:#fff}.download-all{background:#eab308;color:#0b1d3a}.grid{max-width:1368px;padding:30px 24px;margin:auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px}article{min-width:0}.label{display:flex;justify-content:space-between;gap:10px;margin-bottom:10px;font-size:12px}video{display:block;width:100%;aspect-ratio:4/5;background:#0b1d3a;border-radius:18px}.buttons{display:flex;gap:10px;justify-content:center;margin-top:12px}.buttons button{background:#fff;color:#0b1d3a}.caption{max-width:850px;margin:0 auto 45px;padding:24px}h2{font-size:20px}textarea{width:100%;min-height:360px;resize:vertical;border:1px solid #cbd0d7;background:#fff;padding:20px;border-radius:14px;font:15px/1.65 Montserrat,Arial,sans-serif;color:#0b1d3a}.caption button{margin-top:12px}.note{font-size:13px;line-height:1.5}footer{text-align:center;padding:15px 24px 35px;font-size:12px}footer a{background:transparent;color:#0b1d3a;text-decoration:underline;padding:0}@media(max-width:620px){header{padding:24px 18px}h1{font-size:23px}.grid{padding:24px 16px;grid-template-columns:1fr}}</style></head><body><header><h1>SEXTOU · CARROSSEL ANIMADO</h1><p>7 vídeos separados · 1080 × 1350 · Sem áudio<br>Entradas suaves, fotos em movimento e pausa para leitura.</p><a class="download-all" href="sextou_animado_7_videos.zip" download>Baixar os 7 vídeos em ZIP</a></header><main class="grid">''' + '\n'.join(cards) + '''</main><section class="caption"><h2>Legenda da postagem</h2><textarea id="caption" readonly>''' + caption + '''</textarea><button onclick="copyCaption(this)">Copiar legenda</button><p class="note">Os vídeos estão numerados na ordem do carrossel, do 01 ao 07.</p></section><footer><a href="carrossel_sextou.html">Abrir a versão em imagens</a></footer><script>
function replay(button){const v=button.closest('article').querySelector('video');v.currentTime=0;v.play()}
document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(other=>{if(other!==v)other.pause()})));
async function copyCaption(btn){const t=document.getElementById('caption');try{await navigator.clipboard.writeText(t.value);btn.textContent='Legenda copiada!'}catch(e){t.select();btn.textContent='Legenda selecionada para copiar'}}
</script></body></html>'''
(root / 'carrossel_sextou_animado.html').write_text(gallery, encoding='utf-8')
print('ZIP, visualizador e validação finalizados.')
