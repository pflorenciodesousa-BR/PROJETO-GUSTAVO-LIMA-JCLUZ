$folder = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\carencia-pegadinha_2026-06-15"

$imgs = @{
  'slide2_b64.txt' = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\carencia_slide2_watch_1781552970208.png'
  'slide3_b64.txt' = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\carencia_slide3_contract_1781552980868.png'
  'slide5_b64.txt' = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\carencia_slide5_glasses_1781552990594.png'
}

foreach ($key in $imgs.Keys) {
  $bytes = [System.IO.File]::ReadAllBytes($imgs[$key])
  $b64   = [System.Convert]::ToBase64String($bytes)
  [System.IO.File]::WriteAllText("$folder\$key", $b64)
  Write-Host "Atualizado: $key"
}
