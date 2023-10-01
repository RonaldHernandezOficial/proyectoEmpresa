from flask import Flask, render_template, request, redirect, url_for
from . import modelo_terminos
import app

#Crear una instancia Flask
app = Flask(__name__)

@modelo_terminos.route("/terminos")
def menu():
    return render_template("terminosycondiciones.html")