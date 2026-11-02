from flask import Blueprint, request

from src.services import turno_service
from src.utils.responses import success_response
from src.validators import turno_validator

turnos_bp = Blueprint("turnos", __name__)


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
