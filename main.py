from app import app
from flask import render_template, redirect, url_for
from flask_mysqldb import MySQL
from app.menu import modelo_menu

# MYSQL Connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'post_sale'

# Settings
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

app.register_blueprint(modelo_menu)

@app.route('/')
def redirigir_a_menu():
    return redirect(url_for('modelo_menu.menu'))  # <- redirige al blueprint


if __name__ == "__main__":
    app.run(debug=True)
