from flask import Flask, render_template, redirect, url_for, Response
from flask_mysqldb import MySQL
from flask_caching import Cache
import psutil
import os
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# Creación de la aplicación Flask
application = Flask(__name__)


@application.route('/prueba-site')
def prueba_site():
    return "RUTA NUEVA FUNCIONANDO"

@application.route('/robots.txt')
def robots():
    return """User-agent: *
Allow: /

Sitemap: https://www.fabriautomaticassas.com/sitemap.xml
""", 200, {'Content-Type': 'text/plain'}


# Configuración de MySQL
application.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
application.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
application.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")  # ¡Cuidado! No deberías tener contraseña vacía en producción
application.config['MYSQL_DB'] = os.environ.get("post_sale")
application.secret_key = os.environ.get("s8f7as8f7as8f7a8s7f8as7f8as7")  # Deberías usar una clave más segura en producción

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
    application.run()