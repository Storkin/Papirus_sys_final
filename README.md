# 📦 Papirus SYS — Kırtasiye Toptancı Yönetim Sistemi

> A desktop inventory & point-of-sale management system for stationery wholesalers, built with Django. Runs as a native desktop app — no browser, no terminal.

Kırtasiye toptancıları için **stok yönetimi, müşteri & borç takibi ve hızlı satış (POS)** işlemlerini tek bir masaüstü uygulamasında birleştiren, Django tabanlı bir sistem. Tarayıcı veya terminal gerektirmeden, çift tıkla açılan kendi penceresinde çalışır.

---

## ✨ Öne Çıkan Özellikler

### 📊 Stok & Ürün Yönetimi
- Ürün ekleme, düzenleme, silme; gerçek zamanlı stok takibi
- **Düşük stok uyarıları** ve minimum stok eşiği
- Kategori, tedarikçi, fiyat aralığı ile **filtreleme** ve sıralama
- Her stok değişiminin **değişmez denetim kaydı** (stok hareketleri)

### 🔫 Barkod Entegrasyonu
- Fiziksel **barkod okuyucu** desteği (satış ve girişte)
- **Yerel barkod hafızası**: okutulan ürünü tanır, adını otomatik doldurur — internete hiçbir veri gitmeden
- **Otomatik tamamlama**: isim/barkod yazarken canlı öneri

### 🛒 Satış (POS)
- Çok kalemli satış, barkodla hızlı ekleme, +/- miktar butonları
- Anlık toplam, stok yeterlilik kontrolü, satışta otomatik stok düşümü
- İsteğe bağlı **müşteri borcuna ekleme**

### 👥 Müşteri & Borç Takibi
- Müşteri kayıtları, borç ve son ödeme tarihi
- **Otomatik A–F borç notu** ve risk skoru (borç × gecikme günü)

### 📥 Toplu İçe Aktarma
- **CSV / Excel / PDF** dosyalarından ürün aktarımı
- Tedarikçi sipariş formu **PDF'lerini otomatik ayrıştırma** (konum-bazlı)
- İçe aktarmadan önce **düzenlenebilir önizleme** (miktar/satış fiyatı ayarlama)

### ⚡ Hızlı Ürün Girişi
- Yeni gelen ürünleri liste halinde, sade arayüzle hızlı ekleme

### 🔐 Güvenlik & Roller
- İki seviye yetki: **Patron** (tam erişim) / **Çalışan** (kısıtlı)
- Oturum açık kalma, ortam-değişkenli SECRET_KEY/DEBUG, CSRF koruması
- **Otomatik veritabanı yedekleme** (her açılışta)

### 🌍 Çift Dil
- Tam **Türkçe / İngilizce** arayüz (Django i18n)

---

## 🛠️ Teknolojiler

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3, Django 6, Django ORM |
| Veritabanı | SQLite |
| Masaüstü | pywebview + Waitress (WSGI) |
| Statik sunum | WhiteNoise |
| Frontend | Bootstrap 4 (SB Admin 2), Vanilla JS, Font Awesome |
| Dosya işleme | openpyxl (Excel), pdfplumber (PDF), Pillow |

**Mimari:** Django MVT (Model–View–Template), 3NF normalize edilmiş ilişkisel veritabanı şeması.

---

## 🚀 Kurulum

```bash
# 1) Depoyu klonla
git clone <repo-url>
cd Papirus-sys/toptanci_projesi

# 2) Tek komutla kurulum (Windows)
powershell -ExecutionPolicy Bypass -File kur.ps1
```

`kur.ps1` paketleri kurar, veritabanını hazırlar, yönetici hesabı oluşturur ve **masaüstü kısayolu** ekler. Sonra ikona çift tıkla — uygulama açılır.

**Manuel kurulum:**
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python launcher.py
```

---

## 📸 Ekran Görüntüleri

> _Ekran görüntülerini buraya ekleyebilirsiniz: Dashboard, Satış sayfası, Stok yönetimi, Dosyadan aktarma._

---

## 📂 Proje Yapısı

```
toptanci_projesi/
├── inventory/          # Ana uygulama (modeller, görünümler, formlar)
│   ├── models.py       # Product, Customer, Sale, SaleItem, StockMovement, ReferenceBarcode
│   ├── views.py        # İş mantığı
│   └── templates/      # Arayüz şablonları
├── launcher.py         # Masaüstü başlatıcı (pywebview + Waitress)
├── kur.ps1             # Otomatik kurulum scripti
└── requirements.txt
```

---

## 📝 Lisans

Bu proje kişisel/eğitim amaçlı geliştirilmiştir.

---

<p align="center">Made with ☕ and Django</p>
