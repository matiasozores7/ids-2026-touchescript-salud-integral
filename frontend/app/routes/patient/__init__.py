from flask import Blueprint

from app.constants.roles import Roles
from app.utils.access_control import proteger_por_rol

patient_bp = Blueprint("patient", __name__)

patient_bp.before_request(proteger_por_rol(Roles.PACIENTE))

from app.routes.patient import home_route, turnos_route, reserva_route,especialidades_route,profesionales_route