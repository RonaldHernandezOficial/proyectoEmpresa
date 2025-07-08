from flask import render_template, request, redirect, url_for, flash
from . import modelo_admin
from app.models import Garantias, Usuario, Reseñas, Pqrs
from app import db
from app.decoradores import solo_admin


@modelo_admin.route("/admin")
def login():
    return redirect("admin.html")

@modelo_admin.route("/menuAdmin")
def menu():
    return render_template("indexadmin.html")


@modelo_admin.route("/menuAdmin")
@solo_admin
def menu_admin(): 
     return render_template("indexadmin.html")

 
@modelo_admin.route('/insertar')
def insertar():
    garantias = Garantias.query.all()
    # CONVIERTE a listas o tuplas explícitamente:
    lista = [
        (g.fechaGarantia, g.descripcionGarantia, g.tipoGarantia, g.estadoGarantia)
        for g in garantias
    ]
    return render_template('garantiasadmin.html', garantias=garantias)

@modelo_admin.route('/editar_garantia/<int:id>')
def obtener_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    return render_template('editar.html', garantia=garantia)

@modelo_admin.route('/actualizar_garantia/<int:id>', methods=['POST'])
def actualizar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    if request.method == 'POST':
        garantia.fechaGarantia = request.form['fechaGarantia']
        garantia.descripcionGarantia = request.form['descripcionGarantia']
        garantia.tipoGarantia = request.form['garantia']
        garantia.estadoGarantia = request.form['estado']
        db.session.commit()
        flash('¡Garantía actualizada satisfactoriamente!')
        return redirect(url_for('modelo_admin.insertar'))

@modelo_admin.route('/eliminar/<int:id>')
def eliminar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    db.session.delete(garantia)
    db.session.commit()
    flash('¡Garantía eliminada satisfactoriamente!')
    return redirect(url_for('modelo_admin.insertar'))

@modelo_admin.route('/consultar')
def consultar():
    usuarios = Usuario.query.all()
    # CONVIERTE a listas o tuplas explícitamente:
    lista = [
        (g.nombreUsuario, g.apellidoUsuario, g.telefonoUsuario, g.emailUsuario, g.rol.tipoRol)
        for g in usuarios
    ]
    return render_template('usuariosAdmin.html', usuario=usuarios)

@modelo_admin.route('/consultarR')
def consultarR():
    reseñas = Reseñas.query.all()
    # CONVIERTE a listas o tuplas explícitamente:
    lista = [
        (g.nombre, g.correo, g.comentarios, g.calificacion)
        for g in reseñas
    ]
    return render_template('reseñasAdmin.html', reseñas=reseñas)

@modelo_admin.route('/consultarP')
def consultarP():
    pqrs = Pqrs.query.all()
    return render_template('responderPqr.html', pqrs=pqrs)

@modelo_admin.route('/editar_pqrs/<int:id>')
def obtener_pqrs(id):
    pqrs = Pqrs.query.get_or_404(id)
    return render_template('respuesta.html', pqrs=pqrs)

@modelo_admin.route('/actualizar_pqrs/<int:id>', methods=['POST'])
def responderPqrs(id):
    pqrs = Pqrs.query.get_or_404(id)
    if request.method == 'POST':
        pqrs.tipoPqrs = request.form['estado']
        pqrs.descripcionPqrs = request.form['descripcionPqrs']
        db.session.commit()
        flash('¡Pqrs respondido satisfactoriamente!')
        return redirect(url_for('modelo_admin.consultarP'))
