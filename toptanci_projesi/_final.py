import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','toptanci_projesi.settings')
django.setup()
from django.contrib.auth.models import User
from inventory.models import Product
# admin sifresi hala admin123 mu? (guvenlik)
a=User.objects.filter(username='admin').first()
if a:
    print('admin sifresi hala "admin123" mu:', a.check_password('admin123'))
    print('admin superuser mu:', a.is_superuser)
# kac kullanici var
print('Toplam kullanici:', User.objects.count(), '| superuser:', User.objects.filter(is_superuser=True).count())
# temizlenmesi gereken cop kayitlar
print('\nTemizlik adaylari:')
print('  Baslik satiri urun (barcode=Barkod):', Product.objects.filter(barcode='Barkod').count())
print('  asdadsj test urunu:', Product.objects.filter(name='asdadsj').count())
import os as _os
db=_os.path.getsize('db.sqlite3')/1024
print('\ndb.sqlite3 boyutu: %.0f KB' % db)
