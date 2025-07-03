from flask import render_template
from . import modelo_contacto_not_cliente

from app.decoradores import login_requerido

@modelo_contacto_not_cliente.route("/contactanosnotclient")
def contacto():
    return render_template("contactanos_not_client.html")
