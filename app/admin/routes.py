from flask import render_template, request, redirect, url_for, flash, session
from . import modelo_admin
from app.models import Garantias, Usuario, Reseñas, Pqrs
from app import db
from app.decoradores import solo_admin
from sqlalchemy import func
from datetime import datetime, timedelta
import csv, io
from flask import make_response, request, render_template
import pandas as pd
import io

@modelo_admin.route('/perfilAdmin')
@solo_admin
def perfil_admin():
    usuario = Usuario.query.first()
    return render_template('admin.html', usuario=usuario)


@modelo_admin.route("/menuAdmin")
@solo_admin
def menu():
    if "idUsu" not in session:
        flash("Debe iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for("modelo_login.login"))  # Ajusta al nombre de tu login

    # Filtro por fechas (rango personalizado o últimos 14 días por defecto)
    fecha_inicio_str = request.args.get("fecha_inicio")
    fecha_fin_str = request.args.get("fecha_fin")

    hoy = datetime.now()
    if fecha_inicio_str and fecha_fin_str:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d") + timedelta(days=1)
        except ValueError:
            fecha_inicio = hoy - timedelta(days=14)
            fecha_fin = hoy
    else:
        fecha_inicio = hoy - timedelta(days=14)
        fecha_fin = hoy

    # Ajuste: semanas relativas al filtro
    hace_una_semana = fecha_fin - timedelta(days=7)
    hace_dos_semanas = fecha_fin - timedelta(days=14)

    # Totales filtrados por rango
    total_usuarios = Usuario.query.filter(Usuario.fecha_creacion >= fecha_inicio, Usuario.fecha_creacion < fecha_fin).count()
    total_reseñas = Reseñas.query.filter(Reseñas.fecha_creacion >= fecha_inicio, Reseñas.fecha_creacion < fecha_fin).count()
    total_garantias = Garantias.query.filter(Garantias.fecha_creacion >= fecha_inicio, Garantias.fecha_creacion < fecha_fin).count()
    total_pqrs = Pqrs.query.filter(Pqrs.fecha_creacion >= fecha_inicio, Pqrs.fecha_creacion < fecha_fin).count()

    # Función para calcular el crecimiento
    def calcular_crecimiento(actual, pasada):
        if pasada > 0:
            return round((actual - pasada) * 100 / pasada, 0)
        elif actual > 0:
            return 100
        else:
            return 0

    # Crecimiento basado en semanas relativas al filtro
    usuarios_semana_actual = Usuario.query.filter(Usuario.fecha_creacion >= hace_una_semana, Usuario.fecha_creacion < fecha_fin).count()
    usuarios_semana_pasada = Usuario.query.filter(Usuario.fecha_creacion >= hace_dos_semanas, Usuario.fecha_creacion < hace_una_semana).count()
    crecimiento_usuarios = calcular_crecimiento(usuarios_semana_actual, usuarios_semana_pasada)
    cambio_usuarios = usuarios_semana_actual - usuarios_semana_pasada

    reseñas_semana_actual = Reseñas.query.filter(Reseñas.fecha_creacion >= hace_una_semana, Reseñas.fecha_creacion < fecha_fin).count()
    reseñas_semana_pasada = Reseñas.query.filter(Reseñas.fecha_creacion >= hace_dos_semanas, Reseñas.fecha_creacion < hace_una_semana).count()
    crecimiento_reseñas = calcular_crecimiento(reseñas_semana_actual, reseñas_semana_pasada)
    cambio_reseñas = reseñas_semana_actual - reseñas_semana_pasada

    garantias_semana_actual = Garantias.query.filter(Garantias.fecha_creacion >= hace_una_semana, Garantias.fecha_creacion < fecha_fin).count()
    garantias_semana_pasada = Garantias.query.filter(Garantias.fecha_creacion >= hace_dos_semanas, Garantias.fecha_creacion < hace_una_semana).count()
    crecimiento_garantias = calcular_crecimiento(garantias_semana_actual, garantias_semana_pasada)
    cambio_garantias = garantias_semana_actual - garantias_semana_pasada

    pqrs_semana_actual = Pqrs.query.filter(Pqrs.fecha_creacion >= hace_una_semana, Pqrs.fecha_creacion < fecha_fin).count()
    pqrs_semana_pasada = Pqrs.query.filter(Pqrs.fecha_creacion >= hace_dos_semanas, Pqrs.fecha_creacion < hace_una_semana).count()
    crecimiento_pqrs = calcular_crecimiento(pqrs_semana_actual, pqrs_semana_pasada)
    cambio_pqrs = pqrs_semana_actual - pqrs_semana_pasada

    # Alertas PQRs basadas en semana relativa al filtro
    pqr_negativas = Pqrs.query.filter(Pqrs.tipoPqrs.in_(['Queja', 'Reclamo']), Pqrs.fecha_creacion >= hace_una_semana, Pqrs.fecha_creacion < fecha_fin).count()
    pqr_deficientes = Pqrs.query.filter(Pqrs.tipoPqrs == 'Sugerencia', Pqrs.fecha_creacion >= hace_una_semana, Pqrs.fecha_creacion < fecha_fin).count()
    pqr_peticion = Pqrs.query.filter(Pqrs.tipoPqrs == 'Peticion', Pqrs.fecha_creacion >= hace_una_semana, Pqrs.fecha_creacion < fecha_fin).count()

    if pqr_negativas >= 10:
        alerta_pqrs = "alta"
    elif pqr_deficientes >= 5:
        alerta_pqrs = "media"
    elif pqr_peticion >= 10:
        alerta_pqrs = "peticiones"
    else:
        alerta_pqrs = "baja"

    total_global = total_usuarios + total_reseñas + total_garantias + total_pqrs
    porc_usuarios = round((total_usuarios / total_global) * 100) if total_global > 0 else 0
    porc_reseñas = round((total_reseñas / total_global) * 100) if total_global > 0 else 0
    porc_garantias = round((total_garantias / total_global) * 100) if total_global > 0 else 0
    porc_pqrs = round((total_pqrs / total_global) * 100) if total_global > 0 else 0

    # Datos por día para gráficas
    fechas = [fecha_inicio + timedelta(days=i) for i in range((fecha_fin - fecha_inicio).days)]
    labels = [f.strftime('%d-%b') for f in fechas]
    usuarios_dia = [Usuario.query.filter(func.date(Usuario.fecha_creacion) == f.date()).count() for f in fechas]
    reseñas_dia = [Reseñas.query.filter(func.date(Reseñas.fecha_creacion) == f.date()).count() for f in fechas]
    garantias_dia = [Garantias.query.filter(func.date(Garantias.fecha_creacion) == f.date()).count() for f in fechas]
    pqrs_dia = [Pqrs.query.filter(func.date(Pqrs.fecha_creacion) == f.date()).count() for f in fechas]

    response = make_response(render_template(
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
        porc_pqrs=porc_pqrs,
        labels=labels,
        usuarios_dia=usuarios_dia,
        reseñas_dia=reseñas_dia,
        garantias_dia=garantias_dia,
        pqrs_dia=pqrs_dia,
        fecha_inicio=fecha_inicio.strftime('%Y-%m-%d'),
        fecha_fin=(fecha_fin - timedelta(days=1)).strftime('%Y-%m-%d')
    ))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@modelo_admin.route("/exportar_csv")
@solo_admin
def exportar_csv():
    tabla = request.args.get("tabla", "").lower()
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    try:
        inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d") if fecha_inicio else None
        fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d") + timedelta(days=1, seconds=-1) if fecha_fin else None
    except ValueError:
        return "Formato de fecha inválido.", 400

    if tabla == "usuarios":
        query = Usuario.query
        if inicio_dt and fin_dt:
            query = query.filter(Usuario.fecha_creacion.between(inicio_dt, fin_dt))
        resultados = query.all()
        if not resultados:
            return "No hay usuarios para exportar.", 404

        data = [{
            "ID": str(u.idUsu),
            "Nombre": u.nombreUsuario,
            "Apellido": u.apellidoUsuario,
            "Correo": u.emailUsuario,
            "Teléfono": u.telefonoUsuario,
            "Fecha Registro": u.fecha_creacion
        } for u in resultados]

    elif tabla == "resenas":
        query = Reseñas.query
        if inicio_dt and fin_dt:
            query = query.filter(Reseñas.fecha_creacion.between(inicio_dt, fin_dt))
        resultados = query.all()
        if not resultados:
            return "No hay reseñas para exportar.", 404

        data = [{
            "ID": str(r.idReseña),
            "Nombre Usuario": r.nombre,
            "Correo": r.correo,
            "Comentario": r.comentarios,
            "Calificación": r.calificacion,
            "Fecha Registro": r.fecha_creacion
        } for r in resultados]

    elif tabla == "garantias":
        query = Garantias.query
        if inicio_dt and fin_dt:
            query = query.filter(Garantias.fecha_creacion.between(inicio_dt, fin_dt))
        resultados = query.all()
        if not resultados:
            return "No hay garantías para exportar.", 404

        data = [{
            "ID": str(g.idGarantia),
            "Tipo": g.tipoGarantia,
            "Descripción": g.descripcionGarantia,
            "Estado": g.estadoGarantia,
            "Fecha Registro": g.fecha_creacion
        } for g in resultados]

    elif tabla == "pqrs":
        query = Pqrs.query
        if inicio_dt and fin_dt:
            query = query.filter(Pqrs.fecha_creacion.between(inicio_dt, fin_dt))
        resultados = query.all()
        if not resultados:
            return "No hay datos de PQRs para exportar.", 404

        data = [{
            "ID": str(p.idPqrs),
            "Tipo": p.tipoPqrs,
            "Descripción": p.descripcionPqrs,
            "Fecha Registro": p.fecha_creacion
        } for p in resultados]

    else:
        return "Entidad no válida para exportar.", 400

    # Convertir a DataFrame y parsear fecha
    df = pd.DataFrame(data)
    if "Fecha Registro" in df.columns:
        df['Fecha Registro'] = pd.to_datetime(df['Fecha Registro'], errors='coerce')

    # Exportar a Excel con estilos
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
        workbook = writer.book
        worksheet = writer.sheets['Datos']

        # Formatos
        formato_header = workbook.add_format({'bold': True, 'bg_color': '#DDEBF7'})
        formato_fecha_reciente = workbook.add_format({'bg_color': '#C6EFCE', 'num_format': 'yyyy-mm-dd hh:mm:ss'})
        formato_fecha_antigua = workbook.add_format({'bg_color': '#D9D9D9', 'num_format': 'yyyy-mm-dd hh:mm:ss'})

        # Escribir encabezado
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, formato_header)

        # Escribir datos con estilos
        for row_num, row_data in enumerate(df.itertuples(index=False), start=1):
            # Detectar formato base por fila
            bg_color = '#E2EFDA'  # color por defecto

            if tabla == "pqrs":
                tipo = getattr(row_data, 'Tipo', '').strip().lower()
                if tipo in ['queja', 'reclamo']:
                    bg_color = '#F8CBAD'
                elif tipo == 'sugerencia':
                    bg_color = '#FFE699'
                elif tipo == 'peticion':
                    bg_color = '#BDD7EE'

            elif tabla == "resenas":
                calificacion = getattr(row_data, 'Calificación', '').strip().lower()
                colores = {
                    'pesimo': '#FF4C4C',      # rojo fuerte
                    'deficiente': '#FFA500',  # naranja
                    'aceptable': '#FFFF99',   # amarillo claro
                    'buena': '#90EE90',       # verde claro
                    'excelente': '#32CD32'    # verde oscuro
                }
                bg_color = colores.get(calificacion, '#FFFFFF')
            elif tabla == "garantias":
                estado = getattr(row_data, 'Estado', '').strip().lower()
                bg_color = '#E2EFDA' if estado == 'aprobada' else '#F8CBAD'

            elif tabla == "usuarios":
                fecha_registro = getattr(row_data, 'Fecha_Registro', None) or getattr(row_data, 'Fecha Registro', None)
                dias = (datetime.now() - fecha_registro).days if fecha_registro else 0
                formato_fila = formato_fecha_reciente if dias <= 7 else formato_fecha_antigua
            else:
                bg_color = '#E2EFDA'

            # Crear formato para la fila (excepto usuarios que ya tienen uno listo)
            if tabla != "usuarios":
                formato_fila = workbook.add_format({'bg_color': bg_color})
                formato_fecha_coloreada = workbook.add_format({
                    'bg_color': bg_color,
                    'num_format': 'yyyy-mm-dd hh:mm:ss'
                })

            for col_num, valor in enumerate(row_data):
                col_name = df.columns[col_num]
                if isinstance(valor, pd.Timestamp) and "fecha" in col_name.lower():
                    worksheet.write_datetime(row_num, col_num, valor, formato_fila if tabla == "usuarios" else formato_fecha_coloreada)
                else:
                    worksheet.write(row_num, col_num, valor, formato_fila)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={tabla}_filtradas.xlsx"
    response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    return response

