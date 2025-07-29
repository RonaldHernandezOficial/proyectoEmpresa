from flask import Flask, render_template, redirect, url_for
from flask_mysqldb import MySQL
from flask_caching import Cache
import psutil
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# Creación de la aplicación Flask
application = Flask(__name__)

# Configuración de MySQL
application.config['MYSQL_HOST'] = 'localhost'
application.config['MYSQL_USER'] = 'root'
application.config['MYSQL_PASSWORD'] = ''  # ¡Cuidado! No deberías tener contraseña vacía en producción
application.config['MYSQL_DB'] = 'post_sale'
application.secret_key = 'mysecretkey'  # Deberías usar una clave más segura en producción

# Inicialización de MySQL
mysql = MySQL(application)

# Importación y registro de blueprints
from app.menu import modelo_menu
application.register_blueprint(modelo_menu)

@application.route('/')
def redirigir_a_menu():
    return redirect(url_for('modelo_menu.menu'))

@application.route('/server-status')
def server_status():
    return {
        "cpu": f"{psutil.cpu_percent()}%",
        "ram": f"{psutil.virtual_memory().percent}%"
    }

if __name__ == "__main__":
    application.run(debug=True)