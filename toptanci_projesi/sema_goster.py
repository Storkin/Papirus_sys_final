import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name LIKE 'inventory_%' ORDER BY name")
for row in cur.fetchall():
    print('=' * 70)
    print(row[0] + ';')
    print()
con.close()