@modelo_admin.route('/insertar')
@solo_admin
def insertar():
    garantias = Garantias.query.all()
    return render_template('garantiasadmin.html', garantias=garantias)

@modelo_admin.route('/editar_garantia/<int:id>')
@solo_admin
def obtener_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    return render_template('editar.html', garantia=garantia)

@modelo_admin.route('/actualizar_garantia/<int:id>', methods=['POST'])
@solo_admin
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
@solo_admin
def eliminar_garantia(id):
    garantia = Garantias.query.get_or_404(id)
    db.session.delete(garantia)
    db.session.commit()
    flash('¡Garantía eliminada satisfactoriamente!')
    return redirect(url_for('modelo_admin.insertar'))

@modelo_admin.route('/consultar')
@solo_admin
def consultar():
    usuarios = Usuario.query.all()
    return render_template('usuariosAdmin.html', usuario=usuarios)

@modelo_admin.route('/consultarR')
@solo_admin
def consultarR():
    reseñas = Reseñas.query.all()
    return render_template('reseñasAdmin.html', reseñas=reseñas)

@modelo_admin.route('/consultarP')
@solo_admin
def consultarP():
    pqrs = Pqrs.query.all()
    return render_template('responderPqr.html', pqrs=pqrs)

@modelo_admin.route('/editar_pqrs/<int:id>')
@solo_admin
def obtener_pqrs(id):
    pqrs = Pqrs.query.get_or_404(id)
    return render_template('respuesta.html', pqrs=pqrs)

@modelo_admin.route('/actualizar_pqrs/<int:id>', methods=['POST'])
@solo_admin
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