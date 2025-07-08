from flask import render_template
from . import modelo_menu

@modelo_menu.route("/")
def menu():
    return render_template("menu.html")

@modelo_menu.route("/menuClientes")
def menuC():
    return render_template("menuClientes.html")

@modelo_menu.route("/nuestrosTrabajos")
def menuT():
    return render_template("nuestrosTrabajos.html")