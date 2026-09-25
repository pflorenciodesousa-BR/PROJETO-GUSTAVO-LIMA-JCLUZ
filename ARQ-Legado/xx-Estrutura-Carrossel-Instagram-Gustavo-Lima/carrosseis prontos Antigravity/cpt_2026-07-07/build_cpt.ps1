$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_cpt.html'
$outputPath = Join-Path $scriptDir 'carrossel_cpt.html'

$images = @{
    'COVER_B64_HERE'   = 'cover_cpt_roxa_v3_1783425238609.png'
    'SKETCH2_B64_HERE' = 'sketch_dps_formulario_1783424263336.png'
    'SKETCH4_B64_HERE' = 'sketch_cobertura_escudo_1783424273040.png'
    'SKETCH6_B64_HERE' = 'sketch_checklist_prancheta_1783424279749.png'
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
