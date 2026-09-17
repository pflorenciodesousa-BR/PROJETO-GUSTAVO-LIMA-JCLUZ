$ErrorActionPreference = 'Stop'

$scriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir   = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_rede_credenciada.html'
$outputPath   = Join-Path $scriptDir 'carrossel_rede_credenciada_v4.html'

$images = @{
    'COVER_B64_HERE' = 'capa_medico_barrando_casal_1784573066384.png'
    'REAL_IMG_HERE'  = 'real_familia_preocupada_hospital_1784573076502.png'
    'SKETCH_B64_HERE'= 'sketch_pdf_vs_lista_oficial_1784573085158.png'
}

Write-Host 'BUILD Rede Credenciada — V4' -ForegroundColor Cyan

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




