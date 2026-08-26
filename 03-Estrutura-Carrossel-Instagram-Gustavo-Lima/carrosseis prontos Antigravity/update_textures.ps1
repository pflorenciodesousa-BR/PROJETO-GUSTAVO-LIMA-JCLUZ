$ErrorActionPreference = 'Stop'
$baseDir = "C:\Users\Jcluz\Antigravity\03-Estrutura-Carrossel-Instagram-Gustavo-Lima\carrosseis prontos"
$dirs = Get-ChildItem -Path $baseDir -Directory

foreach ($d in $dirs) {
    if ($d.Name -like "*reajuste*") { continue }
    if ($d.Name -notlike "*_v4_*") { continue }
    
    $htmlFile = Get-ChildItem -Path $d.FullName -Filter "template_*.html" | Select-Object -First 1
    if ($htmlFile) {
        Write-Host "Updating $($htmlFile.Name)..."
        $content = Get-Content $htmlFile.FullName -Raw -Encoding UTF8
        
        $content = $content -replace "baseFrequency='0.8' numOctaves='4'", "baseFrequency='1.5' numOctaves='2'"
        $content = $content -replace "opacity:\s*0\.22;\s*mix-blend-mode:\s*overlay;", "opacity: 0.08; mix-blend-mode: overlay;"
        $content = $content -replace "opacity:\s*0\.12;\s*mix-blend-mode:\s*multiply;", "opacity: 0.04; mix-blend-mode: multiply;"
        
        Set-Content -Path $htmlFile.FullName -Value $content -Encoding UTF8
        
        $buildScript = Get-ChildItem -Path $d.FullName -Filter "build_*.ps1" | Select-Object -First 1
        if ($buildScript) {
            Write-Host "Building $($buildScript.Name)..."
            $ps1Content = Get-Content $buildScript.FullName -Raw -Encoding UTF8
            $ps1Content = $ps1Content -replace "(?m)^try \{ Start-Process.*", ""
            $ps1Content = $ps1Content -replace "(?m)^catch \{ Start-Process.*", ""
            Set-Content -Path $buildScript.FullName -Value $ps1Content -Encoding UTF8
            
            Set-Location $d.FullName
            & $buildScript.FullName
        }
    }
}
Write-Host "All remaining carousels updated successfully!"
