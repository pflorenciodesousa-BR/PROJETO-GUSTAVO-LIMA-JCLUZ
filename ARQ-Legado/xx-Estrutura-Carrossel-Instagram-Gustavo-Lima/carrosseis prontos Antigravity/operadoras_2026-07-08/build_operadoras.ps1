$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_operadoras.html'
$outputPath = Join-Path $scriptDir 'carrossel_operadoras.html'

$images = @{
    'COVER_B64_HERE'   = 'cover_operadoras_boxe_v2_1783535150179.png'
    'SKETCH3_B64_HERE' = 'sketch_mapa_regional_1783534382237.png'
    'SKETCH5_B64_HERE' = 'sketch_rede_nacional_1783534389700.png'
}

Write-Host 'BUILD Iniciado' -ForegroundColor Cyan

$html = Get-Content -Path $templatePath -Raw -Encoding UTF8

foreach ($placeholder in $images.Keys) {
    $imgFile = Join-Path $brainDir $images[$placeholder]
    if (-not (Test-Path $imgFile)) {
        Write-Host "ERRO: Arquivo nao encontrado: $imgFile" -ForegroundColor Red
        exit 1
    }
    $bytes = [System.IO.File]::ReadAllBytes($imgFile)
    $b64 = [Convert]::ToBase64String($bytes)
    $dataUri = 'data:image/png;base64,' + $b64
    $html = $html.Replace($placeholder, $dataUri)
    Write-Host "Injetado: $placeholder" -ForegroundColor Green
}

[System.IO.File]::WriteAllText($outputPath, $html, [System.Text.Encoding]::UTF8)
Write-Host 'BUILD CONCLUIDO!' -ForegroundColor Cyan
Start-Process $outputPath
