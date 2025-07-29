from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_application():
    application = Flask(__name__)  # Cambiado de 'app' a 'application'
    application.config.from_object(Config)

    db.init_app(application)  # Corregido: init_app (no init_application)
    migrate.init_app(application, db)

    from .models import Rol, Usuario, Contrato, Pqrs, Garantias

    # Importa los blueprints (ajusta las rutas según tu estructura)
    from app.menu import modelo_menu
    from app.garantias import modelo_garantias
    from app.login import modelo_login
    from app.admin import modelo_admin
    from app.contactanos import modelo_contacto
    from app.serviciocliente import modelo_servicio
    from app.terminosycondiciones import modelo_terminos
    from app.contactanos_not_client import modelo_contacto_not_cliente
    from app.contrato import modelo_contratos

    # Registra los blueprints usando 'application' (no 'app')
    application.register_blueprint(modelo_menu)
    application.register_blueprint(modelo_login)
    application.register_blueprint(modelo_admin)
    application.register_blueprint(modelo_contacto)
    application.register_blueprint(modelo_servicio)
    application.register_blueprint(modelo_terminos)
    application.register_blueprint(modelo_garantias)
    application.register_blueprint(modelo_contacto_not_cliente)
    application.register_blueprint(modelo_contratos)

    return application  # Cambiado de 'app' a 'application'

# Crea la instancia que PythonAnywhere buscará
application = create_application()  # ¡Esta línea es clave!