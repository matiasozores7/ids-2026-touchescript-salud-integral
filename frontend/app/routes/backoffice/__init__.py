from flask import Blueprint

from app.constants.roles import Roles
from app.utils.access_control import proteger_por_rol

backoffice_bp = Blueprint("backoffice", __name__)

backoffice_bp.before_request(proteger_por_rol(Roles.ADMIN))

from . import dashboard_route
from . import especialidades_route
from . import medicos_route
from . import consultorios_route
from . import checkin_route
from . import pacientes_route
from . import coberturas_route
from . import turnos_route
from . import calendario_route
from . import agendas_route
from . import reportes_route
from . import sala_espera_route
