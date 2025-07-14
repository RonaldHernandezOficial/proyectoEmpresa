from flask import render_template, request, redirect, url_for, flash
from . import modelo_garantias
from app.models import Garantias
from app import db
from app.decoradores import login_requerido

@modelo_garantias.route('/garantia')
def garantia():
    garantias = Garantias.query.all()

    # CONVIERTE a listas o tuplas explícitamente:
    lista = [
        (g.id, g.fechaGarantia, g.descripcionGarantia, g.tipoGarantia, g.estadoGarantia)
        for g in garantias
    ]
    return render_template('garantias.html', garantias=Garantias.query.all())

@modelo_garantias.route('/insertar_garantia')
@login_requerido
def insertar():
    garantias = Garantias.query.all()
    return render_template('insertar_garantias.html', garantias=garantias)

@modelo_garantias.route('/agregar_garantia', methods=['POST'])
@login_requerido
def agregar_garantia():
    if request.method == 'POST':
        nueva = Garantias(
            fechaGarantia=request.form['fechaGarantia'],
            descripcionGarantia=request.form['descripcionGarantia'],
            tipoGarantia=request.form['garantia'],
            estadoGarantia='Pendiente',  
            idUsuFk=None 
        )
        db.session.add(nueva)
        db.session.commit()
        flash('¡Garantía agregada satisfactoriamente!')
    return redirect(url_for('modelo_garantias.insertar'))

# Mostrar el formulario de edición (GET)
@modelo_garantias.route('/editar_garantia/<int:id>', methods=['GET'])
@login_requerido
def obtener_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    return render_template('editar_garantias.html', garantia=garantia)

# Procesar el formulario de edición (POST)
@modelo_garantias.route('/actualizar_garantia/<int:id>', methods=['POST'])
@login_requerido
def actualizar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    garantia.fechaGarantia = request.form['fechaGarantia']
    garantia.descripcionGarantia = request.form['descripcionGarantia']
    garantia.tipoGarantia = request.form['garantia']
    db.session.commit()
    flash('¡Garantía actualizada satisfactoriamente!')
    return redirect(url_for('modelo_garantias.insertar'))

@modelo_garantias.route('/eliminar_garantia/<int:id>')
@login_requerido
def eliminar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    db.session.delete(garantia)
    db.session.commit()
    flash('¡Garantía eliminada satisfactoriamente!')
    return redirect(url_for('modelo_garantias.insertar'))
