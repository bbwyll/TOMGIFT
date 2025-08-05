import sqlite3

conn = sqlite3.connect('app/database.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE recargas ADD COLUMN metodo TEXT DEFAULT 'transferencia'")
    print("Columna 'metodo' agregada.")
except sqlite3.OperationalError as e:
    print("Ya existe o error:", e)

conn.commit()
conn.close()
