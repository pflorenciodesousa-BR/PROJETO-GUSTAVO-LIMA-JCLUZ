$ErrorActionPreference = 'Stop'
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $projectDir 'template_plano_agencia.html'
$outputPath = Join-Path $projectDir 'carrossel_plano_agencia.html'
$utf8 = [Text.UTF8Encoding]::new($false)
$html = [IO.File]::ReadAllText($templatePath, $utf8)

$fontPath = Join-Path $projectDir 'assets\Montserrat-Variable.ttf'
$fontData = 'data:font/ttf;base64,' + [Convert]::ToBase64String([IO.File]::ReadAllBytes($fontPath))
$html = $html.Replace('__FONT_DATA__', $fontData)
$coverPath = Join-Path $projectDir 'assets\capa-atlas-agencia-exausto-v3.png'
$coverData = 'data:image/png;base64,' + [Convert]::ToBase64String([IO.File]::ReadAllBytes($coverPath))
$html = $html.Replace('__COVER_DATA__', $coverData)
$html = $html.Replace('__HTML2CANVAS_JS__', [IO.File]::ReadAllText((Join-Path $projectDir 'assets\html2canvas.min.js'), $utf8))
$html = $html.Replace('__JSPDF_JS__', [IO.File]::ReadAllText((Join-Path $projectDir 'assets\jspdf.umd.min.js'), $utf8))
$html = $html.Replace('__JSZIP_JS__', [IO.File]::ReadAllText((Join-Path $projectDir 'assets\jszip.min.js'), $utf8))

[IO.File]::WriteAllText($outputPath, $html, $utf8)
Write-Output $outputPath
