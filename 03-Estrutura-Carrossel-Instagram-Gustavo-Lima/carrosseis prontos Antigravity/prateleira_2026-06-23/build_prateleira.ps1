$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_prateleira.html'
$outputPath = Join-Path $scriptDir 'carrossel_prateleira.html'

$images = @{
    'COVER_B64_HERE' = 'cover_prateleira_1782225155747.png'
    'SKETCH2_B64_HERE' = 'sketch_slide2_1782225173686.png'
    'SKETCH4_B64_HERE' = 'sketch_slide4_1782225189556.png'
    'SKETCH6_B64_HERE' = 'sketch_slide6_unidunite_1782231367950.png'
    'SKETCH7_B64_HERE' = 'sketch_slide7_1782225218259.png'
}

Write-Host 'BUILD Iniciado' -ForegroundColor Cyan

$html = Get-Content -Path $templatePath -Raw -Encoding UTF8

foreach ($placeholder in $images.Keys) {
    $imgFile = Join-Path $brainDir $images[$placeholder]
    
    if (-not (Test-Path $imgFile)) {
        Write-Host "ERRO: $imgFile" -ForegroundColor Red
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
