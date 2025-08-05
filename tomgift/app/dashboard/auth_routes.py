# app/dashboard/auth_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import (
    get_user_by_username,
    get_user_by_email,
    create_user,
    add_user
)
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username:
            return render_template('register.html', error='El nombre de usuario es obligatorio.', field_error='username')
        if not email:
            return render_template('register.html', error='El correo electrónico es obligatorio.', field_error='email')
        if not password:
            return render_template('register.html', error='La contraseña es obligatoria.', field_error='password')
        if password != confirm_password:
            return render_template('register.html', error='Las contraseñas no coinciden.', field_error='confirm_password')

        if get_user_by_username(username):
            return render_template('register.html', error='Este nombre de usuario ya está en uso.', field_error='username')
        if get_user_by_email(email):
            return render_template('register.html', error='Este correo ya está en uso.', field_error='email')

        hashed_pw = generate_password_hash(password)
        add_user(username, email, hashed_pw)

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username:
            return render_template('login.html', error='El nombre de usuario es obligatorio.', field_error='username')
        if not password:
            return render_template('login.html', error='La contraseña es obligatoria.', field_error='password')

        user = get_user_by_username(username)
        if not user:
            return render_template('login.html', error='El usuario no existe.', field_error='username')
        if not check_password_hash(user['password'], password):
            return render_template('login.html', error='Contraseña incorrecta.', field_error='password')

        session['user_id'] = user['id']
        session['username'] = user['username']

        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Sesión cerrada exitosamente.', 'success')
    return redirect(url_for('auth.login'))
