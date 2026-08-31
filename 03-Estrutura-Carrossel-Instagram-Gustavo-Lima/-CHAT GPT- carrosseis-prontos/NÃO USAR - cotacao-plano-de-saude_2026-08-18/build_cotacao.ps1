$ErrorActionPreference = 'Stop'
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $projectDir 'template_cotacao_plano_de_saude.html'
$outputPath = Join-Path $projectDir 'carrossel_cotacao_plano_de_saude_v4.html'

function Get-DataUri([string]$relativePath) {
    $fullPath = Join-Path $projectDir $relativePath
    $extension = [IO.Path]::GetExtension($fullPath).TrimStart('.').ToLowerInvariant()
    $mime = if ($extension -eq 'jpg' -or $extension -eq 'jpeg') { 'image/jpeg' } else { "image/$extension" }
    $bytes = [IO.File]::ReadAllBytes($fullPath)
    return "data:$mime;base64,$([Convert]::ToBase64String($bytes))"
}

$html = [IO.File]::ReadAllText($templatePath)
$html = $html.Replace('__COVER_DATA__', (Get-DataUri 'assets\capa-cotacao-iceberg-v3.png'))
$html = $html.Replace('__FAMILY_DATA__', (Get-DataUri 'assets\familia-comparando-planos.png'))
$html = $html.Replace('__SKETCH_DATA__', (Get-DataUri 'assets\sketch-cotacao.png'))
$html = $html.Replace('__PROCESS_SKETCH_DATA__', (Get-DataUri 'assets\sketch-processo-consultoria-v4.png'))
$html = $html.Replace('__HTML2CANVAS_JS__', [IO.File]::ReadAllText((Join-Path $projectDir 'assets\html2canvas.min.js')))
$html = $html.Replace('__JSPDF_JS__', [IO.File]::ReadAllText((Join-Path $projectDir 'assets\jspdf.umd.min.js')))
[IO.File]::WriteAllText($outputPath, $html, [Text.UTF8Encoding]::new($false))
Write-Output $outputPath
