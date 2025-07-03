from flask import render_template, request, redirect, url_for, flash
from . import modelo_contratos
from app.models import Contrato
from app import db
from app.decoradores import login_requerido

@modelo_contratos.route('/contrato')
def contrato():
    contratos = Contrato.query.all()
    lista = [
        (c.idContrato, c.tipoContrato, c.descripcionContrato, c.idGarantiaFk, c.idUsuFk)
        for c in contratos
    ]
    return render_template('contratos.html', contratos=contratos)

@modelo_contratos.route('/insertar_contrato')
@login_requerido  
def insertar_contrato():
    contratos = Contrato.query.all()
    return render_template('contratos.html', contratos=contratos)

@modelo_contratos.route('/agregar_contrato', methods=['POST'])
@login_requerido
def agregar_contrato():
    if request.method == 'POST':
        nuevo_contrato = Contrato(
            tipoContrato=request.form['tipoContrato'],
            descripcionContrato=request.form['descripcionContrato'],
            idGarantiaFk=request.form['idGarantiaFk'],
            idUsuFk=request.form['idUsuFk']
        )
        db.session.add(nuevo_contrato)
        db.session.commit()
        flash('¡Contrato agregado satisfactoriamente!')
    return redirect(url_for('modelo_contratos.insertar_contrato'))

@modelo_contratos.route('/editar_contrato/<string:id>')
@login_requerido
def obtener_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    return render_template('editar_contratos.html', contrato=contrato)

@modelo_contratos.route('/actualizar_contrato/<string:id>', methods=['POST'])
@login_requerido
def actualizar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    contrato.tipoContrato = request.form['tipoContrato']
    contrato.descripcionContrato = request.form['descripcionContrato']
    contrato.idGarantiaFk = request.form['idGarantiaFk']
    contrato.idUsuFk = request.form['idUsuFk']
    db.session.commit()
    flash('¡Contrato actualizado satisfactoriamente!')
    return redirect(url_for('modelo_contratos.insertar_contrato'))

@modelo_contratos.route('/eliminar_contrato/<string:id>')
@login_requerido
def eliminar_contrato(id):
    contrato = Contrato.query.get_or_404(id)
    db.session.delete(contrato)
    db.session.commit()
    flash('¡Contrato eliminado satisfactoriamente!')
    return redirect(url_for('modelo_contratos.insertar_contrato'))
