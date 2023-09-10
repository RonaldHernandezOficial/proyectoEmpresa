from app import app
from app import render_template 
from flask_mysqldb import MySQL
from flask import Flask, request

if __name__ == "__main__":
    app.run(port = 3000, debug = True)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'post_sale'

mysql = MySQL(app)

@app.route('/')
def inicio():
    return render_template('menu.html')

@app.route('/agregar_garantia' , methods=['POST'])
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

@app.route('/editar_garantia')
def editar_garantia():
    return 'Garantía editada'

@app.route('/eliminar_garantia')
def eliminar_garantia():
    return 'Garantía eliminada'
