# app/dashboard/admin_routes.py

from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.db import obtener_recarga_por_id, sumar_saldo
from flask import send_from_directory
from flask import Blueprint, send_from_directory
import os
from app.db import (
    get_user_by_username,
    obtener_recargas_pendientes,
    aprobar_recarga,
    rechazar_recarga,
    get_db
)

admin_routes = Blueprint('admin_routes', __name__)

def es_admin():
    return session.get('username') == 'qwpsjay'

@admin_routes.route('/admin')
def admin_panel():
    if not es_admin():
        flash("Acceso denegado. No tienes permisos de administrador.", "danger")
        return redirect(url_for('main.dashboard'))

    # Obtener recargas pendientes
    recargas = obtener_recargas_pendientes()
    # Obtener datos del usuario actual (admin)
    username = session.get("username")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, saldo, created_at FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    user_data = {
        "username": row["username"],
        "email": row["email"],
        "saldo": row["saldo"],
        "created_at": row["created_at"]
    }

    return render_template("admin.html", recargas=recargas, user_data=user_data)

@admin_routes.route('/admin/aprobar/<int:id>')
def aprobar(id):
    if not es_admin():
        flash("Acceso denegado. No tienes permisos de administrador.", "danger")
        return redirect(url_for('main.dashboard'))

    recarga = obtener_recarga_por_id(id)

    if recarga and recarga["estado"] == "pendiente":
           aprobar_recarga(id)
           sumar_saldo(recarga["username"], recarga["monto"])
           flash(f"Recarga aprobada y saldo actualizado para {recarga['username']}.", "success")

    else:
        flash("Esta recarga ya fue procesada o no existe.", "warning")

    return redirect(url_for('admin_routes.admin_panel'))

@admin_routes.route('/admin/rechazar/<int:id>')
def rechazar(id):
    if not es_admin():
        flash("Acceso denegado. No tienes permisos de administrador.", "danger")
        return redirect(url_for('main.dashboard'))

    rechazar_recarga(id)
    flash("Recarga rechazada correctamente.", "warning")
    return redirect(url_for('admin_routes.admin_panel'))

@admin_routes.route('/comprobantes/<nombre_archivo>')
def servir_comprobante(nombre_archivo):
    ruta_comprobantes = os.path.join(os.getcwd(), 'app', 'static', 'comprobantes')
    return send_from_directory(ruta_comprobantes, nombre_archivo)
