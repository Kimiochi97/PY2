import sqlite3

conn = sqlite3.connect("arquivos.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(segredos);")
colunas = cursor.fetchall()

for coluna in colunas:
    print(coluna)

conn.close()