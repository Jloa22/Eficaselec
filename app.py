from flask import Flask, render_template, request, flash, url_for, send_from_directory, redirect
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Obtener la ruta base del proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY', '123')

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto')
def contacto():
    return render_template('index2.html')



# Manejo del formulario
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        nombre = request.form['nombre']
        correo = request.form['correo']
        mensaje = request.form['mensaje']

        msg = Message('Nuevo mensaje de contacto',
                     sender=app.config['MAIL_USERNAME'],
                     recipients=[app.config['MAIL_USERNAME']])
        msg.body = f"Nombre: {nombre}\nCorreo: {correo}\nMensaje: {mensaje}"
        mail.send(msg)
        
        flash("Mensaje enviado correctamente", "success")
    except Exception as e:
        print(f"Error: {e}")
        flash("Error al enviar el mensaje", "danger")
    
    return redirect(url_for('contacto'))

if __name__ == "__main__":
    app.run(debug=False)  