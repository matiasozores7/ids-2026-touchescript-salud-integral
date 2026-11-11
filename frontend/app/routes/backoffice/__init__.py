from flask import Blueprint

from app.constants.roles import ADMIN
from app.utils.access_control import proteger_por_rol

backoffice_bp = Blueprint("backoffice", __name__)

backoffice_bp.before_request(proteger_por_rol(ADMIN))

from . import dashboard_route
from . import especialidades_route
from . import medicos_route
from . import consultorios_route
from . import checkin_route
from . import pacientes_route