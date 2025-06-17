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
        if session.get('idRolFk') != 1:
            flash("Acceso restringido solo para administradores.")
            return redirect(url_for('modelo_menu.menu'))
        return f(*args, **kwargs)
    return decorada
