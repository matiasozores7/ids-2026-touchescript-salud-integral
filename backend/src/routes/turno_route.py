from flask import Blueprint, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request

from src.errors.exceptions import BadRequestError
from src.services import turno_service
from src.utils.responses import success_response
from src.validators import turno_validator

turnos_bp = Blueprint("turnos", __name__)


def _obtener_claims_actuales() -> dict:
    try:
        verify_jwt_in_request(optional=True)
        return get_jwt() or {}
    except Exception:
        return {}


# -----------------------------------------------------------------------------
# Tarea 3: PUT /turnos/<id>/estado
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/<int(min=1):turno_id>/estado", methods=["PUT", "PATCH"])
def actualizar_estado_turno(turno_id: int):
    data = request.get_json(silent=True) or {}
    turno_validator.validar_actualizacion_estado(data)

    nuevo_estado = data["estado"].strip().lower()
    resultado = turno_service.actualizar_estado(turno_id, nuevo_estado)

    return success_response(
        data=resultado,
        message="Estado del turno actualizado correctamente."
    )


# -----------------------------------------------------------------------------
# Tarea 4: POST /turnos/generar
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/generar", methods=["POST"])
def generar_turnos():
    data = request.get_json(silent=True) or {}
    turno_validator.validar_generacion_turnos(data)

    fecha_inicio = data["fecha_inicio"].strip()
    fecha_fin = data["fecha_fin"].strip()
    medico_id = data.get("medico_id")

    cantidad = turno_service.generar_turnos(
        fecha_inicio_str=fecha_inicio,
        fecha_fin_str=fecha_fin,
        medico_id=medico_id
    )

    return success_response(
        data={"turnos_generados": cantidad},
        message=f"Se generaron {cantidad} turnos exitosamente.",
        status_code=201
    )


# -----------------------------------------------------------------------------
# Tarea 5: POST /turnos (Reservar)
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos", methods=["POST"])
def reservar_turno():
    data = request.get_json(silent=True) or {}
    turno_validator.validar_reserva_turno(data)

    claims = _obtener_claims_actuales()
    paciente_id = None

    if claims.get("rol") == "paciente":
        paciente_id = claims.get("perfil_id")

    if paciente_id is None:
        paciente_id = data.get("paciente_id")

    if paciente_id is None:
        raise BadRequestError(
            description="Debe especificarse el 'paciente_id' para efectuar la reserva."
        )

    turno_id = data["turno_id"]
    resultado = turno_service.reservar_turno(turno_id=turno_id, paciente_id=paciente_id)

    return success_response(
        data=resultado,
        message="Turno reservado exitosamente.",
        status_code=201
    )
