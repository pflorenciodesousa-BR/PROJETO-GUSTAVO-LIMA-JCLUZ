$folder  = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\operadora-certa_2026-06-18"
$tmpl    = "$folder\template_operadora.html"
$outPath = "$folder\operadora-certa_2026-06-18.html"

$cover  = [System.IO.File]::ReadAllText("$folder\cover_b64.txt")
$slide3 = [System.IO.File]::ReadAllText("$folder\slide3_b64.txt")

$html = [System.IO.File]::ReadAllText($tmpl)
$html = $html.Replace('COVER_B64_HERE',  $cover)
$html = $html.Replace('SLIDE3_B64_HERE', $slide3)

[System.IO.File]::WriteAllText($outPath, $html, [System.Text.Encoding]::UTF8)
Write-Host "Gerado com sucesso! Tamanho: $((Get-Item $outPath).Length) bytes"
