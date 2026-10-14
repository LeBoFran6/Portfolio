param([string[]]$Pages = @("index.html"))
$REPO = "C:\Users\Fran6\Documents\GitHub\Portfolio"
$SHOTS = "C:\Users\Fran6\AppData\Local\Temp\opencode\shots"
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
New-Item -ItemType Directory -Force -Path $SHOTS | Out-Null
foreach ($pg in $Pages) {
  $name = [IO.Path]::GetFileNameWithoutExtension($pg)
  $out = Join-Path $SHOTS "$name.png"
  Remove-Item $out -Force -ErrorAction SilentlyContinue
  $url = "file:///C:/Users/Fran6/Documents/GitHub/Portfolio/" + $pg
  $p = Start-Process -FilePath $chrome -PassThru -WindowStyle Hidden -ArgumentList `
    "--headless=new","--disable-gpu","--no-sandbox","--hide-scrollbars",
    "--force-device-scale-factor=1","--run-all-compositor-stages-before-draw",
    "--window-size=1440,3200","--virtual-time-budget=25000",
    "--screenshot=$out", $url
  if (-not $p.WaitForExit(90000)) { $p.Kill() }
  Start-Sleep -Milliseconds 400
  if (Test-Path $out) { Write-Host "ok  $name  $((Get-Item $out).Length) bytes" }
  else { Write-Host "FAIL $name" }
}
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue