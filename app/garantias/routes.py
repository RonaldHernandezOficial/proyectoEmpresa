from flask import Flask, render_template, request, redirect, url_for, flash
from . import modelo_garantias
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

@modelo_garantias.route('/garantia')
def garantia():
    return render_template('garantias.html')

@modelo_garantias.route('/insertar')
def insertar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM garantia')
    data = cur.fetchall()
    return render_template('insertar_garantias.html' , garantias = data)

@modelo_garantias.route('/agregar_garantia' , methods=['GET','POST'])
def agregar_garantia():
    if request.method == 'POST':
        fechaGarantia = request.form['fechaGarantia']
        descripcionGarantia = request.form['descripcionGarantia']
        garantia = request.form['garantia']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO garantia (fechaGarantia, descripcionGarantia, tipoGarantia) VALUES (%s, %s, %s)', 
                    (fechaGarantia, descripcionGarantia, garantia))
        mysql.connection.commit()
        flash('!Garantía agregada satisfactoriamente¡')
    return redirect(url_for('modelo_garantias.insertar'))
