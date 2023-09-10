from flask import Flask, render_template, request, redirect, url_for
from . import modelo_garantias
import app

#Crear una instancia Flask
app = Flask(__name__)
        
@modelo_garantias.route("/garantias")
def garantias():
    return render_template("garantias.html")

@modelo_garantias.route("/insertar_garantias")
def insertar_garantias():
    return render_template("insertar_garantias.html")