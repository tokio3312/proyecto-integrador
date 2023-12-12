from flask import Flask, render_template, request, redirect, url_for
import qrcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(__name__)

# Configuración para el envío de correos
EMAIL_ADDRESS = 'correo'
EMAIL_PASSWORD = 'contraseña'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar_qr', methods=['POST'])
def generar_qr():
    nombre = request.form['nombre']
    correo = request.form['correo']
    edad = request.form['edad']

    # Crear datos para el código QR
    datos_usuario = f"Nombre: {nombre}\nCorreo: {correo}\nEdad: {edad}"

    # Generar código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(datos_usuario)
    qr.make(fit=True)
    qr_imagen = qr.make_image(fill_color="black", back_color="white")

    # Guardar el código QR como imagen
    qr_imagen_path = f"static/qrcodes/{correo}.png"
    qr_imagen.save(qr_imagen_path)

    # Enviar correo con el código QR adjunto
    enviar_correo(correo, qr_imagen_path)

    return render_template('exito.html', correo=correo)

def enviar_correo(destinatario, adjunto):
    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_ADDRESS
    mensaje['To'] = destinatario
    mensaje['Subject'] = 'Código QR de Usuario'

    cuerpo = MIMEText('Adjunto encontrarás tu código QR generado con tus datos.')
    mensaje.attach(cuerpo)

    with open(adjunto, 'rb') as archivo_adjunto:
        adjunto_mensaje = MIMEText(archivo_adjunto.read(), 'base64')
        adjunto_mensaje.add_header('Content-Disposition', 'attachment', filename=f'codigo_qr.png')
        mensaje.attach(adjunto_mensaje)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor_smtp:
        servidor_smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        servidor_smtp.sendmail(EMAIL_ADDRESS, destinatario, mensaje.as_string())

if __name__ == '__main__':
    app.run(debug=True)
