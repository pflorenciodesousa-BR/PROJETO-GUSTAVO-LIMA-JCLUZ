$CoverImg = "C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\ilusao_cover_2026_06_21_1782062310524.png"
$SketchImg = "C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\ilusao_sketch_2026_06_21_1782062318039.png"
$Sketch2 = "C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\ilusao_sketch_light_slide2_1782063487887.png"
$Sketch4 = "C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\ilusao_sketch_light_slide4_1782063495791.png"
$Sketch7 = "C:\Users\Jcluz\.gemini\antigravity-ide\brain\490278bb-c877-40c8-8a1f-0a7b6926274a\ilusao_sketch_light_slide7_1782063505968.png"

$CoverBytes = [System.IO.File]::ReadAllBytes($CoverImg)
$CoverB64 = "data:image/png;base64," + [Convert]::ToBase64String($CoverBytes)

$SketchBytes = [System.IO.File]::ReadAllBytes($SketchImg)
$SketchB64 = "data:image/png;base64," + [Convert]::ToBase64String($SketchBytes)

$Sketch2B64 = "data:image/png;base64," + [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($Sketch2))
$Sketch4B64 = "data:image/png;base64," + [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($Sketch4))
$Sketch7B64 = "data:image/png;base64," + [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($Sketch7))

$TemplatePath = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\ilusao_cnpj_2026-06-21\template_ilusao.html"
$OutputPath = "C:\Users\Jcluz\Antigravity IDE\Estrutura Carrossel\carrosseis prontos\ilusao_cnpj_2026-06-21\carrossel_ilusao_cnpj.html"

$HtmlContent = [System.IO.File]::ReadAllText($TemplatePath, [System.Text.Encoding]::UTF8)

# Inject images
$HtmlContent = $HtmlContent.Replace("COVER_B64_HERE", $CoverB64)
$HtmlContent = $HtmlContent.Replace("STICKER_B64_HERE", $SketchB64)
$HtmlContent = $HtmlContent.Replace("STICKER_LIGHT_2_B64_HERE", $Sketch2B64)
$HtmlContent = $HtmlContent.Replace("STICKER_LIGHT_4_B64_HERE", $Sketch4B64)
$HtmlContent = $HtmlContent.Replace("STICKER_LIGHT_7_B64_HERE", $Sketch7B64)

[System.IO.File]::WriteAllText($OutputPath, $HtmlContent, [System.Text.Encoding]::UTF8)

Write-Host "Build Finalizado! Arquivo carrossel_ilusao_cnpj.html gerado com sucesso."
