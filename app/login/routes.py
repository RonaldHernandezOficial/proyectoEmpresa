from flask import Flask, render_template, request, redirect, url_for
from . import modelo_login
import app

app = Flask(__name__)

@modelo_login.route("/login")
def login():
    return render_template("login.html")

@modelo_login.route("/nuevo_usuario")
def nuevo_usuario():
    return render_template("nuevoUsuario.html")
