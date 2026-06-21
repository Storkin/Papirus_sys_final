# -*- coding: utf-8 -*-
"""Elle veritabanı yedeği al. Çalıştır: python yedekle.py
Yedekler 'backups/' klasörüne tarihli olarak kaydedilir."""
import os
import shutil
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(BASE_DIR, 'db.sqlite3')

if not os.path.exists(db):
    print('db.sqlite3 bulunamadı.')
else:
    bdir = os.path.join(BASE_DIR, 'backups')
    os.makedirs(bdir, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(bdir, 'db_ELLE_' + ts + '.sqlite3')
    shutil.copy2(db, dest)
    print('Yedek alındı:', dest)
