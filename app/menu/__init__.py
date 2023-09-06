#dependencia para hacer un Blueprint
from flask import Blueprint

#definir paquete 'products'
modelo_menu = Blueprint('modelo_menu',
                    __name__,
                    static_folder='static',
                    url_prefix='/menu',
                    template_folder='templates')

from  . import routes