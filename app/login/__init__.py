# dependencias para hacer un blue_print
from flask import Blueprint

modelo_login = Blueprint('modelo_login',
                        __name__,
                        static_folder="static",
                        url_prefix="/login",
                        template_folder="templates"
                        )

from . import routes