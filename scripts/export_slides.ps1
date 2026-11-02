param (
    [string]$PptxPath = "",
    [string]$OutDir = ""
)

# If no path specified, search in current directory or presentations folder
if (-not $PptxPath) {
    $searchDirs = @(".", "presentations", "slides")
    $file = $null
    foreach ($d in $searchDirs) {
        if (Test-Path $d) {
            $candidate = Get-ChildItem $d -Filter "*.pptx" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if ($candidate) {
                $file = $candidate
                break
            }
        }
    }
    if (-not $file) {
        Write-Error "No PPTX found. Please provide -PptxPath explicitly."
        exit 1
    }
    $PptxPath = $file.FullName
} else {
    $PptxPath = (Resolve-Path $PptxPath).Path
}

if (-not $OutDir) {
    $parentDir = Split-Path -Parent $PptxPath
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($PptxPath)
    $OutDir = Join-Path $parentDir ($baseName + "_rendered")
}

Write-Host "Target PPTX: $PptxPath"
Write-Host "Output Dir:  $OutDir"

if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}

$ppt = New-Object -ComObject PowerPoint.Application
try {
    $pres = $ppt.Presentations.Open($PptxPath, $true, $false, $false)
    for ($i = 1; $i -le $pres.Slides.Count; $i++) {
        $slide = $pres.Slides.Item($i)
        $outPath = Join-Path $OutDir ("slide_{0:D2}.png" -f $i)
        $slide.Export($outPath, "PNG")
        Write-Host "Exported slide $i to $outPath"
    }
    $pres.Close()
    Write-Host "Successfully exported $($pres.Slides.Count) slides!"
} finally {
    $ppt.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
    [System.GC]::Collect()
}
