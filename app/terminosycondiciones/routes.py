from flask import render_template
from . import modelo_terminos

@modelo_terminos.route("/terminos")
def terminos():
    return render_template("terminosycondiciones.html")
