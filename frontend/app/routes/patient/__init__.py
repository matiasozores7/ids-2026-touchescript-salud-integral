from flask import Blueprint

from app.constants.roles import PACIENTE
from app.utils.access_control import proteger_por_rol

patient_bp = Blueprint("patient", __name__)

patient_bp.before_request(proteger_por_rol(PACIENTE))

from app.routes.patient import home_route, turnos_route, reserva_route