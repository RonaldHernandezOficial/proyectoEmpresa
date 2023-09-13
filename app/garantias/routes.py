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

@modelo_garantias.route('/editar_garantia/<id>')
def obtener_garantia(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM garantia WHERE idGarantia = %s', (id))
    dataG = cur.fetchall()
    return render_template('editar_garantias.html', garantia = dataG[0])

@modelo_garantias.route('/actualizar_garantia/<id>', methods = ['POST'])
def actualizar_garantia(id):
    if request.method == 'POST':
        fechaGarantia = request.form['fechaGarantia']
        descripcionGarantia = request.form['descripcionGarantia']
        tipoGarantia = request.form['garantia']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE garantia 
            SET fechaGarantia = %s,
                    descripcionGarantia = %s,
                    tipoGarantia = %s
            WHERE idGarantia = %s
            """, (fechaGarantia, descripcionGarantia, tipoGarantia, estadoGarantia, id))
        flash('!Garantía actualizada satisfactoriamente¡')
        cur.connection.commit()
        return redirect(url_for('modelo_garantias.insertar'))

@modelo_garantias.route('/eliminar_garantia/<string:id>')
def eliminar_garantia(id):
    cur = mysql.connection.cursor()  
    cur.execute('DELETE FROM garantia WHERE idGarantia = {0}'.format(id))
    mysql.connection.commit() 
    flash('!Garantía eliminada satisfactoriamente¡')
    return redirect(url_for('modelo_garantias.insertar'))
