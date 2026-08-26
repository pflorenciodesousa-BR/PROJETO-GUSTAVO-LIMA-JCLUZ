$ErrorActionPreference = 'Stop'

$scriptDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$brainDir     = 'C:\Users\Jcluz\.gemini\antigravity\brain\6fde117d-5946-4b52-879c-752f25fa6ead'
$templatePath = Join-Path $scriptDir 'template_cnpj_cpf.html'
$outputPath   = Join-Path $scriptDir 'carrossel_cnpj_cpf_v4.html'

$images = @{
    'COVER_B64_HERE' = 'capa_cartoes_cpf_cnpj_1784636003515.png'
    'REAL_IMG_HERE'  = 'real_empresario_contrato_duvida_1784636012269.png'
    'SKETCH_B64_HERE'= 'sketch_diluicao_risco_1784636020730.png'
}

Write-Host 'BUILD CNPJ vs CPF — V4' -ForegroundColor Cyan

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




