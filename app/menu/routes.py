from flask import Flask, render_template, request, redirect, url_for
from . import modelo_menu
import app

#Crear una instancia Flask
app = Flask(__name__)

@modelo_menu.route("/menu")
def menu():
    return render_template("menu.html")
