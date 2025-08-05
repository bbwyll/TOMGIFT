import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = 'app/database.db'

# ---------------------- Inicialización ----------------------

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                saldo REAL DEFAULT 0
            )
        ''')
        conn.commit()

    # Crear tabla de recargas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recargas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            monto REAL NOT NULL,
            comprobante TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            fecha TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# ---------------------- Conexión ----------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    return get_db_connection()

# ---------------------- Usuarios ----------------------

def create_user(username, password, email):
    conn = get_db_connection()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('''
        INSERT INTO users (username, password, email, created_at, saldo)
        VALUES (?, ?, ?, ?, ?)
    ''', (username, password, email, created_at, 0.0))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def update_user_password(user_id, new_password_hash):
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (new_password_hash, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def acreditar_saldo(user_id, monto):
    conn = get_db_connection()
    conn.execute('UPDATE users SET saldo = saldo + ? WHERE id = ?', (monto, user_id))
    conn.commit()
    conn.close()

# ---------------------- Recargas ----------------------

def insertar_recarga(user_id, monto, comprobante, metodo):
    conn = get_db_connection()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute('''
        INSERT INTO recargas (user_id, monto, comprobante, metodo, estado, fecha)
        VALUES (?, ?, ?, ?, 'pendiente', ?)
    ''', (user_id, monto, comprobante, metodo, fecha))
    conn.commit()
    conn.close()

def obtener_recargas_pendientes():
    conn = get_db_connection()
    recargas = conn.execute('''
        SELECT recargas.*, users.username
        FROM recargas
        JOIN users ON recargas.user_id = users.id
        WHERE estado = 'pendiente'
    ''').fetchall()
    conn.close()
    return recargas

def actualizar_estado_recarga(recarga_id, nuevo_estado):
    conn = get_db_connection()
    conn.execute('UPDATE recargas SET estado = ? WHERE id = ?', (nuevo_estado, recarga_id))
    conn.commit()
    conn.close()

# ---------------------- Utilidades extra para rutas ----------------------

def actualizar_password(username, nueva_password):
    conn = get_db_connection()
    hashed = generate_password_hash(nueva_password)
    conn.execute('UPDATE users SET password = ? WHERE username = ?', (hashed, username))
    conn.commit()
    conn.close()

def eliminar_usuario(username):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    conn.close()

def guardar_recarga(user_id, monto, comprobante, metodo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO recargas (user_id, monto, comprobante, metodo, estado, fecha)
        VALUES (?, ?, ?, ?, 'pendiente', datetime('now'))
    """, (user_id, monto, comprobante, metodo))
    conn.commit()
    conn.close()


def aprobar_recarga(recarga_id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE recargas
        SET estado = 'aprobada', fecha = ?
        WHERE id = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), recarga_id))
    conn.commit()
    conn.close()

def rechazar_recarga(recarga_id):
    conn = get_db_connection()
    conn.execute('''
        UPDATE recargas
        SET estado = 'rechazada', fecha = ?
        WHERE id = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), recarga_id))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def add_user(username, email, hashed_password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password, created_at, saldo) VALUES (?, ?, ?, datetime('now'), 0)",
        (username, email, hashed_password)
    )
    conn.commit()
    conn.close()

def sumar_saldo(username, monto):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET saldo = saldo + ? WHERE username = ?", (float(monto), username))
    conn.commit()
    conn.close()

def obtener_recarga_por_id(recarga_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT recargas.*, users.username
        FROM recargas
        JOIN users ON recargas.user_id = users.id
        WHERE recargas.id = ?
    ''', (recarga_id,))
    recarga = cursor.fetchone()
    conn.close()
    return recarga

def obtener_recargas_pendientes():
    conn = get_db_connection()
    recargas = conn.execute('''
        SELECT recargas.*, users.username, users.email
        FROM recargas
        JOIN users ON recargas.user_id = users.id
        WHERE estado = 'pendiente'
    ''').fetchall()
    conn.close()
    return recargas


