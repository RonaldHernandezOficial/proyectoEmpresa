from flask import Flask, render_template, request, redirect, url_for
from . import modelo_servicio
import app

#Crear una instancia Flask
app = Flask(__name__)

@modelo_servicio.route("/reseñas")
def reseña():
    return render_template("serviciocliente.html")

@modelo_servicio.route("/pqr")
def pqr():
    return render_template("registrarpqr.html")
