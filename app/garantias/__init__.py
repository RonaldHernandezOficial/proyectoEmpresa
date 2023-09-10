#dependencia para hacer un Blueprint
from flask import Blueprint

#definir paquete 'products'
modelo_garantias = Blueprint('modelo_garantias',
                    __name__,
                    static_folder='static',
                    url_prefix='/garantias',
                    template_folder='templates')

from . import routes