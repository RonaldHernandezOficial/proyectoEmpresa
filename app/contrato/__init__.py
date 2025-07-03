from flask import Blueprint

modelo_contratos = Blueprint('modelo_contratos',
                    __name__,
                    static_folder='static',
                    url_prefix='/contratos',
                    template_folder='templates')

from . import routes