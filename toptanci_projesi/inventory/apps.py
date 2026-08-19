from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = 'inventory'

    def ready(self):
        # SQLite'ı WAL (Write-Ahead Logging) moduna al: okumalar yazmayı,
        # yazmalar okumaları bloklamaz — "database is locked" hatasını büyük
        # ölçüde azaltır (özellikle uzun içe aktarma işlemlerinde).
        from django.db.backends.signals import connection_created

        def _set_sqlite_pragmas(sender, connection, **kwargs):
            if connection.vendor == 'sqlite':
                cursor = connection.cursor()
                cursor.execute('PRAGMA journal_mode=WAL;')
                cursor.execute('PRAGMA synchronous=NORMAL;')

        # weak=False: yereldeki fonksiyon çöp toplanıp sinyalin sessizce
        # etkisiz kalmaması için güçlü referansla bağlanır.
        connection_created.connect(_set_sqlite_pragmas, weak=False)
