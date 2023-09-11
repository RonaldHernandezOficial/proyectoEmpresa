from flask import Flask, render_template, request, redirect, url_for
from . import modelo_login
import app
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'post_sale'

mysql = MySQL(app)

@modelo_login.route("/olvidar_contraseña")
def nuevo_usuario():
    return render_template("olvidarcon.html")

@modelo_login.route("/login")
def login():
    return render_template("login.html")

@modelo_login.route('/insertar' , methods=['GET','POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombreUsuario = request.form['nombre']
        apellidoUsuario = request.form['apellido']
        emailUsuario = request.form['email']
        telefonoUsuario = request.form['telefono']
        contrasenaUsuario = request.form['contrasena']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuario (nombreUsuario, apellidoUsuario, emailUsuario, telefonoUsuario, contrasenaUsuario) VALUES (%s, %s, %s, %s, %s)', 
                    (nombreUsuario, apellidoUsuario, emailUsuario, telefonoUsuario, contrasenaUsuario))
        mysql.connection.commit()
    return render_template('login.html')