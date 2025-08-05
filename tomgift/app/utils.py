import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')

# Configuración SMTP para Brevo (antes Sendinblue)
SMTP_SERVER = 'smtp-relay.brevo.com'
SMTP_PORT = 587

# Función: Enviar correo con comprobante adjunto al correo oficial de TOMGIFT
def enviar_comprobante_email(usuario, monto, filename):
    destinatario = EMAIL_USER  # Se envía a sí mismo (tomgift@...)
    asunto = f"Nuevo comprobante de recarga - {usuario}"
    mensaje = f"""
    Se ha recibido un nuevo comprobante de recarga.

    Usuario: {usuario}
    Monto: ${monto:.2f} MXN

    El comprobante se adjunta a este correo.
    """

    # Ruta del comprobante
    filepath = os.path.join('app', 'static', 'comprobantes', filename)

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    # Adjuntar comprobante
    with open(filepath, 'rb') as file:
        part = MIMEApplication(file.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    # Enviar correo
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Error al enviar el comprobante por email: {e}")

# Función: Enviar correo cuando se sube un comprobante (usada en user_routes.py)
def enviar_correo_comprobante(username, monto, metodo, ruta_adjunto):
    asunto = f"Nuevo comprobante de recarga - {username}"
    mensaje = f"""
    Usuario: {username}
    Monto: {monto}
    Método: {metodo}

    Se adjunta el comprobante.
    """

    filename = os.path.basename(ruta_adjunto)

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_USER
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    with open(ruta_adjunto, 'rb') as f:
        part = MIMEApplication(f.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Error al enviar el correo con comprobante: {e}")

# Función: Enviar correo al usuario cuando su recarga ha sido aprobada
def enviar_correo_aprobacion(usuario, monto, fecha, correo_usuario):
    asunto = "✅ Tu recarga ha sido aprobada"
    mensaje = f"""
    Hola {usuario},

    Tu recarga por ${monto:.2f} MXN realizada el {fecha} ha sido APROBADA exitosamente.

    Ya puedes ver tu nuevo saldo en tu panel TOMGIFT.

    ¡Gracias por confiar en nosotros!

    — El equipo de TOMGIFT
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = correo_usuario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print(f"Error al enviar el correo de aprobación: {e}")
