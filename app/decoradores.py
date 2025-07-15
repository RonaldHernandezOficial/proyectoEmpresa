from functools import wraps
from flask import session, redirect, url_for, flash

def login_requerido(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if 'logueado' not in session:
            flash("Debes iniciar sesión para acceder a esta página.")
            return redirect(url_for('modelo_login.login'))
        return f(*args, **kwargs)
    return decorada


def solo_admin(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        # Si no está logueado o no es admin, se saca inmediatamente
        if not session.get('logueado') or session.get('idRolFk') != 1:
            session.clear()  # 🔥 Limpia por seguridad si algo raro queda en sesión
            flash("Acceso restringido. Inicia sesión como administrador.")
            return redirect(url_for('modelo_login.login'))
        return f(*args, **kwargs)
    return decorada

def solo_clientes(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get('logueado'):
            flash("Debes iniciar sesión primero.")
            return redirect(url_for('modelo_login.login'))
        if session.get('idRolFk') != 2:  # Solo clientes
            flash("Acceso restringido solo para clientes.")
            return redirect(url_for('modelo_login.login'))
        return f(*args, **kwargs)
    return decorada