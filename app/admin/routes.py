from flask import Flask, render_template, request, redirect, url_for
from . import modelo_admin
import app

app = Flask(__name__)

@modelo_admin.route("/admin")
def login():
    return render_template("admin.html")