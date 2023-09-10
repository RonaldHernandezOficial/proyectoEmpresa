from flask import Flask, render_template, request, redirect, url_for
from . import modelo_garantias
from flask_mysqldb import MySQL
import app

#Crear una instancia Flask
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'post_sale'

mysql = MySQL(app)

@modelo_garantias.route('/garantia')
def garantia():
    return render_template('garantias.html')

@modelo_garantias.route('/insertar')
def insertar():
    return render_template('insertar_garantias.html')
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
    return 'recibido'

@modelo_garantias.route('/editar_garantia')
def editar_garantia():
    return 'Garantía editada'

@modelo_garantias.route('/eliminar_garantia')
def eliminar_garantia():
    return 'Garantía eliminada'

