$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$assets = Join-Path $root 'assets'

function DataUri([string]$path, [string]$mime) {
  $bytes = [System.IO.File]::ReadAllBytes($path)
  return 'data:' + $mime + ';base64,' + [Convert]::ToBase64String($bytes)
}

$template = Get-Content -Raw -LiteralPath (Join-Path $root 'template_cultura.html')
$template = $template.Replace('FONT_DATA_HERE', (DataUri (Join-Path $assets 'Montserrat-Variable.ttf') 'font/ttf'))
$template = $template.Replace('COVER_DATA_HERE', (DataUri (Join-Path $assets 'cover-cultura.png') 'image/png'))
$template = $template.Replace('SKETCH_ORG_DATA_HERE', (DataUri (Join-Path $assets 'sketch-organograma.png') 'image/png'))
$template = $template.Replace('SKETCH_PAUSA_DATA_HERE', (DataUri (Join-Path $assets 'sketch-pausa.png') 'image/png'))
$template = $template.Replace('SKETCH_PART_DATA_HERE', (DataUri (Join-Path $assets 'sketch-participacao.png') 'image/png'))
$template = $template.Replace('__HTML2CANVAS_JS__', (Get-Content -Raw -LiteralPath (Join-Path $assets 'html2canvas.min.js')))
$template = $template.Replace('__JSPDF_JS__', (Get-Content -Raw -LiteralPath (Join-Path $assets 'jspdf.umd.min.js')))

$out = Join-Path $root 'carrossel_cultura.html'
[System.IO.File]::WriteAllText($out, $template, [System.Text.UTF8Encoding]::new($false))
Write-Host "HTML final criado em $out"
