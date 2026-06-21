# -*- coding: utf-8 -*-
"""
Papirus SYS - Masaüstü başlatıcı.
Django uygulamasını arka planda (Waitress WSGI) çalıştırır ve
pywebview ile kendi penceresinde açar. Tarayıcı/terminal gerekmez.
"""
import os
import sys
import socket
import threading
import time
from urllib.request import urlopen

import webview
from waitress import serve

# --- Proje yolunu ve Django ayarlarını hazırla ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toptanci_projesi.settings')

import django  # noqa: E402
django.setup()

from toptanci_projesi.wsgi import application  # noqa: E402

HOST = '127.0.0.1'
PREFERRED_PORT = 8731  # sabit port: oturum çerezinin origin'i hep aynı kalsın


def _port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, port))
            return True
        except OSError:
            return False


def pick_port():
    """Önce sabit portu dene; doluysa boş bir port bul."""
    if _port_free(PREFERRED_PORT):
        return PREFERRED_PORT
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, 0))
        return s.getsockname()[1]


PORT = pick_port()
URL = f'http://{HOST}:{PORT}/'

# Çerezlerin (oturum) diske yazılacağı kalıcı klasör — "oturum açık kalsın" için şart
STORAGE_PATH = os.path.join(
    os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'PapirusSYS', 'webview'
)
os.makedirs(STORAGE_PATH, exist_ok=True)


def backup_db():
    """Her açılışta veritabanını tarihli olarak yedekler; son 15 yedeği tutar."""
    import shutil
    import glob
    import datetime
    db = os.path.join(BASE_DIR, 'db.sqlite3')
    if not os.path.exists(db):
        return
    bdir = os.path.join(BASE_DIR, 'backups')
    os.makedirs(bdir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    try:
        shutil.copy2(db, os.path.join(bdir, 'db_' + ts + '.sqlite3'))
    except OSError:
        return
    # son 15 yedeği tut, eskileri sil (RESET yedekleri korunur)
    files = sorted(glob.glob(os.path.join(bdir, 'db_2*.sqlite3')))
    for f in files[:-15]:
        try:
            os.remove(f)
        except OSError:
            pass


def run_server():
    """Django'yu Waitress ile sessizce sun."""
    serve(application, host=HOST, port=PORT, threads=8, _quiet=True)


def wait_until_ready(timeout=20):
    """Sunucu yanıt verene kadar bekle."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            urlopen(URL, timeout=1)
            return True
        except Exception:
            time.sleep(0.2)
    return False


def main():
    # Açılışta otomatik yedek al (veri kaybına karşı)
    backup_db()

    # Sunucuyu arka plan thread'inde başlat (uygulama kapanınca o da kapanır)
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    wait_until_ready()

    # Masaüstü penceresini aç
    webview.create_window(
        'Papirus SYS',
        URL,
        width=1280,
        height=820,
        min_size=(1024, 680),
        confirm_close=True,
    )
    # private_mode=False + sabit storage_path -> çerezler diske yazılır,
    # uygulama kapanıp açılınca "oturum açık kalsın" korunur.
    webview.start(private_mode=False, storage_path=STORAGE_PATH)


if __name__ == '__main__':
    main()
