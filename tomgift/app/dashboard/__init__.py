# app/dashboard/__init__.py

from flask import Flask, render_template
from dotenv import load_dotenv
import os
from app.db import init_db
from app.extensions import mail

# Importar blueprints desde los nuevos archivos
from app.dashboard.main_routes import main
from app.dashboard.auth_routes import auth
from app.dashboard.user_routes import user_routes 
from app.dashboard.admin_routes import admin_routes as admin

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

    # Configuración del correo
    app.config.update(
        MAIL_SERVER=os.getenv("MAIL_SERVER"),
        MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
        MAIL_USE_TLS=os.getenv("MAIL_USE_TLS", "True") == "True",
        MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
        MAIL_DEFAULT_SENDER=os.getenv("MAIL_DEFAULT_SENDER"),
    )

    # Inicializar extensiones y base de datos
    mail.init_app(app)
    init_db()

    # Registrar todos los Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user_routes)
    app.register_blueprint(admin)

    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html"), 500

    return app
