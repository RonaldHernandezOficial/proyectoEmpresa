from flask import Flask, render_template
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.menu import modelo_menu
from app.login import modelo_login
from app.admin import modelo_admin
from app.contactanos import modelo_contacto
from app.serviciocliente import modelo_servicio

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app=app , db=db)

from .models import Rol, Usuario, Contrato, Pqrs, Garantias

app.register_blueprint(modelo_menu)
app.register_blueprint(modelo_login)
app.register_blueprint(modelo_admin)
app.register_blueprint(modelo_contacto)
app.register_blueprint(modelo_servicio)

if __name__ == '__main__':
    app.run(port=3000, debug=True)