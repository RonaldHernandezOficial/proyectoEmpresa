from flask import Flask, render_template, request, redirect, url_for, flash
from . import modelo_admin
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

@modelo_admin.route("/admin")
def login():
    return render_template("admin.html")

@modelo_admin.route("/menu")
def menu():
    return render_template("indexadmin.html")

@modelo_admin.route('/insertar')
def insertar():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM garantia')
    data = cur.fetchall()
    return render_template('garantiasadmin.html' , garantias = data)

@modelo_admin.route('/editar_garantia/<id>')
def obtener_garantia(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM garantia WHERE idGarantia = %s', (id))
    dataG = cur.fetchall()
    return render_template('editar.html', garantia = dataG[0])

@modelo_admin.route('/actualizar_garantia/<id>', methods = ['POST'])
def actualizar_garantia(id):
    if request.method == 'POST':
        fechaGarantia = request.form['fechaGarantia']
        descripcionGarantia = request.form['descripcionGarantia']
        tipoGarantia = request.form['garantia']
        estadoGarantia = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE garantia 
            SET fechaGarantia = %s,
                    descripcionGarantia = %s,
                    tipoGarantia = %s,
                    estadoGarantia = %s
            WHERE idGarantia = %s
        """, (fechaGarantia, descripcionGarantia, tipoGarantia, estadoGarantia, id))
        flash('!Garantía actualizada satisfactoriamente¡')
        cur.connection.commit()
        return redirect(url_for('modelo_admin.insertar'))
    
@modelo_admin.route('/eliminar/<string:id>')
def eliminar_garantia(id):
    cur = mysql.connection.cursor()  
    cur.execute('DELETE FROM garantia WHERE idGarantia = {0}'.format(id))
    mysql.connection.commit() 
    flash('!Garantía eliminada satisfactoriamente¡')
    return redirect(url_for('modelo_admin.insertar'))
