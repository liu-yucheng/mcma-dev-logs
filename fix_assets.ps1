$docsRoot = 'D:\Program-Files\MCMA-Toolchain\dev-logs\docs'
$assetRe = '(?:styles|preview|lightbox)\.(?:css|js)'
$changed = @()

$files = Get-ChildItem -LiteralPath $docsRoot -Recurse -Filter *.html
foreach ($f in $files) {
    $dirPath = Split-Path -Parent $f.FullName
    $rel = [System.IO.Path]::GetRelativePath($dirPath, $docsRoot) -replace '\', '/'
    if ([string]::IsNullOrEmpty($rel)) { $rel = '.' }

    $content = Get-Content -LiteralPath $f.FullName -Raw

    $content = [regex]::Replace($content, '(href|src)="([^"]*?)(' + $assetRe + ')"', {
        param($m)
        $prefix = $m.Groups[2].Value
        if ($prefix -match '^(?:https?:)?//' -or $prefix -match '^[a-zA-Z]+:' -or $prefix.StartsWith('/')) { return $m.Value }
        return $m.Groups[1].Value + '="' + $rel + '/' + $m.Groups[3].Value + '"'
    })

    if ($content -ne (Get-Content -LiteralPath $f.FullName -Raw)) {
        Set-Content -LiteralPath $f.FullName -Value $content -NoNewline -Encoding utf8
        $changed += $f.FullName
    }
}

Write-Output "Changed $($changed.Count) files"