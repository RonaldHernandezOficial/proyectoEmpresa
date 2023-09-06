#dependencia para hacer un Blueprint
from flask import Blueprint

#definir paquete 'products'
modelo_servicio = Blueprint('modelo_servicio',
                    __name__,
                    static_folder='static',
                    url_prefix='/servicio',
                    template_folder='templates')

from  . import routes