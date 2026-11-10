from flask import Blueprint, request

from src.utils.responses import success_response
from src.utils.decorators import validar_rol
from src.utils.pagination import get_pagination_params, generate_hateoas_links
from src.services import medico_service
from src.validators import medico_validator

medico_bp = Blueprint("medicos", __name__)


@medico_bp.route("/medicos", methods=["GET"])
@validar_rol("admin", "paciente")
def listar_medicos():
    limit, offset = get_pagination_params()
    especialidad_id = request.args.get("especialidad_id", type=int)

    items, total = medico_service.listar_medicos(limit, offset, especialidad_id=especialidad_id)
    links = generate_hateoas_links(request.base_url, limit, offset, total, request.args)

    return success_response(
        data={"items": items, "total": total, "_links": links},
        message="Listado de médicos"
    )


@medico_bp.route("/medicos/<int(min=1):medico_id>", methods=["GET"])
@validar_rol("admin", "paciente")
def obtener_medico(medico_id):
    resultado = medico_service.obtener_medico(medico_id)

    return success_response(data=resultado, message="Detalle del médico")


@medico_bp.route("/medicos", methods=["POST"])
@validar_rol("admin")
def crear_medico():
    data = request.get_json() or {}
    medico_validator.validar_creacion(data)

    medico_id = medico_service.crear_medico(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        password=data["password"],
        especialidad_id=data["especialidad_id"]
    )

    return success_response(
        data={"id": medico_id},
        message="Médico creado exitosamente",
        status_code=201
    )


@medico_bp.route("/medicos/<int(min=1):medico_id>", methods=["PATCH"])
@validar_rol("admin")
def modificar_medico(medico_id):
    data = request.get_json() or {}
    medico_validator.validar_modificacion_parcial(data)

    medico_service.modificar_medico(medico_id, data)

    return success_response(message="Médico modificado exitosamente")


@medico_bp.route("/medicos/<int(min=1):medico_id>", methods=["DELETE"])
@validar_rol("admin")
def eliminar_medico(medico_id):
    medico_service.eliminar_medico(medico_id)

    return success_response(message="Médico dado de baja exitosamente")