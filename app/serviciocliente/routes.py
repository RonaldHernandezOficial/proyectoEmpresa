from flask import render_template, request, redirect, url_for, flash
from . import modelo_servicio
from app.models import Reseñas, Pqrs
from app import db
from app.decoradores import login_requerido

@modelo_servicio.route('/reseña')
def reseña():
    reseñas = Reseñas.query.all()

    # CONVIERTE a listas o tuplas explícitamente:
    lista = [
        (g.nombre, g.correo, g.comentarios, g.calificacion)
        for g in reseñas
    ]
    return render_template('serviciocliente.html', reseñas=Reseñas.query.all())

@modelo_servicio.route("/insertar_reseña")
@login_requerido
def insertar_reseña():
    reseñas = Reseñas.query.all()
    return render_template("serviciocliente.html", reseñas=reseñas)

@modelo_servicio.route('/insertar_reseña', methods=['POST'])
@login_requerido
def agregar_reseña():
    if request.method == 'POST':
        nueva = Reseñas(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            comentarios=request.form['comentario'],
            calificacion=request.form['calificacion'],
            idUsuFk=None,  # Ajustar si hay sesión
            idPqrFk=None   # Ajustar si aplica
        )
        db.session.add(nueva)
        db.session.commit()
        flash("¡RESEÑA registrada exitosamente!")

        if nueva.calificacion in ["deficiente", "pesimo"]:
            return render_template('registrarpqr.html')

    return redirect(url_for('modelo_servicio.insertar_reseña'))

@modelo_servicio.route('/eliminar_reseña/<int:id>')
@login_requerido
def eliminar_reseña(id):
    reseña = Reseñas.query.get_or_404(id)
    db.session.delete(reseña)
    db.session.commit()
    flash('Reseña eliminada satisfactoriamente')
    return redirect(url_for('modelo_servicio.insertar_reseña'))


#_____________________________________________________ pqrs

@modelo_servicio.route('/pqrs')
@login_requerido
def pqrs():
    pqrs = Pqrs.query.all()
    # CONVIERTE a listas o tuplas explícitamente:
    lista = [
        (g.tipoPqrs, g.descripcionPqrs, g.idGarantiaFk, g.idContratoFk)
        for g in pqrs
    ]
    return render_template('registrarpqr.html', pqrs=Pqrs.query.all())

@modelo_servicio.route('/insertar_pqrs')
@login_requerido
def insertar_pqrs():
    pqrs = Pqrs.query.all()
    return render_template('registrarpqr.html', pqrs=pqrs)

@modelo_servicio.route('/insertar_pqrs', methods=['POST'])
@login_requerido
def agregar_pqrs():
    if request.method == 'POST':
        nuevo = Pqrs(
            tipoPqrs=request.form['tipoPqrs'],
            descripcionPqrs=request.form['descripcionPqrs'],
            estadopqrs='Pendiente',
            idGarantiaFk=request.form.get('idGarantiaFk') or None,
            idContratoFk=request.form.get('idContratoFk') or None
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("¡PQR'S registrado exitosamente!")
    return redirect(url_for('modelo_servicio.insertar_pqrs'))

@modelo_servicio.route('/eliminar_servicio/<int:id>')
@login_requerido
def eliminar_pqrs(id):
    pqrs = Pqrs.query.get_or_404(id)
    db.session.delete(pqrs)
    db.session.commit()
    flash('Pqrs eliminado satisfactoriamente')
    return redirect(url_for('modelo_servicio.insertar_pqrs'))

@modelo_servicio.route('/editar_servicio/<int:id>')
@login_requerido
def obtener_pqrs(id):
    pqrs = Pqrs.query.get_or_404(id)
    return render_template('editarpqr.html', pqrs=pqrs)

@modelo_servicio.route('/actualizar_servicio/<int:id>', methods=['POST'])
@login_requerido
def actualizar_pqrs(id):
    pqrs = Pqrs.query.get_or_404(id)
    pqrs.tipoPqrs = request.form['tipoPqrs']
    pqrs.descripcionPqrs = request.form['descripcionPqrs']
    db.session.commit()
    flash('Pqrs actualizado satisfactoriamente')
    return redirect(url_for('modelo_servicio.insertar_pqrs'))
