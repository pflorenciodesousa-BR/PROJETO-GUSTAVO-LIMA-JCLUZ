$folder  = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\carencia-pegadinha_2026-06-15"
$imgPath = 'C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\carencia_cover_v3_1781538393027.png'
$bytes = [System.IO.File]::ReadAllBytes($imgPath)
$b64   = [System.Convert]::ToBase64String($bytes)
[System.IO.File]::WriteAllText("$folder\cover_b64.txt", $b64)
Write-Host "cover_b64.txt atualizado com a nova imagem da mulher desesperada!"
