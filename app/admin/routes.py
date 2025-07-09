from flask import render_template, request, redirect, url_for, flash
from . import modelo_admin
from app.models import Garantias, Usuario, Reseñas, Pqrs
from app import db
from app.decoradores import solo_admin
from sqlalchemy import func
from datetime import datetime, timedelta

@modelo_admin.route("/menuAdmin")
@solo_admin
def menu():
    # Fechas
    hoy = datetime.now()
    hace_una_semana = hoy - timedelta(days=7)
    hace_dos_semanas = hoy - timedelta(days=14)

    # Totales
    total_usuarios = Usuario.query.count()
    total_reseñas = Reseñas.query.count()
    total_garantias = Garantias.query.count()
    total_pqrs = Pqrs.query.count()

    # Crecimiento por semana

    # Usuarios
    usuarios_semana_actual = Usuario.query.filter(Usuario.fecha_creacion >= hace_una_semana).count()
    usuarios_semana_pasada = Usuario.query.filter(
        Usuario.fecha_creacion >= hace_dos_semanas,
        Usuario.fecha_creacion < hace_una_semana
    ).count()
    cambio_usuarios = usuarios_semana_actual - usuarios_semana_pasada
    if usuarios_semana_pasada > 0:
        crecimiento_usuarios = round((cambio_usuarios * 100 / usuarios_semana_pasada), 0)
    elif usuarios_semana_actual > 0:
        crecimiento_usuarios = 100
    else:
        crecimiento_usuarios = 0

    # Reseñas
    reseñas_semana_actual = Reseñas.query.filter(Reseñas.fecha_creacion >= hace_una_semana).count()
    reseñas_semana_pasada = Reseñas.query.filter(
        Reseñas.fecha_creacion >= hace_dos_semanas,
        Reseñas.fecha_creacion < hace_una_semana
    ).count()
    cambio_reseñas = reseñas_semana_actual - reseñas_semana_pasada
    if reseñas_semana_pasada > 0:
        crecimiento_reseñas = round((cambio_reseñas * 100 / reseñas_semana_pasada), 0)
    elif reseñas_semana_actual > 0:
        crecimiento_reseñas = 100
    else:
        crecimiento_reseñas = 0

    # Garantías
    garantias_semana_actual = Garantias.query.filter(Garantias.fecha_creacion >= hace_una_semana).count()
    garantias_semana_pasada = Garantias.query.filter(
        Garantias.fecha_creacion >= hace_dos_semanas,
        Garantias.fecha_creacion < hace_una_semana
    ).count()
    cambio_garantias = garantias_semana_actual - garantias_semana_pasada
    if garantias_semana_pasada > 0:
        crecimiento_garantias = round((cambio_garantias * 100 / garantias_semana_pasada), 0)
    elif garantias_semana_actual > 0:
        crecimiento_garantias = 100
    else:
        crecimiento_garantias = 0

    # PQRs
    pqrs_semana_actual = Pqrs.query.filter(Pqrs.fecha_creacion >= hace_una_semana).count()
    pqrs_semana_pasada = Pqrs.query.filter(
        Pqrs.fecha_creacion >= hace_dos_semanas,
        Pqrs.fecha_creacion < hace_una_semana
    ).count()
    cambio_pqrs = pqrs_semana_actual - pqrs_semana_pasada
    if pqrs_semana_pasada > 0:
        crecimiento_pqrs = round((cambio_pqrs * 100 / pqrs_semana_pasada), 0)
    elif pqrs_semana_actual > 0:
        crecimiento_pqrs = 100
    else:
        crecimiento_pqrs = 0

    # Alertas PQR
    pqr_negativas = Pqrs.query.filter(Pqrs.tipoPqrs == 'negativa').count()
    pqr_deficientes = Pqrs.query.filter(Pqrs.tipoPqrs == 'deficiente').count()

    if pqr_negativas >= 10:
        alerta_pqrs = "alta"
    elif pqr_deficientes >= 5:
        alerta_pqrs = "media"
    else:
        alerta_pqrs = "baja"

    # Porcentajes para barras de progreso
    total_global = total_usuarios + total_reseñas + total_garantias + total_pqrs
    porc_usuarios = round((total_usuarios / total_global) * 100) if total_global > 0 else 0
    porc_reseñas = round((total_reseñas / total_global) * 100) if total_global > 0 else 0
    porc_garantias = round((total_garantias / total_global) * 100) if total_global > 0 else 0
    porc_pqrs = round((total_pqrs / total_global) * 100) if total_global > 0 else 0

    return render_template(
        "indexadmin.html",
        total_usuarios=total_usuarios,
        total_reseñas=total_reseñas,
        total_garantias=total_garantias,
        total_pqrs=total_pqrs,
        cambio_usuarios=cambio_usuarios,
        cambio_reseñas=cambio_reseñas,
        cambio_garantias=cambio_garantias,
        cambio_pqrs=cambio_pqrs,
        alerta_pqrs=alerta_pqrs,
        crecimiento_usuarios=crecimiento_usuarios,
        crecimiento_reseñas=crecimiento_reseñas,
        crecimiento_garantias=crecimiento_garantias,
        crecimiento_pqrs=crecimiento_pqrs,
        porc_usuarios=porc_usuarios,
        porc_reseñas=porc_reseñas,
        porc_garantias=porc_garantias,
        porc_pqrs=porc_pqrs
    )

    


