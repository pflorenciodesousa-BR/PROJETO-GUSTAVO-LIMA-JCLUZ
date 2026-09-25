$imgPath = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\concept_reajuste_bg1_1781540587544.png'
$bytes = [System.IO.File]::ReadAllBytes($imgPath)
$b64   = [System.Convert]::ToBase64String($bytes)
$bgUrl = "data:image/png;base64,$b64"

$html = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Protótipo: Reajuste Empresarial</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;display:flex;justify-content:center;gap:60px;padding:50px;font-family:'Montserrat',sans-serif;}
.slide{
  width:1080px;height:1350px;
  background-image:url(`'$bgUrl`');
  background-size:cover;
  background-position:center;
  position:relative;
  display:flex;flex-direction:column;
  justify-content:center;align-items:center;
  transform:scale(0.6);
  transform-origin:top center;
  margin-bottom:-540px;
  border-radius:12px;
  overflow:hidden;
  box-shadow: 0 15px 40px rgba(0,0,0,0.8);
}
.glass-card {
  background: rgba(11, 29, 58, 0.45);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-radius: 40px;
  border: 1.5px solid rgba(255, 255, 255, 0.15);
  border-top: 1.5px solid rgba(255, 255, 255, 0.35);
  border-left: 1.5px solid rgba(255, 255, 255, 0.25);
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
  padding: 80px 60px;
  width: 86%;
  display:flex; flex-direction:column;
}

.t-tag  {font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:rgba(255,255,255,0.40);margin-bottom:24px}
.accent-line{width:52px;height:4px;background:#60a5fa;border-radius:2px;margin-bottom:34px}
.t-bold {font-size:62px;font-weight:900;color:#fff;line-height:1.20;letter-spacing:-.8px}
.t-reg  {font-size:46px;font-weight:400;color:rgba(255,255,255,0.75);line-height:1.45;letter-spacing:-.5px}
.t-accent{color:#60a5fa}
.sp-lg{height:54px}
.hl{background:rgba(245,158,11,0.24);border-radius:6px;padding:4px 12px;display:inline;-webkit-box-decoration-break:clone;box-decoration-break:clone}

.brand{position:absolute;top:60px;left:0;right:0;text-align:center;font-size:18px;font-weight:700;letter-spacing:4px;text-transform:uppercase;color:rgba(255,255,255,0.25)}

</style>
</head>
<body>

  <!-- SLIDE CONTEXTO 1 -->
  <div class="slide">
    <div class="brand">@gustavojcluz</div>
    <div class="glass-card">
      <div class="t-tag">o pesadelo do empresário</div>
      <div class="accent-line"></div>
      <div class="t-bold">O reajuste<br><span class="t-accent">chegou.</span></div>
      <div class="sp-lg"></div>
      <div class="t-reg">Seu plano empresarial sofreu<br>um aumento absurdo e você<br>não sabe o porquê.</div>
    </div>
  </div>

</body>
</html>
"@

$outHtml = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\carencia-pegadinha_2026-06-15\prototipo_reajuste.html"
[System.IO.File]::WriteAllText($outHtml, $html, [System.Text.Encoding]::UTF8)
Write-Host "Prototipo Reajuste criado com sucesso!"
