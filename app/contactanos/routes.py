from flask import Flask, render_template, request, redirect, url_for
from . import modelo_contacto
import app

app = Flask(__name__)

@modelo_contacto.route("/contactanos")
def login():
    return render_template("contactanos.html")