@modelo_admin.route('/insertar')
def insertar():
    garantias = Garantias.query.all()
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
    return render_template('usuariosAdmin.html', usuario=usuarios)

@modelo_admin.route('/consultarR')
def consultarR():
    reseñas = Reseñas.query.all()
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

"""@modelo_admin.route('/insertar_usuarios_prueba')
def insertar_usuarios_prueba():
    from datetime import datetime, timedelta

    hoy = datetime.now()

    # Fechas simuladas
    semana_pasada_1 = hoy - timedelta(days=10)
    semana_pasada_2 = hoy - timedelta(days=12)
    esta_semana_1 = hoy - timedelta(days=2)
    esta_semana_2 = hoy - timedelta(days=4)
    esta_semana_3 = hoy - timedelta(days=1)

    # Usuarios de la semana pasada
    usuario1 = Usuario(
        nombreUsuario="Mario",
        apellidoUsuario="Pérez",
        telefonoUsuario="1001",
        emailUsuario="mario@ej.com",
        contrasenaUsuario="123456",
        idRolFk=2,
        fecha_creacion=semana_pasada_1
    )

    usuario2 = Usuario(
        nombreUsuario="Clara",
        apellidoUsuario="López",
        telefonoUsuario="1002",
        emailUsuario="clara@ej.com",
        contrasenaUsuario="123456",
        idRolFk=2,
        fecha_creacion=semana_pasada_2
    )

     #Usuarios de esta semana
    nuevos = [
        Usuario(nombreUsuario="Luis", apellidoUsuario="Martínez", telefonoUsuario="1003", emailUsuario="luis@ej.com", contrasenaUsuario="123456", idRolFk=2, fecha_creacion=esta_semana_1),
        Usuario(nombreUsuario="Ana", apellidoUsuario="Torres", telefonoUsuario="1004", emailUsuario="ana@ej.com", contrasenaUsuario="123456", idRolFk=2, fecha_creacion=esta_semana_2),
        Usuario(nombreUsuario="Sofía", apellidoUsuario="Gómez", telefonoUsuario="1005", emailUsuario="sofia@ej.com", contrasenaUsuario="123456", idRolFk=2, fecha_creacion=esta_semana_3),
        Usuario(nombreUsuario="Pedro", apellidoUsuario="Díaz", telefonoUsuario="1006", emailUsuario="pedro@ej.com", contrasenaUsuario="123456", idRolFk=2, fecha_creacion=esta_semana_2),
        Usuario(nombreUsuario="Laura", apellidoUsuario="Mejía", telefonoUsuario="1007", emailUsuario="laura@ej.com", contrasenaUsuario="123456", idRolFk=2, fecha_creacion=esta_semana_1)
    ]

    db.session.add_all(usuario1)
    db.session.commit()

    return "Usuarios simulados insertados correctamente para prueba de crecimiento"

@modelo_admin.route('/borrar_todos_usuarios')
def borrar_todos_usuarios():
    usuarios = Usuario.query.all()
    for u in usuarios:
        db.session.delete(u)
    db.session.commit()
    return "Todos los usuarios eliminados"


@modelo_admin.route('/insertar_usuarios_antiguos')
def insertar_usuarios_antiguos():
    from datetime import datetime, timedelta
    semana_pasada = datetime.now() - timedelta(days=10)

    usuarios_antiguos = [
        Usuario(
            nombreUsuario="Juan",
            apellidoUsuario="Viejo",
            telefonoUsuario="9999",
            emailUsuario="viejo1@ej.com",
            contrasenaUsuario="123456",
            idRolFk=2,
            fecha_creacion=semana_pasada
        ),
        Usuario(
            nombreUsuario="Maria",
            apellidoUsuario="Vieja",
            telefonoUsuario="8888",
            emailUsuario="viejo2@ej.com",
            contrasenaUsuario="123456",
            idRolFk=2,
            fecha_creacion=semana_pasada
        )
    ]

    db.session.add_all(usuarios_antiguos)
    db.session.commit()

    return "Usuarios antiguos insertados"

@modelo_admin.route('/eliminar_usuarios_recientes')
def eliminar_usuarios_recientes():
    from datetime import datetime, timedelta
    hace_una_semana = datetime.now() - timedelta(days=7)

    recientes = Usuario.query.filter(Usuario.fecha_creacion >= hace_una_semana).all()
    for u in recientes:
        db.session.delete(u)

    db.session.commit()
    return "Usuarios recientes eliminados"""