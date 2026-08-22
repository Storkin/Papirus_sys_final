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


def get_lan_ip():
    """Bu bilgisayarın yerel ağ (WiFi) IP adresini bul. UDP 'connect' sadece
    rota seçer, gerçekten paket göndermez — internet olmasa da çalışır."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'
    finally:
        s.close()


LAN_IP = get_lan_ip()
HOST = '127.0.0.1'      # Waitress SADECE burada dinler; masaüstü penceresi + HTTPS proxy buradan bağlanır
PREFERRED_PORT = 8731    # sabit port: oturum çerezinin origin'i hep aynı kalsın
HTTPS_PORT_PREFERRED = 8443


def _port_free(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def pick_port(host, preferred):
    """Önce tercih edilen portu dene; doluysa boş bir port bul."""
    if _port_free(host, preferred):
        return preferred
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 0))
        return s.getsockname()[1]


PORT = pick_port(HOST, PREFERRED_PORT)
URL = f'http://{HOST}:{PORT}/'

HTTPS_PORT = pick_port('0.0.0.0', HTTPS_PORT_PREFERRED)
LAN_URL = f'https://{LAN_IP}:{HTTPS_PORT}/'
os.environ['PAPIRUS_LAN_URL'] = LAN_URL

# Aşağıdakiler django.setup()'tan ÖNCE ayarlanmalı — settings.py bunları
# import anında (yani setup() sırasında) okuyor:
# 1) Aynı WiFi'daki telefon/tabletten erişilebilsin diye ALLOWED_HOSTS'a bu
#    bilgisayarın yerel IP'sini ekle.
if 'PAPIRUS_ALLOWED_HOSTS' not in os.environ:
    os.environ['PAPIRUS_ALLOWED_HOSTS'] = f'127.0.0.1,localhost,{LAN_IP}'
# 2) HTTPS üzerinden gelen POST isteklerinde CSRF Origin kontrolü geçsin diye.
os.environ.setdefault('PAPIRUS_CSRF_TRUSTED_ORIGINS', LAN_URL.rstrip('/'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toptanci_projesi.settings')

import django  # noqa: E402
django.setup()

from toptanci_projesi.wsgi import application  # noqa: E402


CERT_PATH = os.path.join(BASE_DIR, 'papirus_cert.pem')
KEY_PATH = os.path.join(BASE_DIR, 'papirus_key.pem')


def ensure_tls_cert():
    """Kendinden imzalı (self-signed) bir HTTPS sertifikası üretir — telefonun
    kamerayı kullanabilmesi için 'güvenli bağlam' (HTTPS) şart. Bir kere
    üretilir; sertifikadaki IP artık geçerli değilse (ağ değiştiyse) yeniden
    üretilir. Telefon ilk bağlantıda bir kerelik 'güvenilmiyor' uyarısı
    gösterir — 'Devam Et' ile geçilir, sonrasında sorunsuz çalışır."""
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    import datetime
    import ipaddress

    if os.path.exists(CERT_PATH) and os.path.exists(KEY_PATH):
        try:
            with open(CERT_PATH, 'rb') as f:
                cert = x509.load_pem_x509_certificate(f.read())
            san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
            ips = san.get_values_for_type(x509.IPAddress)
            if ipaddress.ip_address(LAN_IP) in ips and cert.not_valid_after_utc > datetime.datetime.now(datetime.timezone.utc):
                return  # geçerli, yeniden üretmeye gerek yok
        except Exception:
            pass  # okunamadıysa/bozuksa yeniden üret

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'Papirus SYS')])
    san_list = [x509.DNSName('localhost'), x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]
    try:
        san_list.append(x509.IPAddress(ipaddress.ip_address(LAN_IP)))
    except ValueError:
        pass
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(days=1))
        .not_valid_after(now + datetime.timedelta(days=3650))
        .add_extension(x509.SubjectAlternativeName(san_list), critical=False)
        .sign(key, hashes.SHA256())
    )
    with open(KEY_PATH, 'wb') as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))
    with open(CERT_PATH, 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))


def run_tls_proxy():
    """0.0.0.0:HTTPS_PORT üzerinde TLS ile dinler, gelen her bağlantıyı düz
    metin olarak 127.0.0.1:PORT'taki Waitress'e aktarır (basit TCP relay).
    Waitress'e hiç dokunmadan, telefon için gerçek HTTPS sağlar."""
    import ssl
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(CERT_PATH, KEY_PATH)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(('0.0.0.0', HTTPS_PORT))
    listener.listen(20)

    def pipe(src, dst):
        try:
            while True:
                data = src.recv(65536)
                if not data:
                    break
                dst.sendall(data)
        except OSError:
            pass
        finally:
            try:
                dst.shutdown(socket.SHUT_WR)
            except OSError:
                pass

    def handle(raw_client):
        try:
            client = ctx.wrap_socket(raw_client, server_side=True)
        except Exception:
            raw_client.close()
            return
        try:
            backend = socket.create_connection((HOST, PORT), timeout=10)
        except OSError:
            client.close()
            return
        t1 = threading.Thread(target=pipe, args=(client, backend), daemon=True)
        t2 = threading.Thread(target=pipe, args=(backend, client), daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        client.close()
        backend.close()

    while True:
        try:
            conn, _addr = listener.accept()
        except OSError:
            break
        threading.Thread(target=handle, args=(conn,), daemon=True).start()

# Çerezlerin (oturum) diske yazılacağı kalıcı klasör — "oturum açık kalsın" için şart
STORAGE_PATH = os.path.join(
    os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'PapirusSYS', 'webview'
)
os.makedirs(STORAGE_PATH, exist_ok=True)


KEEP_BACKUPS = 30  # her konumda tutulacak yedek sayısı


def backup_dirs():
    """Yedeklerin yazılacağı KONUMLAR — proje klasörünün DIŞINDA, birden fazla yerde.
    Böylece proje/uygulama silinse bile yedekler durur; OneDrive varsa buluta da gider."""
    home = os.path.expanduser('~')
    dirs = []
    # 1) OneDrive (buluta otomatik yüklenir — bilgisayar tamamen gitse bile veri durur)
    od = os.environ.get('OneDrive') or os.environ.get('OneDriveConsumer')
    if od and os.path.isdir(od):
        dirs.append(os.path.join(od, 'Papirus_Yedek'))
    # 2) Kullanıcı klasöründe sabit yer (proje klasörü silinse de durur)
    dirs.append(os.path.join(home, 'Papirus_Yedek'))
    # 3) Belgeler klasörü
    for docs in (os.path.join(home, 'Documents'), os.path.join(home, 'Belgeler')):
        if os.path.isdir(docs):
            dirs.append(os.path.join(docs, 'Papirus_Yedek'))
            break
    return dirs


def backup_db():
    """Veritabanını birden fazla güvenli konuma tarihli olarak yedekler."""
    import shutil
    import glob
    import datetime
    import sqlite3
    db = os.path.join(BASE_DIR, 'db.sqlite3')
    if not os.path.exists(db):
        return
    # WAL modunda son işlemler önce ana dosyaya "checkpoint" edilmeli, yoksa
    # ham dosya kopyası son yazılan verileri kaçırabilir.
    try:
        conn = sqlite3.connect(db, timeout=10)
        conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
        conn.close()
    except Exception:
        pass
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    for bdir in backup_dirs():
        try:
            os.makedirs(bdir, exist_ok=True)
            shutil.copy2(db, os.path.join(bdir, 'db_' + ts + '.sqlite3'))
            # her konumda son KEEP_BACKUPS yedeği tut
            files = sorted(glob.glob(os.path.join(bdir, 'db_2*.sqlite3')))
            for f in files[:-KEEP_BACKUPS]:
                try:
                    os.remove(f)
                except OSError:
                    pass
        except OSError:
            continue


def periodic_backup(interval=7200):
    """Uygulama açıkken her 2 saatte bir otomatik yedek al (yeniden başlatmasan da)."""
    while True:
        time.sleep(interval)
        try:
            backup_db()
        except Exception:
            pass


def run_server():
    """Django'yu Waitress ile sessizce sun (sadece 127.0.0.1 — dışarıya HTTPS proxy açar)."""
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
    # Açılışta otomatik yedek al (veri kaybına karşı) — güvenli konumlara
    backup_db()
    # Uygulama açık kaldıkça periyodik yedek (her 2 saat)
    threading.Thread(target=periodic_backup, daemon=True).start()

    # Sunucuyu arka plan thread'inde başlat (uygulama kapanınca o da kapanır)
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    # Telefon/tablet için HTTPS: sertifika hazırla + TLS proxy'yi başlat.
    # Herhangi bir sebeple kurulamazsa (ör. cryptography sorunlu) masaüstü
    # uygulaması yine de sorunsuz açılsın diye sessizce devam ediyoruz.
    try:
        ensure_tls_cert()
        threading.Thread(target=run_tls_proxy, daemon=True).start()
    except Exception:
        pass

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
