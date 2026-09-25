$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_presta.html'
$outputPath = Join-Path $scriptDir 'carrossel_presta.html'

$images = @{
    'COVER_B64_HERE'   = 'cover_selfie_contrato_1783620433726.png'
    'SKETCH3_B64_HERE' = 'sketch_presente_armadilha_1783619762831.png'
    'SKETCH5_B64_HERE' = 'sketch_pilha_contas_1783619769777.png'
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
