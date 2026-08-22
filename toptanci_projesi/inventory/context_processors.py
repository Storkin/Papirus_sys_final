import os


def lan_url(request):
    """launcher.py'nin ortam değişkenine yazdığı yerel ağ adresini (telefon/tablet
    bağlantısı için) tüm şablonlara aktarır. Sadece launcher.py ile çalışırken
    dolu olur; runserver ile geliştirme yaparken boş kalır."""
    return {'LAN_URL': os.environ.get('PAPIRUS_LAN_URL', '')}
