from flask import Flask, render_template
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app=app , db=db)

from .models import Rol, Usuario, Contrato, Pqrs, Garantias

if __name__ == '__main__':
    app.run(port=3000, debug=True)