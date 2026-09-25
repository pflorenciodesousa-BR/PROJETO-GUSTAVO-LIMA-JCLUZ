$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_enfermaria_v4.html'
$outputPath = Join-Path $scriptDir 'carrossel_enfermaria_v4.html'

$images = @{
    'COVER_B64_HERE'   = 'cover_chapeuzinho_1782408157445.png'
    'REAL_IMG_HERE'    = 'real_hospital_corridor_1784036804432.png'
    'SKETCH2_B64_HERE' = 'sketch_leito_hospital_1782408168089.png'
}

Write-Host 'BUILD Iniciado - V4' -ForegroundColor Cyan

$html = Get-Content -Path $templatePath -Raw -Encoding UTF8

foreach ($placeholder in $images.Keys) {
    $imgFile = Join-Path $brainDir $images[$placeholder]
    if (-not (Test-Path $imgFile)) {
        Write-Host "AVISO: Imagem pendente ($placeholder): $($images[$placeholder])" -ForegroundColor Yellow
        continue
    }
    $bytes = [System.IO.File]::ReadAllBytes($imgFile)
    $b64 = [Convert]::ToBase64String($bytes)
    $dataUri = 'data:image/png;base64,' + $b64
    $html = $html.Replace($placeholder, $dataUri)
    Write-Host "Injetado: $placeholder" -ForegroundColor Green
}

[System.IO.File]::WriteAllText($outputPath, $html, [System.Text.Encoding]::UTF8)
Write-Host 'BUILD CONCLUIDO!' -ForegroundColor Cyan

# Abre no Edge ou default browser
try {
    Start-Process "msedge.exe" $outputPath -ErrorAction Stop
} catch {
    Start-Process $outputPath
}

