from flask import render_template, session, redirect, url_for, flash, make_response
from . import modelo_menu
from app.decoradores import solo_clientes

@modelo_menu.route("/")
def menu():
    return render_template("menu.html")

 
@modelo_menu.route("/menuClientes")
@solo_clientes
def menuC():
    # ✅ Validación de sesión
    if "idUsu" not in session: 
        flash("Debe iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for("modelo_login.login"))  # Ajusta el nombre de tu blueprint y ruta de login

    response = make_response(render_template("menuClientes.html"))
    # ✅ Evitar que se pueda volver con el botón "Atrás" después de cerrar sesión
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@modelo_menu.route("/nuestrosTrabajos")
def menuT():
    return render_template("nuestrosTrabajos.html")