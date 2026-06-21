# Papirus SYS - Dükkan bilgisayarı kurulum scripti
# Çalıştırma: bu dosyaya sağ tık -> "PowerShell ile çalıştır"
#  ya da terminalde:  powershell -ExecutionPolicy Bypass -File kur.ps1

$ErrorActionPreference = "Stop"
$proj = $PSScriptRoot
Write-Host "==== PAPIRUS SYS KURULUM ====" -ForegroundColor Cyan
Write-Host "Proje klasoru: $proj"

# 1) Python var mi?
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) {
    Write-Host "HATA: Python bulunamadi!" -ForegroundColor Red
    Write-Host "Once https://www.python.org/downloads/ adresinden Python kurun"
    Write-Host "(Kurulumda 'Add Python to PATH' kutusunu MUTLAKA isaretleyin)."
    Read-Host "Cikmak icin Enter"
    exit 1
}
$py = $pyCmd.Source
$pyw = $py -replace 'python\.exe$', 'pythonw.exe'
Write-Host "Python bulundu: $py" -ForegroundColor Green

# 2) Gerekli paketleri kur
Write-Host "`n[1/4] Paketler kuruluyor..." -ForegroundColor Yellow
& $py -m pip install --upgrade pip
& $py -m pip install -r (Join-Path $proj "requirements.txt")

# 3) Veritabani ve statik dosyalar
Write-Host "`n[2/4] Veritabani hazirlaniyor..." -ForegroundColor Yellow
& $py (Join-Path $proj "manage.py") migrate
Write-Host "`n[3/4] Statik dosyalar toplaniyor..." -ForegroundColor Yellow
& $py (Join-Path $proj "manage.py") collectstatic --noinput

# Yonetici (admin) hesabi yoksa olustur (GitHub'dan kurulumda db bos gelir)
$check = & $py (Join-Path $proj "manage.py") shell -c "from django.contrib.auth.models import User; import sys; sys.stdout.write('VAR' if User.objects.filter(is_superuser=True).exists() else 'YOK')"
if ($check -match 'YOK') {
    Write-Host "`nYonetici (patron) hesabi yok. Simdi olusturalim:" -ForegroundColor Cyan
    Write-Host "(Kullanici adi: admin yazabilirsiniz. Sifre yazarken ekranda gorunmez, normaldir.)"
    & $py (Join-Path $proj "manage.py") createsuperuser
}

# 4) Ikon + masaustu kisayolu
Write-Host "`n[4/4] Masaustu kisayolu olusturuluyor..." -ForegroundColor Yellow
& $py (Join-Path $proj "make_icon.py")
$icon = Join-Path $proj "papirus.ico"
$desktop = [Environment]::GetFolderPath("Desktop")
$lnk = Join-Path $desktop "Papirus SYS.lnk"
$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($lnk)
$sc.TargetPath = $pyw
$sc.Arguments = '"' + (Join-Path $proj "launcher.py") + '"'
$sc.WorkingDirectory = $proj
$sc.IconLocation = $icon
$sc.Description = "Papirus SYS - Kirtasiye Yonetim Sistemi"
$sc.Save()

Write-Host "`n==== KURULUM TAMAMLANDI ====" -ForegroundColor Green
Write-Host "Masaustundeki 'Papirus SYS' ikonuna cift tiklayarak baslatabilirsiniz."
Write-Host ""
Write-Host "ONEMLI: Ilk acilistan once admin sifresini ayarlamak isterseniz:" -ForegroundColor Cyan
Write-Host "  python manage.py changepassword admin"
Read-Host "`nCikmak icin Enter"
