from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models import Rol, Usuario, Contrato, Pqrs, Garantias

    from app.menu import modelo_menu
    from app.garantias import modelo_garantias
    from app.login import modelo_login
    from app.admin import modelo_admin
    from app.contactanos import modelo_contacto
    from app.serviciocliente import modelo_servicio
    from app.terminosycondiciones import modelo_terminos

    app.register_blueprint(modelo_menu)
    app.register_blueprint(modelo_login)
    app.register_blueprint(modelo_admin)
    app.register_blueprint(modelo_contacto)
    app.register_blueprint(modelo_servicio)
    app.register_blueprint(modelo_terminos)

    return app
