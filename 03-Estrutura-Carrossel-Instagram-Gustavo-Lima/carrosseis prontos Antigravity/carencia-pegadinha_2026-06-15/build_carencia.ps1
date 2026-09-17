$folder  = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\carencia-pegadinha_2026-06-15"
$tmpl    = "$folder\template_carencia.html"
$outPath = "$folder\carencia-pegadinha_2026-06-15.html"

$cb  = [System.IO.File]::ReadAllText("$folder\cover_b64.txt").Trim()
$s2b = [System.IO.File]::ReadAllText("$folder\slide2_b64.txt").Trim()
$s3b = [System.IO.File]::ReadAllText("$folder\slide3_b64.txt").Trim()
$s5b = [System.IO.File]::ReadAllText("$folder\slide5_b64.txt").Trim()

$html = [System.IO.File]::ReadAllText($tmpl)
$html = $html.Replace('COVER_B64_HERE',  $cb)
$html = $html.Replace('SLIDE2_B64_HERE', $s2b)
$html = $html.Replace('SLIDE3_B64_HERE', $s3b)
$html = $html.Replace('SLIDE5_B64_HERE', $s5b)

[System.IO.File]::WriteAllText($outPath, $html, [System.Text.Encoding]::UTF8)
$size = [System.IO.File]::ReadAllBytes($outPath).Length
Write-Host "Gerado com sucesso! Tamanho: $size bytes"

