# dependencias para hacer un blue_print
from flask import Blueprint

modelo_contacto = Blueprint('modelo_contacto',
                        __name__,
                        static_folder="static",
                        url_prefix="/contactanos",
                        template_folder="templates"
                        )

from . import routes