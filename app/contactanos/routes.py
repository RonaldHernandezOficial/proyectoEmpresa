from flask import render_template
from . import modelo_contacto

from app.decoradores import login_requerido

@modelo_contacto.route("/contactanos")
@login_requerido
def contacto():
    return render_template("contactanos.html")
