# Papirus SYS - Guncelleme scripti
# Yeni surumu GitHub'dan ceker ve her seyi otomatik hazirlar.
# Calistirma: bu dosyaya sag tik -> "PowerShell ile calistir"
# (Once uygulamayi KAPATIN.)

$ErrorActionPreference = "Stop"
$proj = $PSScriptRoot
Write-Host "==== PAPIRUS SYS GUNCELLEME ====" -ForegroundColor Cyan

$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { Write-Host "HATA: Python bulunamadi." -ForegroundColor Red; Read-Host "Cikis"; exit 1 }
$py = $pyCmd.Source

Set-Location $proj

Write-Host "`n[1/4] Yeni surum indiriliyor (git pull)..." -ForegroundColor Yellow
git pull

Write-Host "`n[2/4] Paketler guncelleniyor..." -ForegroundColor Yellow
& $py -m pip install -r (Join-Path $proj "requirements.txt") --quiet

Write-Host "`n[3/4] Veritabani guncelleniyor..." -ForegroundColor Yellow
& $py (Join-Path $proj "manage.py") migrate

Write-Host "`n[4/4] Statik dosyalar guncelleniyor..." -ForegroundColor Yellow
& $py (Join-Path $proj "manage.py") collectstatic --noinput

Write-Host "`n==== GUNCELLEME TAMAMLANDI ====" -ForegroundColor Green
Write-Host "Veritabaniniz (urunler/satislar) korunmustur." -ForegroundColor Green
Write-Host "Simdi masaustundeki Papirus SYS ikonundan uygulamayi acabilirsiniz."
Read-Host "`nCikmak icin Enter"
