$ErrorActionPreference = 'Stop'

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir   = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_cripto.html'
$outputPath   = Join-Path $scriptDir 'carrossel_cripto_v4.html'

$images = @{
    'COVER_B64_HERE' = 'capa_bitcoin_cruz_1784573579083.png'
    'REAL_IMG_HERE'  = 'real_uti_alta_complexidade_1784573591748.png'
    'SKETCH_B64_HERE'= 'sketch_bomba_contrato_1784573603136.png'
}

Write-Host 'BUILD Cripto vs Plano — V4' -ForegroundColor Cyan

$html = Get-Content -Path $templatePath -Raw -Encoding UTF8

foreach ($placeholder in $images.Keys) {
    $imgFile = Join-Path $brainDir $images[$placeholder]
    if (-not (Test-Path $imgFile)) {
        Write-Host "AVISO: Imagem nao encontrada ($placeholder): $($images[$placeholder])" -ForegroundColor Yellow
        continue
    }
    $bytes  = [System.IO.File]::ReadAllBytes($imgFile)
    $b64    = [Convert]::ToBase64String($bytes)
    $uri    = 'data:image/png;base64,' + $b64
    $html   = $html.Replace($placeholder, $uri)
    Write-Host "OK: $placeholder" -ForegroundColor Green
}

[System.IO.File]::WriteAllText($outputPath, $html, [System.Text.Encoding]::UTF8)
Write-Host 'BUILD CONCLUIDO!' -ForegroundColor Cyan




