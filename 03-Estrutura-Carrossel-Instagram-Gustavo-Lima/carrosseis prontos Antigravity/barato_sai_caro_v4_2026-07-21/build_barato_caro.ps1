$ErrorActionPreference = 'Stop'

$scriptDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir     = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_barato_caro.html'
$outputPath   = Join-Path $scriptDir 'carrossel_barato_caro_v4.html'

$images = @{
    'COVER_B64_HERE' = 'capa_rato_ratoeira_v2_1784637674048.png'
    'REAL_IMG_HERE'  = 'real_paciente_conta_assustado_1784636841672.png'
    'SKETCH_B64_HERE'= 'sketch_iceberg_contrato_1784636849526.png'
}

Write-Host 'BUILD Barato Sai Caro — V4' -ForegroundColor Cyan

$html = Get-Content -Path $templatePath -Raw -Encoding UTF8

foreach ($placeholder in $images.Keys) {
    $imgFile = Join-Path $brainDir $images[$placeholder]
    if (-not (Test-Path $imgFile)) {
        Write-Host "AVISO: Imagem nao encontrada ($placeholder): $($images[$placeholder])" -ForegroundColor Yellow
        continue
    }
    $bytes = [System.IO.File]::ReadAllBytes($imgFile)
    $b64   = [Convert]::ToBase64String($bytes)
    $uri   = 'data:image/png;base64,' + $b64
    $html  = $html.Replace($placeholder, $uri)
    Write-Host "OK: $placeholder" -ForegroundColor Green
}

[System.IO.File]::WriteAllText($outputPath, $html, [System.Text.Encoding]::UTF8)
Write-Host 'BUILD CONCLUIDO!' -ForegroundColor Cyan





