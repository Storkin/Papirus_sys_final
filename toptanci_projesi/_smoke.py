import os, django
os.environ['PAPIRUS_ALLOWED_HOSTS']='testserver,127.0.0.1,localhost'
os.environ.setdefault('DJANGO_SETTINGS_MODULE','toptanci_projesi.settings')
django.setup()
from django.test.utils import setup_test_environment; setup_test_environment()
from django.test import Client
from django.contrib.auth.models import User
from django.db import transaction
from inventory.models import Product, Customer, Sale, StockMovement

patron,_=User.objects.get_or_create(username='_a_p'); patron.is_superuser=True; patron.is_staff=True; patron.save()
calisan,_=User.objects.get_or_create(username='_a_c'); calisan.is_superuser=False; calisan.is_staff=False; calisan.save()
cp=Client(); cp.force_login(patron)
cc=Client(); cc.force_login(calisan)

def chk(label, cond): print(('  OK  ' if cond else ' FAIL ')+label)

# sayfa erisilebilirligi
for path in ['/','/products/','/products/add/','/products/intake/','/products/import/','/sales/','/sales/new/','/stock-movements/','/customers/']:
    r=cp.get(path); chk(f'GET {path} = {r.status_code}', r.status_code==200)

try:
    with transaction.atomic():
        # SATIS: stok dusumu + hareket
        p=Product.objects.filter(stock_quantity__gte=5).first()
        old=p.stock_quantity
        r=cp.post('/sales/new/', {'customer':'','note':'test','product_0':str(p.pk),'quantity_0':'2','price_0':'10'})
        p.refresh_from_db()
        chk('Satis stok dusurdu (-2)', p.stock_quantity==old-2)
        chk('Satis hareketi olustu', StockMovement.objects.filter(product=p, note__startswith='Satış').exists())
        # STOK ARTIR/AZALT
        r=cp.post(f'/products/{p.pk}/increase/', {'amount':'5'}); p.refresh_from_db()
        chk('Stok artir', p.stock_quantity==old-2+5)
        r=cp.post(f'/products/{p.pk}/decrease/', {'amount':'100000'}); p.refresh_from_db()
        chk('Stoktan fazla azaltma engellendi', p.stock_quantity==old-2+5)
        # MUSTERI CRUD (patron)
        r=cp.post('/customers/add/', {'name':'Test Musteri','debt':'1.500,50'})
        m=Customer.objects.filter(name='Test Musteri').first()
        chk('Musteri olustu + borc parse (1500.5)', m is not None and abs(m.debt-1500.5)<0.01)
        # CALISAN musteri engeli
        chk('Calisan /customers/ engellendi', cc.get('/customers/').status_code==302)
        chk('Calisan /register/ engellendi', cc.get('/register/').status_code==302)
        chk('Calisan satis yapabilir', cc.get('/sales/new/').status_code==200)
        # negatif borc reddi
        r=cp.post('/customers/add/', {'name':'NegTest','debt':'-50'})
        chk('Negatif borc reddedildi', not Customer.objects.filter(name='NegTest').exists())
        raise RuntimeError('rb')
except RuntimeError: pass
User.objects.filter(username__in=['_a_p','_a_c']).delete()
print('temizlendi')
