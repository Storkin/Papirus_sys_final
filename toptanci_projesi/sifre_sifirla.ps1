# Papirus SYS - SIFRE SIFIRLAMA
# Giris sifresini unuttuysaniz yeni sifre belirlemek icin kullanilir.
# Calistirma: bu dosyaya sag tik -> "PowerShell ile calistir"
# (Once uygulamayi KAPATIN.)
#
# Guvenlik notu: bu arac sadece bilgisayarin basindayken calisir.
# Telefondan veya ag uzerinden erisilemez.

$ErrorActionPreference = "Stop"
$proj = $PSScriptRoot
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==== PAPIRUS SYS SIFRE SIFIRLAMA ====" -ForegroundColor Cyan

$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { Write-Host "HATA: Python bulunamadi." -ForegroundColor Red; Read-Host "Cikis"; exit 1 }
$py = $pyCmd.Source
$arac = Join-Path $proj "sifre_araci.py"

# --- Kullanicilari listele ---
$satirlar = & $py $arac liste
if ($LASTEXITCODE -ne 0 -or -not $satirlar) {
    Write-Host "HATA: Kullanici listesi alinamadi." -ForegroundColor Red
    Write-Host $satirlar
    Read-Host "`nCikmak icin Enter"; exit 1
}

$kullanicilar = @()
foreach ($s in $satirlar) {
    $p = $s -split '\|'
    if ($p.Count -ge 3) {
        $kullanicilar += [pscustomobject]@{ Id = $p[0]; Ad = $p[1]; Rol = $p[2] }
    }
}
if ($kullanicilar.Count -eq 0) {
    Write-Host "Kayitli kullanici bulunamadi." -ForegroundColor Red
    Read-Host "`nCikmak icin Enter"; exit 1
}

Write-Host "`nKayitli kullanicilar:" -ForegroundColor Yellow
for ($i = 0; $i -lt $kullanicilar.Count; $i++) {
    $k = $kullanicilar[$i]
    Write-Host ("  {0}) {1}   [{2}]" -f ($i + 1), $k.Ad, $k.Rol)
}

# --- Kullanici sec ---
$secim = Read-Host "`nSifresini degistirmek istediginiz kullanicinin numarasi"
$idx = 0
if (-not [int]::TryParse($secim, [ref]$idx) -or $idx -lt 1 -or $idx -gt $kullanicilar.Count) {
    Write-Host "Gecersiz secim. Iptal edildi." -ForegroundColor Red
    Read-Host "`nCikmak icin Enter"; exit 1
}
$secilen = $kullanicilar[$idx - 1]
Write-Host "`nSecilen kullanici: $($secilen.Ad)" -ForegroundColor Green

# --- Yeni sifreyi iki kez sor (yazarken ekranda gorunmez) ---
Write-Host "Yeni sifreyi yazin (guvenlik geregi ekranda gorunmez):"
$s1 = Read-Host "Yeni sifre" -AsSecureString
$s2 = Read-Host "Yeni sifre (tekrar)" -AsSecureString

function SecureToPlain($sec) {
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
}

$p1 = SecureToPlain $s1
$p2 = SecureToPlain $s2

if ($p1 -ne $p2) {
    Write-Host "`nIki sifre birbirini tutmuyor. Iptal edildi." -ForegroundColor Red
    Read-Host "`nCikmak icin Enter"; exit 1
}
if ($p1.Length -lt 4) {
    Write-Host "`nSifre en az 4 karakter olmali. Iptal edildi." -ForegroundColor Red
    Read-Host "`nCikmak icin Enter"; exit 1
}

# --- Degistir (sifre komut satirinda gorunmesin diye ortam degiskeniyle gonderilir) ---
$env:PAPIRUS_YENI_SIFRE = $p1
try {
    $sonuc = & $py $arac degistir $secilen.Id
} finally {
    Remove-Item Env:PAPIRUS_YENI_SIFRE -ErrorAction SilentlyContinue
    $p1 = $null; $p2 = $null
}

if ($sonuc -like "TAMAM*") {
    Write-Host "`n==== SIFRE DEGISTIRILDI ====" -ForegroundColor Green
    Write-Host "Kullanici: $($secilen.Ad)" -ForegroundColor Green
    Write-Host "Artik uygulamayi acip yeni sifrenizle giris yapabilirsiniz."
} else {
    Write-Host "`nSifre degistirilemedi." -ForegroundColor Red
    Write-Host $sonuc
}
Read-Host "`nCikmak icin Enter"
