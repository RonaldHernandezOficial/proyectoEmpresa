from flask import render_template
from . import modelo_contacto

@modelo_contacto.route("/contactanos")
def contacto():
    return render_template("contactanos.html")
