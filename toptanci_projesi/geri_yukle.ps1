# Papirus SYS - Veritabani GERI YUKLEME
# Yedeklerden en yenisini bulup geri yukler.
# Calistirma: bu dosyaya sag tik -> "PowerShell ile calistir"
# (Once uygulamayi KAPATIN.)

$ErrorActionPreference = "Stop"
$proj = $PSScriptRoot
$home = $env:USERPROFILE

# Yedeklerin arandigi tum konumlar
$locs = @()
if ($env:OneDrive) { $locs += (Join-Path $env:OneDrive 'Papirus_Yedek') }
$locs += (Join-Path $home 'Papirus_Yedek')
$locs += (Join-Path $home 'Documents\Papirus_Yedek')
$locs += (Join-Path $home 'Belgeler\Papirus_Yedek')
$locs += (Join-Path $proj 'backups')

Write-Host "==== VERITABANI GERI YUKLEME ====" -ForegroundColor Cyan
$all = @()
foreach ($l in $locs) {
    if (Test-Path $l) {
        $all += Get-ChildItem (Join-Path $l "db_*.sqlite3") -ErrorAction SilentlyContinue
    }
}
if (-not $all) {
    Write-Host "Hicbir yedek bulunamadi. Aranan yerler:" -ForegroundColor Red
    $locs | ForEach-Object { Write-Host "  $_" }
    Read-Host "Cikis"; exit
}

# En yeni 5 yedegi goster
$sorted = $all | Sort-Object LastWriteTime -Descending
Write-Host "`nBulunan en yeni yedekler:" -ForegroundColor Yellow
$sorted | Select-Object -First 5 | ForEach-Object {
    Write-Host ("  {0}  ({1:dd.MM.yyyy HH:mm})  {2}" -f $_.Name, $_.LastWriteTime, $_.DirectoryName)
}

$newest = $sorted | Select-Object -First 1
Write-Host "`nEN YENI: $($newest.FullName)" -ForegroundColor Green
Write-Host ("Tarih: {0:dd.MM.yyyy HH:mm}" -f $newest.LastWriteTime)
$ans = Read-Host "`nBu yedegi geri yuklemek istiyor musunuz? (E/H)"

if ($ans -eq 'E' -or $ans -eq 'e') {
    $db = Join-Path $proj 'db.sqlite3'
    if (Test-Path $db) {
        Copy-Item $db "$db.geri_yukleme_oncesi" -Force
        Write-Host "Mevcut veritabani '$db.geri_yukleme_oncesi' olarak saklandi."
    }
    Copy-Item $newest.FullName $db -Force
    # WAL modundan kalan eski -wal/-shm dosyalari varsa temizle (tutarsizlik olmasin)
    Remove-Item "$db-wal" -Force -ErrorAction SilentlyContinue
    Remove-Item "$db-shm" -Force -ErrorAction SilentlyContinue
    Write-Host "`nGERI YUKLENDI! Artik uygulamayi acabilirsiniz." -ForegroundColor Green
} else {
    Write-Host "Iptal edildi."
}
Read-Host "`nCikmak icin Enter"
