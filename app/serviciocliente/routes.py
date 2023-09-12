from flask import Flask, render_template, request, redirect, url_for, flash
from . import modelo_servicio
from flask_mysqldb import MySQL
import app

#Crear una instancia Flask
app = Flask(__name__)

# MYSQL Connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'post_sale'

# Settings
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@modelo_servicio.route("/reseñas")
def reseña():
    return render_template("serviciocliente.html")

@modelo_servicio.route('/insertar', methods=['GET', 'POST'])
def agregar_reseña():
    if request.method == 'POST':
        tipoPqrs = request.form['tipoPqrs']
        descripcionPqrs = request.form['descripcionPqrs']
        cur = mysql.connection.curso()
        cur.execute('INSERT INTO  pqrs (tipoPqrs, descripcionPqrs) VALUES (%s,%s)',
                    (tipoPqrs, descripcionPqrs))
        mysql.connection.commit()
        flash("¡PQR'S registrado exitosamente!")
    return redirect(url_for('modelo_servicio.insertar'))