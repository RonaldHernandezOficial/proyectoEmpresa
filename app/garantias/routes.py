from flask import render_template, request, redirect, url_for, flash
from . import modelo_garantias
from app.models import Garantias
from app import db
from app.decoradores import login_requerido

@modelo_garantias.route('/garantia')
def garantia():
    return render_template('garantias.html')

@modelo_garantias.route('/insertar_garantia')
def insertar():
    garantias = Garantias.query.all()
    return render_template('insertar_garantias.html', garantias=garantias)

@modelo_garantias.route('/agregar_garantia', methods=['POST'])
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

@modelo_garantias.route('/editar_garantia/<int:id>')
def obtener_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    return render_template('editar_garantias.html', garantia=garantia)

@modelo_garantias.route('/actualizar_garantia/<int:id>', methods=['POST'])
def actualizar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    garantia.fechaGarantia = request.form['fechaGarantia']
    garantia.descripcionGarantia = request.form['descripcionGarantia']
    garantia.tipoGarantia = request.form['garantia']
    db.session.commit()
    flash('¡Garantía actualizada satisfactoriamente!')
    return redirect(url_for('modelo_garantias.insertar'))

@modelo_garantias.route('/eliminar_garantia/<int:id>')
def eliminar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    db.session.delete(garantia)
    db.session.commit()
    flash('¡Garantía eliminada satisfactoriamente!')
    return redirect(url_for('modelo_garantias.insertar'))
