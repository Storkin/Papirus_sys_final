import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','toptanci_projesi.settings')
django.setup()
from inventory.models import Product, Customer, Sale, StockMovement, ReferenceBarcode
from django.db.models import Count, Q
print('Urun:', Product.objects.count(), '| Musteri:', Customer.objects.count(), '| Satis:', Sale.objects.count(), '| Hareket:', StockMovement.objects.count(), '| Ref barkod:', ReferenceBarcode.objects.count())
# bozuk/supheli barkodlar (cok uzun veya harf iceren)
bad_bc = Product.objects.filter(barcode__regex=r'[A-Za-zÇĞİÖŞÜçğıöşü]')
print('Harf iceren barkod (bozuk):', bad_bc.count())
for p in bad_bc[:5]: print('   ', repr(p.barcode), '|', p.name[:30])
# cok uzun barkod
longbc = [p for p in Product.objects.all() if len(p.barcode)>14]
print('14 haneden uzun barkod:', len(longbc))
# negatif/asiri stok
print('Negatif stok:', Product.objects.filter(stock_quantity__lt=0).count())
huge = Product.objects.filter(stock_quantity__gt=100000)
print('Asiri stok (>100k):', huge.count(), [f"{p.name}:{p.stock_quantity}" for p in huge[:3]])
# fiyati 0 olan urun
print('Fiyati 0 urun:', Product.objects.filter(price=0).count())
# bos/sacma isimli urun
print('Cok kisa isimli urun (<=3):', Product.objects.filter(name__regex=r'^.{1,3}$').count())
# ayni barkoddan birden fazla urun (cakisma)
dup = Product.objects.exclude(barcode='').values('barcode').annotate(n=Count('id')).filter(n__gt=1)
print('Ayni barkoddan birden fazla urun:', dup.count())
for d in dup[:5]: print('   ', d['barcode'], '->', d['n'], 'kez')
