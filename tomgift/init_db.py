import sqlite3

def agregar_columna_saldo():
    conn = sqlite3.connect('app/database.db')
    try:
        conn.execute('ALTER TABLE users ADD COLUMN saldo REAL DEFAULT 0')
        conn.commit()
        print("✅ Columna 'saldo' agregada correctamente.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e):
            print("⚠️ La columna 'saldo' ya existe.")
        else:
            print(f"❌ Error inesperado: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    agregar_columna_saldo()
