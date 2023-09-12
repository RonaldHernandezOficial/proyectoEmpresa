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

@modelo_servicio.route("/pqr")
def inicio():
    return render_template("serviciocliente.html")

@modelo_servicio.route('/insertar')
def insertar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pqrs')
    data = cur.fetchall()   
    return render_template('registrarpqr.html' , servicios = data)

@modelo_servicio.route('/insertar', methods=['GET', 'POST'])
def agregar_reseña():
    if request.method == 'POST':
        tipoPqrs = request.form['tipoPqrs']
        descripcionPqrs = request.form['descripcionPqrs']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO  pqrs (tipoPqrs, descripcionPqrs) VALUES (%s,%s)',
                    (tipoPqrs, descripcionPqrs))
        mysql.connection.commit()
        flash("¡PQR'S registrado exitosamente!")
    return redirect(url_for('modelo_servicio.insertar'))


@modelo_servicio.route('/eliminar_servicio/<string:id>')
def eliminar_servicio(id):
    cur = mysql.connection.cursor()  
    cur.execute('DELETE FROM pqrs WHERE idPqrs = {0}'.format(id))
    mysql.connection.commit() 
    flash('Pqrs eliminado satisfactoriamente')
    return redirect(url_for('modelo_servicio.insertar'))