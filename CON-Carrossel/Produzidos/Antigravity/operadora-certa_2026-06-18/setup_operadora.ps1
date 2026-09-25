$folder = "C:\Users\Jcluz\Antigravity IDE\operadora-certa_2026-06-18"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

$imgs = @{
  'cover_b64.txt'  = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\capa_qual_melhor_operadora_1781814424503.png'
  'slide3_b64.txt' = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\sketch_mapa_brasil_operadora_1781814430854.png'
}

foreach ($key in $imgs.Keys) {
  $bytes = [System.IO.File]::ReadAllBytes($imgs[$key])
  $b64   = [System.Convert]::ToBase64String($bytes)
  [System.IO.File]::WriteAllText("$folder\$key", $b64)
  Write-Host "OK: $key"
}
Write-Host "Imagens prontas!"
