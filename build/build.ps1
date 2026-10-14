$ErrorActionPreference = "Stop"
# The build regenerates the whole site from the committed baseline, then verifies.
# Source imagery lives outside the repository - see build/README.md.
$REPO = "C:\Users\Fran6\Documents\GitHub\Portfolio"
$BK   = "C:\Users\Fran6\Documents\GitHub\_wix_source_backup"
$HERE = Join-Path $REPO "build"

if (-not (Test-Path $BK)) {
  throw "Source image library not found at $BK - see build/README.md"
}

Write-Host "`n=== 0. reset the generated pages to the committed baseline ===" -ForegroundColor Cyan
Set-Location $REPO
# Only the pages and stylesheet this pipeline writes. Deliberately NOT `git checkout .`,
# which would also revert README.md and any doc that is not itself generated.
git checkout HEAD -- "*.html" "projects" robots.txt sitemap.xml assets/css/site.css
git clean -fdq assets/img assets/media assets/files
Remove-Item "_assets.json" -Force -ErrorAction SilentlyContinue
Write-Host "reset ok"

Set-Location $BK
$steps = @("01-assets.py", "02-media.py", "03-breakdown-shots.py", "04-rewrite.py",
           "05-reel-cv-bio.py", "06-no-still-panels.py", "07-seo-sitemap.py",
           "08-consoles-skills-bio.py", "09-css.py")
foreach ($s in $steps) {
  Write-Host "`n=== $s ===" -ForegroundColor Cyan
  python (Join-Path $HERE $s)
  if ($LASTEXITCODE -ne 0) { throw "$s failed" }
}
Write-Host "`n=== verify ===" -ForegroundColor Cyan
python (Join-Path $HERE "verify.py")