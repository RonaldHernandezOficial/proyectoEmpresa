from flask import render_template, request, redirect, url_for, session, flash
from . import modelo_login
from app.models import Usuario
from app import db
from functools import wraps

@modelo_login.route("/olvidar_contraseña")
def nuevo_usuario():
    return render_template("olvidarcon.html")

@modelo_login.route("/login")
def login():
    return render_template("login.html")

@modelo_login.route('/insertar', methods=['POST'])
def agregar_usuario():
    if request.method == 'POST':
        nuevo = Usuario(
            nombreUsuario=request.form['nombre'],
            apellidoUsuario=request.form['apellido'],
            emailUsuario=request.form['email'],
            telefonoUsuario=request.form['telefono'],
            contrasenaUsuario=request.form['contrasena'],
            idRolFk=2
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("¡Usuario registrado correctamente!")
    return render_template('login.html')

@modelo_login.route('/ingresar', methods=['POST'])
def ingresar():
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    usuario = Usuario.query.filter_by(emailUsuario=correo, contrasenaUsuario=contrasena).first()

    if usuario:
        session['logueado'] = True
        session['idUsu'] = usuario.idUsu
        session['idRolFk'] = usuario.idRolFk
        session['nombreUsuario'] = usuario.nombreUsuario

        if usuario.idRolFk == 1:
            return redirect("/admin/menuAdmin")
        else:
            return redirect("/menu/menuClientes")
    else:
        return render_template('login.html', mensaje="Usuario o contraseña incorrecta")

@modelo_login.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente.")
    return redirect(url_for('modelo_login.login'))

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página.')
            return redirect(url_for('login.login'))  # Asegúrate que 'login.login' coincide con tu nombre de blueprint y ruta
        return f(*args, **kwargs)
    return decorated_function
