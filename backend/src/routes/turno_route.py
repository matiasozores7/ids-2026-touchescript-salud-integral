from flask import Blueprint, request
from flask_jwt_extended import get_jwt

from src.errors.exceptions import BadRequestError
from src.services import turno_service
from src.utils.decorators import validar_rol, validar_token
from src.utils.pagination import generate_hateoas_links, get_pagination_params
from src.utils.responses import success_response
from src.validators import turno_validator

turnos_bp = Blueprint("turnos", __name__)


def _obtener_claims_actuales() -> dict:
    return get_jwt() or {}


# -----------------------------------------------------------------------------
# Tarea 3: PUT /turnos/<id>/estado
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/<int(min=1):turno_id>/estado", methods=["PUT", "PATCH"])
@validar_token
@validar_rol("admin", "recepcionista", "medico")
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
@validar_token
@validar_rol("admin", "recepcionista")
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
@validar_token
@validar_rol("paciente", "admin", "recepcionista")
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


# -----------------------------------------------------------------------------
# Tarea 6: GET /turnos/mis-turnos
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/mis-turnos", methods=["GET"])
@validar_token
@validar_rol("paciente", "admin", "recepcionista")
def listar_mis_turnos():
    claims = _obtener_claims_actuales()
    paciente_id = None

    if claims.get("rol") == "paciente":
        paciente_id = claims.get("perfil_id")

    if paciente_id is None:
        paciente_id = request.args.get("paciente_id", type=int)

    if paciente_id is None:
        raise BadRequestError(
            description="Se requiere identificar al paciente para consultar sus turnos."
        )

    limit, offset = get_pagination_params()
    estado = request.args.get("estado")
    if estado:
        estado = estado.strip().lower()

    items, total = turno_service.listar_mis_turnos(
        paciente_id=paciente_id,
        limit=limit,
        offset=offset,
        estado=estado
    )

    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total,
        request.args
    )

    return success_response(
        data={"items": items, "total": total, "_links": links},
        message="Turnos del paciente obtenidos correctamente."
    )


# -----------------------------------------------------------------------------
# Tarea 7: PUT /turnos/<id>/cancelar
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/<int(min=1):turno_id>/cancelar", methods=["PUT", "PATCH"])
@validar_token
@validar_rol("paciente", "admin", "recepcionista")
def cancelar_turno(turno_id: int):
    claims = _obtener_claims_actuales()
    es_admin = claims.get("rol") in ("admin", "recepcionista")
    paciente_id = claims.get("perfil_id") if claims.get("rol") == "paciente" else None

    # Si no hay token de paciente pero vino en query/body para pruebas
    if paciente_id is None and not es_admin:
        data = request.get_json(silent=True) or {}
        paciente_id = data.get("paciente_id") or request.args.get("paciente_id", type=int)

    resultado = turno_service.cancelar_turno(
        turno_id=turno_id,
        paciente_id=paciente_id,
        es_admin=es_admin
    )

    return success_response(
        data=resultado,
        message="Turno cancelado exitosamente."
    )


# -----------------------------------------------------------------------------
# Tarea 8: POST /turnos/checkin
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/checkin", methods=["POST"])
@validar_token
@validar_rol("paciente", "admin", "recepcionista")
def checkin_turno():
    data = request.get_json(silent=True) or {}
    turno_validator.validar_checkin(data)

    qr_token = data["qr_token"].strip()
    resultado = turno_service.realizar_checkin(qr_token)

    return success_response(
        data=resultado,
        message="Check-in registrado exitosamente. Paciente ingresado a sala de espera."
    )


# -----------------------------------------------------------------------------
# Tarea 9: PUT /turnos/<id>/atendido
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/<int(min=1):turno_id>/atendido", methods=["PUT", "PATCH"])
@validar_token
@validar_rol("admin", "medico")
def marcar_turno_atendido(turno_id: int):
    resultado = turno_service.marcar_atendido(turno_id)

    return success_response(
        data=resultado,
        message="Turno marcado como atendido exitosamente."
    )


# -----------------------------------------------------------------------------
# Tarea 10: POST /turnos/marcar-ausentes
# -----------------------------------------------------------------------------
@turnos_bp.route("/turnos/marcar-ausentes", methods=["POST"])
@validar_token
@validar_rol("admin", "recepcionista")
def marcar_turnos_ausentes():
    afectados = turno_service.marcar_ausentes()

    return success_response(
        data={"turnos_marcados": afectados},
        message=f"Se actualizaron {afectados} turnos al estado ausente."
    )
