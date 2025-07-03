# dependencias para hacer un blue_print
from flask import Blueprint

modelo_contacto_not_cliente = Blueprint('modelo_contacto_not_cliente',
                        __name__,
                        static_folder="static",
                        url_prefix="/contactanosnotclient",
                        template_folder="templates"
                        )

from . import routes