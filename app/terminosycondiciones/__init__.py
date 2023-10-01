#dependencia para hacer un Blueprint
from flask import Blueprint

#definir paquete 'products'
modelo_terminos = Blueprint('modelo_terminos',
                    __name__,
                    static_folder='static',
                    url_prefix='/terminos',
                    template_folder='templates')

from  . import routes