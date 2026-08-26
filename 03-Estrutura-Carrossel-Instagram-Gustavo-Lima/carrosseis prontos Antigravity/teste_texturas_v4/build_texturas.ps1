$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$templatePath = Join-Path $scriptDir 'template_texturas.html'
$outputPath = Join-Path $scriptDir 'carrossel_texturas.html'

Write-Host 'BUILD Iniciado' -ForegroundColor Cyan

# No images to inject for this test, just copy template to output
$html = Get-Content -Path $templatePath -Raw -Encoding UTF8
[System.IO.File]::WriteAllText($outputPath, $html, [System.Text.Encoding]::UTF8)

Write-Host 'BUILD CONCLUIDO!' -ForegroundColor Cyan

# Tentativa de abrir no Edge explicitamente, se falhar abre padrão
try {
    Start-Process "msedge.exe" $outputPath -ErrorAction Stop
} catch {
    Start-Process $outputPath
}
