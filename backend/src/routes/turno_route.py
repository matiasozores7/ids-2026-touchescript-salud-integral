from datetime import date

from flask import Blueprint, request

from src.errors.exceptions import BadRequestError, ForbiddenError
from src.services import turno_service
from src.utils.decorators import validar_rol, validar_token
from src.utils.jwt_config import obtener_claims_actuales
from src.utils.pagination import generate_hateoas_links, get_pagination_params
from src.utils.responses import success_response
from src.validators import turno_validator

turnos_bp = Blueprint("turnos", __name__)

@turnos_bp.route("/turnos/<int(min=1):turno_id>/estado", methods=["PATCH"])
@validar_rol("admin","medico")
def actualizar_estado_turno(turno_id: int):
    data = request.get_json(silent=True) or {}
    turno_validator.validar_actualizacion_estado(data)

    nuevo_estado = data["estado"].strip().lower()
    turno_service.actualizar_estado(turno_id, nuevo_estado)

    return success_response(
        message="Estado del turno actualizado correctamente."
    )


@turnos_bp.route("/turnos/generar", methods=["POST"])
@validar_rol("admin")
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
        message=f"Se generaron {cantidad} turnos exitosamente.",
        status_code=201
    )


@turnos_bp.route("/turnos", methods=["POST"])
@validar_rol("paciente", "admin")
def reservar_turno():
    data = request.get_json(silent=True) or {}
    turno_validator.validar_reserva_turno(data)

    claims = obtener_claims_actuales()
    paciente_id = None

    if claims.get("rol") == "paciente":
        paciente_id = claims.get("perfil_id")

        if paciente_id is None:
            raise ForbiddenError(
                description="No se pudo identificar el perfil del paciente autenticado."
            )
    else:
        paciente_id = data.get("paciente_id")

        if paciente_id is None:
            raise BadRequestError(
                description="Debe especificarse el 'paciente_id' para efectuar la reserva."
            )

    turno_id = turno_service.reservar_turno(turno_id=data["turno_id"], paciente_id=paciente_id)

    return success_response(
        data={"id": turno_id},
        message="Turno reservado exitosamente.",
        status_code=201
    )

@turnos_bp.route("/turnos/mis-turnos", methods=["GET"])
@validar_rol("paciente", "admin")
def listar_mis_turnos():
    claims = obtener_claims_actuales()
    rol = claims.get("rol")

    if rol == "paciente":
        paciente_id = claims.get("perfil_id")

        if paciente_id is None:
            raise ForbiddenError(
                description="No se pudo identificar el perfil del paciente autenticado."
            )
    else:
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


@turnos_bp.route("/turnos/<int(min=1):turno_id>/qr", methods=["GET"])
@validar_rol("paciente", "admin")
def obtener_qr_turno(turno_id: int):
    resultado = turno_service.obtener_qr_turno(turno_id)

    return success_response(
        data=resultado,
        message="Código QR del turno obtenido correctamente."
    )

@turnos_bp.route("/turnos/<int(min=1):turno_id>/cancelar", methods=["PATCH"])
@validar_rol("paciente", "admin")
def cancelar_turno(turno_id: int):
    claims = obtener_claims_actuales()
    rol = claims.get("rol")

    es_admin = rol == "admin"
    paciente_id = None

    if rol == "paciente":
        paciente_id = claims.get("perfil_id")

        if paciente_id is None:
            raise ForbiddenError(
                description="No se pudo identificar el perfil del paciente autenticado."
            )

    turno_service.cancelar_turno(
        turno_id=turno_id,
        paciente_id=paciente_id,
        es_admin=es_admin
    )

    return success_response(
        message="Turno cancelado exitosamente."
    )

@turnos_bp.route("/turnos/checkin", methods=["POST"])
@validar_rol("admin")
def checkin_turno():
    data = request.get_json(silent=True) or {}
    turno_validator.validar_checkin(data)

    qr_token = data["qr_token"].strip()
    turno_service.realizar_checkin(qr_token)

    return success_response(
        message="Check-in registrado exitosamente. Paciente ingresado a sala de espera."
    )

@turnos_bp.route("/turnos/<int(min=1):turno_id>/atendido", methods=["PATCH"])
@validar_rol("admin", "medico")
def marcar_turno_atendido(turno_id: int):
    turno_service.marcar_atendido(turno_id)

    return success_response(
        message="Turno marcado como atendido exitosamente."
    )

@turnos_bp.route("/turnos/marcar-ausentes", methods=["POST"])
@validar_rol("admin")
def marcar_turnos_ausentes():
    afectados = turno_service.marcar_ausentes()

    return success_response(
        message=f"Se actualizaron {afectados} turnos al estado ausente."
    )

@turnos_bp.route(
    "/medicos/<int(min=1):medico_id>/dias-disponibles",
    methods=["GET"]
)
@validar_token
def obtener_dias_disponibles(medico_id: int):
    dias = turno_service.obtener_dias_disponibles(medico_id)

    return success_response(
        data=dias,
        message="Días disponibles obtenidos correctamente."
    )

@turnos_bp.route(
    "/medicos/<int(min=1):medico_id>/horarios-disponibles",
    methods=["GET"]
)
@validar_token
def obtener_horarios_disponibles(medico_id: int):
    fecha = request.args.get("fecha")

    if not fecha:
        raise BadRequestError(
            description="El parámetro 'fecha' es obligatorio."
        )

    try:
        date.fromisoformat(fecha)
    except ValueError:
        raise BadRequestError(
            description="La fecha debe tener el formato YYYY-MM-DD."
        )

    horarios = turno_service.obtener_horarios_disponibles(
        medico_id=medico_id,
        fecha=fecha
    )

    return success_response(
        data=horarios,
        message="Horarios disponibles obtenidos correctamente."
    )


@turnos_bp.route(
    "/medicos/<int(min=1):medico_id>/turnos-disponibles",
    methods=["GET"]
)
@validar_rol("paciente", "admin")
def listar_turnos_disponibles(medico_id: int):
    turnos = turno_service.listar_turnos_disponibles(medico_id)

    return success_response(
        data=turnos,
        message="Turnos disponibles obtenidos correctamente."
    )