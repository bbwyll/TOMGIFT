# app/dashboard/user_routes.py

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.db import get_user_by_username, update_user_password, delete_user, guardar_recarga
from app.utils import enviar_correo_comprobante
import os
from werkzeug.utils import secure_filename
from datetime import datetime

user_routes = Blueprint('user_routes', __name__)

def obtener_datos_usuario():
    username = session.get('username')
    if not username:
        return None
    return get_user_by_username(username)

@user_routes.route('/cuenta', methods=['GET', 'POST'])
def cuenta():
    user_data = obtener_datos_usuario()
    if not user_data:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if request.form.get("change_password"):
            current_password = request.form["current_password"]
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            if new_password != confirm_password:
                flash("Las nuevas contraseñas no coinciden", "error")
                return redirect(url_for("user_routes.cuenta"))

            update_user_password(user_data["id"], new_password)
            flash("Contraseña actualizada exitosamente", "success")
            return redirect(url_for("user_routes.cuenta"))

        if request.form.get("delete_account"):
            delete_user(user_data["id"])
            session.pop("username", None)
            flash("Cuenta eliminada correctamente", "success")
            return redirect(url_for("auth.login"))

    return render_template("cuenta.html", user_data=user_data)

@user_routes.route('/productos')
def productos():
    user_data = obtener_datos_usuario()
    if not user_data:
        return redirect(url_for('auth.login'))
    return render_template("productos.html", user_data=user_data)

@user_routes.route('/recargar', methods=['GET', 'POST'])
def recargar():
    user_data = obtener_datos_usuario()
    if not user_data:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        monto = request.form.get('monto', '').strip()
        metodo = request.form.get('metodo', '').strip()
        archivo = request.files.get('comprobante')
        
        if archivo:
            filename = secure_filename(archivo.filename)
            ruta_comprobante = os.path.join('app/static/comprobantes', filename)
            archivo.save(ruta_comprobante)

            guardar_recarga(user_data['username'], monto, ruta_comprobante, metodo)

            enviar_correo_comprobante(user_data['username'], monto, metodo, ruta_comprobante)

            flash('Comprobante enviado. Espera aprobación del administrador.', 'success')
            return redirect(url_for('user_routes.recargar'))

    return render_template("recargar.html", user_data=user_data)

@user_routes.route('/contactar')
def contactar():
    user_data = obtener_datos_usuario()
    if not user_data:
        return redirect(url_for('auth.login'))
    return render_template("contactar.html", user_data=user_data)
