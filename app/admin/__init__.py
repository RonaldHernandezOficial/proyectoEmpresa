# dependencias para hacer un blue_print
from flask import Blueprint

modelo_admin = Blueprint('modelo_admin',
                        __name__,
                        static_folder="static",
                        url_prefix="/admin",
                        template_folder="templates"
                        )

from . import routes