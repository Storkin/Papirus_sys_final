"""Papirus SYS - sifre sifirlama yardimcisi.

Bu dosya dogrudan calistirilmak icin degil, sifre_sifirla.ps1 tarafindan
cagrilmak icindir. Sadece bilgisayarin basindayken (dosyaya erisimi olan kisi)
kullanilabilir; ag/telefon uzerinden erisilemez.

Kullanim:
    python sifre_araci.py liste
    python sifre_araci.py degistir <kullanici_id>
        -> yeni sifre PAPIRUS_YENI_SIFRE ortam degiskeninden okunur
           (komut satirinda gorunmesin diye)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toptanci_projesi.settings')

# Turkce karakterli kullanici adlari Windows konsolunda bozulmasin
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402


def liste():
    """Her satir: id|kullanici_adi|rol"""
    for u in User.objects.order_by('id'):
        rol = 'Patron' if u.is_superuser else 'Kullanici'
        print(f'{u.id}|{u.username}|{rol}')


def degistir(user_id):
    yeni = os.environ.get('PAPIRUS_YENI_SIFRE', '')
    if not yeni:
        print('HATA: Yeni sifre bos.')
        return 1
    try:
        u = User.objects.get(pk=int(user_id))
    except (User.DoesNotExist, ValueError):
        print('HATA: Kullanici bulunamadi.')
        return 1
    u.set_password(yeni)
    u.save()
    print(f'TAMAM|{u.username}')
    return 0


def main():
    if len(sys.argv) < 2:
        print('HATA: Komut belirtilmedi.')
        return 1
    komut = sys.argv[1]
    if komut == 'liste':
        liste()
        return 0
    if komut == 'degistir':
        if len(sys.argv) < 3:
            print('HATA: Kullanici id belirtilmedi.')
            return 1
        return degistir(sys.argv[2])
    print('HATA: Bilinmeyen komut.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
