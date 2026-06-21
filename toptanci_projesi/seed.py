import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toptanci_projesi.settings')
django.setup()

from inventory.models import Product
from django.contrib.auth.models import User


def seed_db():
    print("Seeding database...")

    if not User.objects.filter(username='admin').exists():
        # SECURITY: never hardcode a real password. Read it from an env var;
        # if not set, create the user WITHOUT a usable password and require
        # the operator to set one via:  python manage.py changepassword admin
        admin_pw = os.environ.get('PAPIRUS_ADMIN_PASSWORD')
        user = User.objects.create_superuser('admin', 'admin@papirus.com', admin_pw or None)
        if not admin_pw:
            user.set_unusable_password()
            user.save()
            print("Admin user created WITHOUT a password.")
            print("Set one now with:  python manage.py changepassword admin")
        else:
            print("Admin user created with password from PAPIRUS_ADMIN_PASSWORD.")

    products = [
        # --- Kalem & Yazı Araçları ---
        {"name": "BIC Cristal Tükenmez Kalem Mavi", "category": "Kalem & Yazı Araçları", "price": 4.50, "manufacturer": "BIC", "stock_quantity": 500, "unit": "adet", "barcode": "3086123400013", "tax_rate": 20.0, "supplier": "BIC Türkiye", "shelf_location": "A1", "min_stock": 50},
        {"name": "BIC Cristal Tükenmez Kalem Siyah", "category": "Kalem & Yazı Araçları", "price": 4.50, "manufacturer": "BIC", "stock_quantity": 500, "unit": "adet", "barcode": "3086123400020", "tax_rate": 20.0, "supplier": "BIC Türkiye", "shelf_location": "A1", "min_stock": 50},
        {"name": "BIC Cristal Tükenmez Kalem Kırmızı", "category": "Kalem & Yazı Araçları", "price": 4.50, "manufacturer": "BIC", "stock_quantity": 300, "unit": "adet", "barcode": "3086123400037", "tax_rate": 20.0, "supplier": "BIC Türkiye", "shelf_location": "A1", "min_stock": 30},
        {"name": "Staedtler Kurşun Kalem 2B", "category": "Kalem & Yazı Araçları", "price": 6.00, "manufacturer": "Staedtler", "stock_quantity": 400, "unit": "adet", "barcode": "4007817326008", "tax_rate": 20.0, "supplier": "Staedtler Türkiye", "shelf_location": "A2", "min_stock": 40},
        {"name": "Staedtler Kurşun Kalem HB", "category": "Kalem & Yazı Araçları", "price": 5.50, "manufacturer": "Staedtler", "stock_quantity": 600, "unit": "adet", "barcode": "4007817326015", "tax_rate": 20.0, "supplier": "Staedtler Türkiye", "shelf_location": "A2", "min_stock": 60},
        {"name": "Faber-Castell Grip 2001 Kurşun Kalem", "category": "Kalem & Yazı Araçları", "price": 8.00, "manufacturer": "Faber-Castell", "stock_quantity": 350, "unit": "adet", "barcode": "4005401172017", "tax_rate": 20.0, "supplier": "Faber-Castell Türkiye", "shelf_location": "A2", "min_stock": 35},
        {"name": "Stabilo Boss Fosforlu Kalem Sarı", "category": "Kalem & Yazı Araçları", "price": 12.00, "manufacturer": "Stabilo", "stock_quantity": 250, "unit": "adet", "barcode": "4006381103008", "tax_rate": 20.0, "supplier": "Stabilo Türkiye", "shelf_location": "A3", "min_stock": 25},
        {"name": "Stabilo Boss Fosforlu Kalem Pembe", "category": "Kalem & Yazı Araçları", "price": 12.00, "manufacturer": "Stabilo", "stock_quantity": 200, "unit": "adet", "barcode": "4006381103015", "tax_rate": 20.0, "supplier": "Stabilo Türkiye", "shelf_location": "A3", "min_stock": 20},
        {"name": "Stabilo Boss Fosforlu Kalem Yeşil", "category": "Kalem & Yazı Araçları", "price": 12.00, "manufacturer": "Stabilo", "stock_quantity": 200, "unit": "adet", "barcode": "4006381103022", "tax_rate": 20.0, "supplier": "Stabilo Türkiye", "shelf_location": "A3", "min_stock": 20},
        {"name": "Pentel Energel Jel Kalem 0.7 Siyah", "category": "Kalem & Yazı Araçları", "price": 18.00, "manufacturer": "Pentel", "stock_quantity": 180, "unit": "adet", "barcode": "0072512263058", "tax_rate": 20.0, "supplier": "Pentel Türkiye", "shelf_location": "A4", "min_stock": 20},
        {"name": "Pentel Energel Jel Kalem 0.7 Mavi", "category": "Kalem & Yazı Araçları", "price": 18.00, "manufacturer": "Pentel", "stock_quantity": 150, "unit": "adet", "barcode": "0072512263065", "tax_rate": 20.0, "supplier": "Pentel Türkiye", "shelf_location": "A4", "min_stock": 15},
        {"name": "Pilot G2 Jel Kalem 0.5 Siyah", "category": "Kalem & Yazı Araçları", "price": 22.00, "manufacturer": "Pilot", "stock_quantity": 200, "unit": "adet", "barcode": "3501179801017", "tax_rate": 20.0, "supplier": "Pilot Türkiye", "shelf_location": "A4", "min_stock": 20},
        {"name": "Edding 3000 Permanent Markör Siyah", "category": "Kalem & Yazı Araçları", "price": 25.00, "manufacturer": "Edding", "stock_quantity": 120, "unit": "adet", "barcode": "4004764324006", "tax_rate": 20.0, "supplier": "Edding Türkiye", "shelf_location": "A5", "min_stock": 15},
        {"name": "Edding 3000 Permanent Markör Kırmızı", "category": "Kalem & Yazı Araçları", "price": 25.00, "manufacturer": "Edding", "stock_quantity": 100, "unit": "adet", "barcode": "4004764324013", "tax_rate": 20.0, "supplier": "Edding Türkiye", "shelf_location": "A5", "min_stock": 10},
        {"name": "Artline Tahta Kalemi Siyah", "category": "Kalem & Yazı Araçları", "price": 15.00, "manufacturer": "Artline", "stock_quantity": 150, "unit": "adet", "barcode": "9310928502001", "tax_rate": 20.0, "supplier": "Artline Türkiye", "shelf_location": "A5", "min_stock": 15},

        # --- Defter & Blok ---
        {"name": "Güvercin A4 Çizgili Defter 96 Yaprak", "category": "Defter & Blok", "price": 35.00, "manufacturer": "Güvercin", "stock_quantity": 300, "unit": "adet", "barcode": "8690526010011", "tax_rate": 20.0, "supplier": "Güvercin Kağıt", "shelf_location": "B1", "min_stock": 30},
        {"name": "Güvercin A4 Kareli Defter 96 Yaprak", "category": "Defter & Blok", "price": 35.00, "manufacturer": "Güvercin", "stock_quantity": 300, "unit": "adet", "barcode": "8690526010028", "tax_rate": 20.0, "supplier": "Güvercin Kağıt", "shelf_location": "B1", "min_stock": 30},
        {"name": "Güvercin A5 Çizgili Defter 60 Yaprak", "category": "Defter & Blok", "price": 22.00, "manufacturer": "Güvercin", "stock_quantity": 400, "unit": "adet", "barcode": "8690526010035", "tax_rate": 20.0, "supplier": "Güvercin Kağıt", "shelf_location": "B1", "min_stock": 40},
        {"name": "Oxford Spiralli Blok A4 80 Yaprak Çizgili", "category": "Defter & Blok", "price": 55.00, "manufacturer": "Oxford", "stock_quantity": 200, "unit": "adet", "barcode": "3020120061008", "tax_rate": 20.0, "supplier": "Oxford Türkiye", "shelf_location": "B2", "min_stock": 20},
        {"name": "Oxford Spiralli Blok A5 80 Yaprak Çizgili", "category": "Defter & Blok", "price": 40.00, "manufacturer": "Oxford", "stock_quantity": 200, "unit": "adet", "barcode": "3020120061015", "tax_rate": 20.0, "supplier": "Oxford Türkiye", "shelf_location": "B2", "min_stock": 20},
        {"name": "Herlitz Ajanda 2025 Haftalık A5", "category": "Defter & Blok", "price": 120.00, "manufacturer": "Herlitz", "stock_quantity": 80, "unit": "adet", "barcode": "4008110290015", "tax_rate": 20.0, "supplier": "Herlitz Türkiye", "shelf_location": "B3", "min_stock": 10},
        {"name": "Moleskine Classic Sert Kapak Defter A5", "category": "Defter & Blok", "price": 280.00, "manufacturer": "Moleskine", "stock_quantity": 50, "unit": "adet", "barcode": "8058647620015", "tax_rate": 20.0, "supplier": "Moleskine Türkiye", "shelf_location": "B3", "min_stock": 5},
        {"name": "Post-it Yapışkanlı Not Kağıdı 76x76mm Sarı", "category": "Defter & Blok", "price": 45.00, "manufacturer": "3M", "stock_quantity": 250, "unit": "paket", "barcode": "0051141358475", "tax_rate": 20.0, "supplier": "3M Türkiye", "shelf_location": "B4", "min_stock": 25},
        {"name": "Post-it Yapışkanlı Not Kağıdı 76x76mm Renkli", "category": "Defter & Blok", "price": 55.00, "manufacturer": "3M", "stock_quantity": 200, "unit": "paket", "barcode": "0051141358482", "tax_rate": 20.0, "supplier": "3M Türkiye", "shelf_location": "B4", "min_stock": 20},

        # --- Kağıt Ürünleri ---
        {"name": "Navigator A4 Fotokopi Kağıdı 80gr 500 Yaprak", "category": "Kağıt Ürünleri", "price": 180.00, "manufacturer": "Navigator", "stock_quantity": 200, "unit": "paket", "barcode": "5601008003009", "tax_rate": 20.0, "supplier": "Navigator Türkiye", "shelf_location": "C1", "min_stock": 20},
        {"name": "Navigator A4 Fotokopi Kağıdı 80gr 5 Paket Koli", "category": "Kağıt Ürünleri", "price": 850.00, "manufacturer": "Navigator", "stock_quantity": 50, "unit": "koli", "barcode": "5601008003016", "tax_rate": 20.0, "supplier": "Navigator Türkiye", "shelf_location": "C1", "min_stock": 5},
        {"name": "IQ Premium A4 Fotokopi Kağıdı 80gr 500 Yaprak", "category": "Kağıt Ürünleri", "price": 165.00, "manufacturer": "IQ", "stock_quantity": 150, "unit": "paket", "barcode": "9002762040018", "tax_rate": 20.0, "supplier": "IQ Türkiye", "shelf_location": "C1", "min_stock": 15},
        {"name": "Renkli Fotokopi Kağıdı A4 80gr Sarı 500 Yaprak", "category": "Kağıt Ürünleri", "price": 220.00, "manufacturer": "Navigator", "stock_quantity": 80, "unit": "paket", "barcode": "5601008004006", "tax_rate": 20.0, "supplier": "Navigator Türkiye", "shelf_location": "C2", "min_stock": 10},
        {"name": "Renkli Fotokopi Kağıdı A4 80gr Mavi 500 Yaprak", "category": "Kağıt Ürünleri", "price": 220.00, "manufacturer": "Navigator", "stock_quantity": 80, "unit": "paket", "barcode": "5601008004013", "tax_rate": 20.0, "supplier": "Navigator Türkiye", "shelf_location": "C2", "min_stock": 10},
        {"name": "Faber-Castell Renkli Karton A4 160gr 50 Yaprak", "category": "Kağıt Ürünleri", "price": 85.00, "manufacturer": "Faber-Castell", "stock_quantity": 100, "unit": "paket", "barcode": "4005401204015", "tax_rate": 20.0, "supplier": "Faber-Castell Türkiye", "shelf_location": "C3", "min_stock": 10},
        {"name": "Canson Çizim Kağıdı A3 180gr 25 Yaprak", "category": "Kağıt Ürünleri", "price": 95.00, "manufacturer": "Canson", "stock_quantity": 60, "unit": "paket", "barcode": "3148950100306", "tax_rate": 20.0, "supplier": "Canson Türkiye", "shelf_location": "C3", "min_stock": 8},

        # --- Dosyalama & Arşivleme ---
        {"name": "Leitz Plastik Klasör Geniş A4 Siyah", "category": "Dosyalama & Arşivleme", "price": 65.00, "manufacturer": "Leitz", "stock_quantity": 150, "unit": "adet", "barcode": "4002432260010", "tax_rate": 20.0, "supplier": "Leitz Türkiye", "shelf_location": "D1", "min_stock": 15},
        {"name": "Leitz Plastik Klasör Geniş A4 Mavi", "category": "Dosyalama & Arşivleme", "price": 65.00, "manufacturer": "Leitz", "stock_quantity": 150, "unit": "adet", "barcode": "4002432260027", "tax_rate": 20.0, "supplier": "Leitz Türkiye", "shelf_location": "D1", "min_stock": 15},
        {"name": "Leitz Plastik Klasör Geniş A4 Kırmızı", "category": "Dosyalama & Arşivleme", "price": 65.00, "manufacturer": "Leitz", "stock_quantity": 100, "unit": "adet", "barcode": "4002432260034", "tax_rate": 20.0, "supplier": "Leitz Türkiye", "shelf_location": "D1", "min_stock": 10},
        {"name": "Herlitz Poşet Dosya A4 Şeffaf 100'lü Paket", "category": "Dosyalama & Arşivleme", "price": 95.00, "manufacturer": "Herlitz", "stock_quantity": 120, "unit": "paket", "barcode": "4008110432018", "tax_rate": 20.0, "supplier": "Herlitz Türkiye", "shelf_location": "D2", "min_stock": 12},
        {"name": "Herlitz Telli Dosya A4 Mavi 25'li Paket", "category": "Dosyalama & Arşivleme", "price": 75.00, "manufacturer": "Herlitz", "stock_quantity": 100, "unit": "paket", "barcode": "4008110432025", "tax_rate": 20.0, "supplier": "Herlitz Türkiye", "shelf_location": "D2", "min_stock": 10},
        {"name": "Leitz Karton Kutu Dosya A4 Siyah", "category": "Dosyalama & Arşivleme", "price": 110.00, "manufacturer": "Leitz", "stock_quantity": 80, "unit": "adet", "barcode": "4002432611018", "tax_rate": 20.0, "supplier": "Leitz Türkiye", "shelf_location": "D3", "min_stock": 8},
        {"name": "Marbig Delgeç Çift Delik Metal 30 Sayfa", "category": "Dosyalama & Arşivleme", "price": 85.00, "manufacturer": "Marbig", "stock_quantity": 60, "unit": "adet", "barcode": "9312900873012", "tax_rate": 20.0, "supplier": "Ofis Depo", "shelf_location": "D4", "min_stock": 6},
        {"name": "Kangaro Zımbalar DP-480 24/6 1000 Adet", "category": "Dosyalama & Arşivleme", "price": 35.00, "manufacturer": "Kangaro", "stock_quantity": 200, "unit": "kutu", "barcode": "8901030024061", "tax_rate": 20.0, "supplier": "Kangaro Türkiye", "shelf_location": "D4", "min_stock": 20},
        {"name": "Kangaro Zımba Makinesi DP-480", "category": "Dosyalama & Arşivleme", "price": 120.00, "manufacturer": "Kangaro", "stock_quantity": 40, "unit": "adet", "barcode": "8901030048006", "tax_rate": 20.0, "supplier": "Kangaro Türkiye", "shelf_location": "D4", "min_stock": 5},
        {"name": "Leitz Parmak Etiket 10x100mm Beyaz 100 Adet", "category": "Dosyalama & Arşivleme", "price": 28.00, "manufacturer": "Leitz", "stock_quantity": 150, "unit": "paket", "barcode": "4002432660019", "tax_rate": 20.0, "supplier": "Leitz Türkiye", "shelf_location": "D5", "min_stock": 15},

        # --- Kesici & Yapıştırıcı ---
        {"name": "Maped Yuvarlak Uçlu Makas 17cm", "category": "Kesici & Yapıştırıcı", "price": 45.00, "manufacturer": "Maped", "stock_quantity": 100, "unit": "adet", "barcode": "3154141463014", "tax_rate": 20.0, "supplier": "Maped Türkiye", "shelf_location": "E1", "min_stock": 10},
        {"name": "Maped Kağıt Kesici Makas 21cm", "category": "Kesici & Yapıştırıcı", "price": 65.00, "manufacturer": "Maped", "stock_quantity": 80, "unit": "adet", "barcode": "3154141463021", "tax_rate": 20.0, "supplier": "Maped Türkiye", "shelf_location": "E1", "min_stock": 8},
        {"name": "Olfa Maket Bıçağı Küçük 9mm", "category": "Kesici & Yapıştırıcı", "price": 40.00, "manufacturer": "Olfa", "stock_quantity": 120, "unit": "adet", "barcode": "4901165100124", "tax_rate": 20.0, "supplier": "Olfa Türkiye", "shelf_location": "E1", "min_stock": 12},
        {"name": "Olfa Yedek Bıçak 9mm 10'lu", "category": "Kesici & Yapıştırıcı", "price": 25.00, "manufacturer": "Olfa", "stock_quantity": 200, "unit": "paket", "barcode": "4901165100131", "tax_rate": 20.0, "supplier": "Olfa Türkiye", "shelf_location": "E1", "min_stock": 20},
        {"name": "UHU Stick Yapıştırıcı 21gr", "category": "Kesici & Yapıştırıcı", "price": 22.00, "manufacturer": "UHU", "stock_quantity": 250, "unit": "adet", "barcode": "4026700452001", "tax_rate": 20.0, "supplier": "UHU Türkiye", "shelf_location": "E2", "min_stock": 25},
        {"name": "UHU All Purpose Sıvı Yapıştırıcı 35ml", "category": "Kesici & Yapıştırıcı", "price": 35.00, "manufacturer": "UHU", "stock_quantity": 150, "unit": "adet", "barcode": "4026700010355", "tax_rate": 20.0, "supplier": "UHU Türkiye", "shelf_location": "E2", "min_stock": 15},
        {"name": "Scotch Şeffaf Bant 19mm x 33m", "category": "Kesici & Yapıştırıcı", "price": 18.00, "manufacturer": "3M Scotch", "stock_quantity": 300, "unit": "adet", "barcode": "0021200049101", "tax_rate": 20.0, "supplier": "3M Türkiye", "shelf_location": "E3", "min_stock": 30},
        {"name": "Scotch Çift Taraflı Bant 12mm x 10m", "category": "Kesici & Yapıştırıcı", "price": 28.00, "manufacturer": "3M Scotch", "stock_quantity": 200, "unit": "adet", "barcode": "0021200049118", "tax_rate": 20.0, "supplier": "3M Türkiye", "shelf_location": "E3", "min_stock": 20},
        {"name": "Kraf Bant 50mm x 50m", "category": "Kesici & Yapıştırıcı", "price": 45.00, "manufacturer": "Nopi", "stock_quantity": 150, "unit": "adet", "barcode": "4006166011013", "tax_rate": 20.0, "supplier": "Ofis Depo", "shelf_location": "E3", "min_stock": 15},

        # --- Okul Gereçleri ---
        {"name": "Maped Pergel Seti Metal 10 Parça", "category": "Okul Gereçleri", "price": 95.00, "manufacturer": "Maped", "stock_quantity": 80, "unit": "set", "barcode": "3154141963017", "tax_rate": 20.0, "supplier": "Maped Türkiye", "shelf_location": "F1", "min_stock": 8},
        {"name": "Staedtler Cetvel 30cm Şeffaf", "category": "Okul Gereçleri", "price": 18.00, "manufacturer": "Staedtler", "stock_quantity": 200, "unit": "adet", "barcode": "4007817563008", "tax_rate": 20.0, "supplier": "Staedtler Türkiye", "shelf_location": "F1", "min_stock": 20},
        {"name": "Staedtler Gönye Seti 45° + 60°", "category": "Okul Gereçleri", "price": 35.00, "manufacturer": "Staedtler", "stock_quantity": 150, "unit": "set", "barcode": "4007817563015", "tax_rate": 20.0, "supplier": "Staedtler Türkiye", "shelf_location": "F1", "min_stock": 15},
        {"name": "Staedtler İletki 180° Şeffaf", "category": "Okul Gereçleri", "price": 12.00, "manufacturer": "Staedtler", "stock_quantity": 200, "unit": "adet", "barcode": "4007817563022", "tax_rate": 20.0, "supplier": "Staedtler Türkiye", "shelf_location": "F1", "min_stock": 20},
        {"name": "Faber-Castell Silgi 7041-20 Beyaz", "category": "Okul Gereçleri", "price": 8.00, "manufacturer": "Faber-Castell", "stock_quantity": 500, "unit": "adet", "barcode": "4005401704102", "tax_rate": 20.0, "supplier": "Faber-Castell Türkiye", "shelf_location": "F2", "min_stock": 50},
        {"name": "Faber-Castell Kalemtıraş Çift Delikli Metal", "category": "Okul Gereçleri", "price": 15.00, "manufacturer": "Faber-Castell", "stock_quantity": 300, "unit": "adet", "barcode": "4005401182016", "tax_rate": 20.0, "supplier": "Faber-Castell Türkiye", "shelf_location": "F2", "min_stock": 30},
        {"name": "Maped Color'Peps Kuru Boya 12 Renk", "category": "Okul Gereçleri", "price": 55.00, "manufacturer": "Maped", "stock_quantity": 120, "unit": "kutu", "barcode": "3154141832014", "tax_rate": 20.0, "supplier": "Maped Türkiye", "shelf_location": "F3", "min_stock": 12},
        {"name": "Maped Color'Peps Kuru Boya 24 Renk", "category": "Okul Gereçleri", "price": 95.00, "manufacturer": "Maped", "stock_quantity": 100, "unit": "kutu", "barcode": "3154141832021", "tax_rate": 20.0, "supplier": "Maped Türkiye", "shelf_location": "F3", "min_stock": 10},
        {"name": "Pelikan Sulu Boya 12 Renk", "category": "Okul Gereçleri", "price": 75.00, "manufacturer": "Pelikan", "stock_quantity": 100, "unit": "kutu", "barcode": "4012700808011", "tax_rate": 20.0, "supplier": "Pelikan Türkiye", "shelf_location": "F3", "min_stock": 10},
        {"name": "Faber-Castell Keçeli Kalem 10 Renk", "category": "Okul Gereçleri", "price": 45.00, "manufacturer": "Faber-Castell", "stock_quantity": 150, "unit": "kutu", "barcode": "4005401554011", "tax_rate": 20.0, "supplier": "Faber-Castell Türkiye", "shelf_location": "F3", "min_stock": 15},
        {"name": "Faber-Castell Plastik Kalemlik Şeffaf", "category": "Okul Gereçleri", "price": 28.00, "manufacturer": "Faber-Castell", "stock_quantity": 80, "unit": "adet", "barcode": "4005401701019", "tax_rate": 20.0, "supplier": "Faber-Castell Türkiye", "shelf_location": "F4", "min_stock": 8},

        # --- Ofis Gereçleri ---
        {"name": "Ataç Standart 28mm 100 Adet Kutu", "category": "Ofis Gereçleri", "price": 15.00, "manufacturer": "Forpus", "stock_quantity": 300, "unit": "kutu", "barcode": "4770004280010", "tax_rate": 20.0, "supplier": "Ofis Depo", "shelf_location": "G1", "min_stock": 30},
        {"name": "Ataç Renkli Plastik 32mm 100 Adet", "category": "Ofis Gereçleri", "price": 18.00, "manufacturer": "Forpus", "stock_quantity": 250, "unit": "kutu", "barcode": "4770004280027", "tax_rate": 20.0, "supplier": "Ofis Depo", "shelf_location": "G1", "min_stock": 25},
        {"name": "Gübre Lastik 100gr Paket", "category": "Ofis Gereçleri", "price": 20.00, "manufacturer": "Yıldız", "stock_quantity": 200, "unit": "paket", "barcode": "8690526200019", "tax_rate": 20.0, "supplier": "Ofis Depo", "shelf_location": "G1", "min_stock": 20},
        {"name": "Dahle Masa Üstü Kalem Standı Metal", "category": "Ofis Gereçleri", "price": 85.00, "manufacturer": "Dahle", "stock_quantity": 50, "unit": "adet", "barcode": "4007885010019", "tax_rate": 20.0, "supplier": "Dahle Türkiye", "shelf_location": "G2", "min_stock": 5},
        {"name": "Helit Evrak Tepsisi Tek Katlı Siyah", "category": "Ofis Gereçleri", "price": 95.00, "manufacturer": "Helit", "stock_quantity": 60, "unit": "adet", "barcode": "4012497201015", "tax_rate": 20.0, "supplier": "Helit Türkiye", "shelf_location": "G2", "min_stock": 6},
        {"name": "Helit Evrak Tepsisi Çift Katlı Siyah", "category": "Ofis Gereçleri", "price": 145.00, "manufacturer": "Helit", "stock_quantity": 40, "unit": "adet", "barcode": "4012497201022", "tax_rate": 20.0, "supplier": "Helit Türkiye", "shelf_location": "G2", "min_stock": 4},
        {"name": "Sigel Masa Altı Yazı Tablası A2 Şeffaf", "category": "Ofis Gereçleri", "price": 75.00, "manufacturer": "Sigel", "stock_quantity": 40, "unit": "adet", "barcode": "4004360630019", "tax_rate": 20.0, "supplier": "Sigel Türkiye", "shelf_location": "G3", "min_stock": 4},
        {"name": "Tesa Bantlık Masa Üstü Şeffaf", "category": "Ofis Gereçleri", "price": 55.00, "manufacturer": "Tesa", "stock_quantity": 70, "unit": "adet", "barcode": "4042448045010", "tax_rate": 20.0, "supplier": "Tesa Türkiye", "shelf_location": "G3", "min_stock": 7},
        {"name": "Leitz Kağıt Ağırlığı Metal Gümüş", "category": "Ofis Gereçleri", "price": 65.00, "manufacturer": "Leitz", "stock_quantity": 30, "unit": "adet", "barcode": "4002432552018", "tax_rate": 20.0, "supplier": "Leitz Türkiye", "shelf_location": "G3", "min_stock": 3},

        # --- Baskı & Mürekkep ---
        {"name": "HP 302 Siyah Mürekkep Kartuşu", "category": "Baskı & Mürekkep", "price": 185.00, "manufacturer": "HP", "stock_quantity": 60, "unit": "adet", "barcode": "0889894118975", "tax_rate": 20.0, "supplier": "HP Türkiye", "shelf_location": "H1", "min_stock": 6},
        {"name": "HP 302 Renkli Mürekkep Kartuşu", "category": "Baskı & Mürekkep", "price": 215.00, "manufacturer": "HP", "stock_quantity": 50, "unit": "adet", "barcode": "0889894118982", "tax_rate": 20.0, "supplier": "HP Türkiye", "shelf_location": "H1", "min_stock": 5},
        {"name": "HP 302XL Siyah Yüksek Kapasiteli Kartuş", "category": "Baskı & Mürekkep", "price": 285.00, "manufacturer": "HP", "stock_quantity": 40, "unit": "adet", "barcode": "0889894118999", "tax_rate": 20.0, "supplier": "HP Türkiye", "shelf_location": "H1", "min_stock": 4},
        {"name": "Canon PG-545 Siyah Kartuş", "category": "Baskı & Mürekkep", "price": 195.00, "manufacturer": "Canon", "stock_quantity": 50, "unit": "adet", "barcode": "8714574600246", "tax_rate": 20.0, "supplier": "Canon Türkiye", "shelf_location": "H2", "min_stock": 5},
        {"name": "Canon CL-546 Renkli Kartuş", "category": "Baskı & Mürekkep", "price": 225.00, "manufacturer": "Canon", "stock_quantity": 45, "unit": "adet", "barcode": "8714574600253", "tax_rate": 20.0, "supplier": "Canon Türkiye", "shelf_location": "H2", "min_stock": 4},
        {"name": "Epson T1811 Siyah Kartuş", "category": "Baskı & Mürekkep", "price": 175.00, "manufacturer": "Epson", "stock_quantity": 40, "unit": "adet", "barcode": "8715946481043", "tax_rate": 20.0, "supplier": "Epson Türkiye", "shelf_location": "H3", "min_stock": 4},
        {"name": "Brother TN-2420 Toner Kartuşu Siyah", "category": "Baskı & Mürekkep", "price": 650.00, "manufacturer": "Brother", "stock_quantity": 20, "unit": "adet", "barcode": "4977766779449", "tax_rate": 20.0, "supplier": "Brother Türkiye", "shelf_location": "H4", "min_stock": 2},
        {"name": "HP CE285A 85A Toner Kartuşu", "category": "Baskı & Mürekkep", "price": 580.00, "manufacturer": "HP", "stock_quantity": 20, "unit": "adet", "barcode": "0884420586791", "tax_rate": 20.0, "supplier": "HP Türkiye", "shelf_location": "H4", "min_stock": 2},

        # --- Çanta & Okul Çantası ---
        {"name": "Herlitz Kalem Çantası Fermuar Kapaklı", "category": "Çanta & Aksesuar", "price": 95.00, "manufacturer": "Herlitz", "stock_quantity": 80, "unit": "adet", "barcode": "4008110119018", "tax_rate": 20.0, "supplier": "Herlitz Türkiye", "shelf_location": "I1", "min_stock": 8},
        {"name": "Herlitz Okul Çantası Loop Siyah", "category": "Çanta & Aksesuar", "price": 650.00, "manufacturer": "Herlitz", "stock_quantity": 30, "unit": "adet", "barcode": "4008110119025", "tax_rate": 20.0, "supplier": "Herlitz Türkiye", "shelf_location": "I1", "min_stock": 3},
        {"name": "Eastpak Padded Pak'r Sırt Çantası", "category": "Çanta & Aksesuar", "price": 1200.00, "manufacturer": "Eastpak", "stock_quantity": 20, "unit": "adet", "barcode": "5400522097065", "tax_rate": 20.0, "supplier": "Eastpak Türkiye", "shelf_location": "I2", "min_stock": 2},

        # --- Hesap & Teknik ---
        {"name": "Casio FX-82ES Plus Bilimsel Hesap Makinesi", "category": "Hesap & Teknik", "price": 350.00, "manufacturer": "Casio", "stock_quantity": 40, "unit": "adet", "barcode": "4971850197973", "tax_rate": 20.0, "supplier": "Casio Türkiye", "shelf_location": "J1", "min_stock": 4},
        {"name": "Casio HS-8VA Standart Hesap Makinesi", "category": "Hesap & Teknik", "price": 180.00, "manufacturer": "Casio", "stock_quantity": 50, "unit": "adet", "barcode": "4971850174370", "tax_rate": 20.0, "supplier": "Casio Türkiye", "shelf_location": "J1", "min_stock": 5},
        {"name": "Sharp EL-531 Bilimsel Hesap Makinesi", "category": "Hesap & Teknik", "price": 320.00, "manufacturer": "Sharp", "stock_quantity": 30, "unit": "adet", "barcode": "4974019923009", "tax_rate": 20.0, "supplier": "Sharp Türkiye", "shelf_location": "J1", "min_stock": 3},
        {"name": "Linex Teknik Çizim Seti 10 Parça", "category": "Hesap & Teknik", "price": 145.00, "manufacturer": "Linex", "stock_quantity": 40, "unit": "set", "barcode": "5708927890014", "tax_rate": 20.0, "supplier": "Linex Türkiye", "shelf_location": "J2", "min_stock": 4},

        # --- Takvim & Planlama ---
        {"name": "Herlitz Masa Takvimi 2025 Spiralli", "category": "Takvim & Planlama", "price": 75.00, "manufacturer": "Herlitz", "stock_quantity": 100, "unit": "adet", "barcode": "4008110880015", "tax_rate": 20.0, "supplier": "Herlitz Türkiye", "shelf_location": "K1", "min_stock": 10},
        {"name": "Güvercin Duvar Takvimi 2025 13 Yaprak", "category": "Takvim & Planlama", "price": 55.00, "manufacturer": "Güvercin", "stock_quantity": 150, "unit": "adet", "barcode": "8690526880013", "tax_rate": 20.0, "supplier": "Güvercin Kağıt", "shelf_location": "K1", "min_stock": 15},
        {"name": "Exacompta Planlama Panosu Aylık A3", "category": "Takvim & Planlama", "price": 185.00, "manufacturer": "Exacompta", "stock_quantity": 25, "unit": "adet", "barcode": "3130630000015", "tax_rate": 20.0, "supplier": "Exacompta Türkiye", "shelf_location": "K2", "min_stock": 3},
    ]

    added = 0
    skipped = 0
    for p in products:
        obj, created = Product.objects.get_or_create(
            name=p['name'],
            defaults={k: v for k, v in p.items() if k != 'name'}
        )
        if created:
            added += 1
            print(f"  [+] {obj.name}")
        else:
            skipped += 1

    print(f"\nDone. {added} products added, {skipped} already existed.")


if __name__ == '__main__':
    seed_db()
