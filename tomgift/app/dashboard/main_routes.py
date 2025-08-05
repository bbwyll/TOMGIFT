# app/dashboard/main_routes.py

from flask import Blueprint, render_template, session, redirect, url_for
from app.db import get_user_by_username

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    username = session['username']
    user = get_user_by_username(username)

    if user:
        user_data = {
            'username': user['username'],
            'email': user['email'],
            'saldo': user['saldo'],
            'created_at': user['created_at']
        }
        return render_template('dashboard.html', user_data=user_data)
    else:
        return redirect(url_for('auth.login'))
