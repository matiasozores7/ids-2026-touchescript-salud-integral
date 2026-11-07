from flask import Blueprint, request
from src.utils.decorators import validar_token

from src.services import especialidades_service
from src.utils.decorators import roles_requeridos
from src.utils.pagination import generate_hateoas_links, get_pagination_params
from src.utils.responses import success_response
from src.validators import especialidades_validator


especialidades_bp = Blueprint("especialidades", __name__)


@especialidades_bp.route("/especialidades", methods=["GET"])
@validar_token
@roles_requeridos("admin")
def listar_especialidades():
    limit, offset = get_pagination_params()
    items, total = especialidades_service.listar_especialidades(limit, offset)
    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total,
        request.args
    )

    return success_response(
        data={"items": items, "total": total, "_links": links},
        message="Especialidades obtenidas correctamente."
    )


@especialidades_bp.route("/especialidades", methods=["POST"])
@validar_token
@roles_requeridos("admin")
def crear_especialidad():
    data = request.get_json(silent=True)
    especialidades_validator.validar_creacion(data)

    especialidad_id = especialidades_service.crear_especialidad(
        nombre=data["nombre"].strip(),
        descripcion=data["descripcion"].strip()
        if data.get("descripcion") is not None else None
    )

    return success_response(
        data={"id": especialidad_id},
        message="Especialidad creada correctamente.",
        status_code=201
    )


@especialidades_bp.route(
    "/especialidades/<int(min=1):especialidad_id>",
    methods=["PUT"]
)
@validar_token
@roles_requeridos("admin")
def actualizar_especialidad(especialidad_id):
    data = request.get_json(silent=True)
    especialidades_validator.validar_actualizacion(data)

    especialidades_service.actualizar_especialidad(
        especialidad_id=especialidad_id,
        nombre=data["nombre"].strip(),
        descripcion=data["descripcion"].strip()
        if data.get("descripcion") is not None else None
    )

    return success_response(
        message="Especialidad actualizada correctamente."
    )


@especialidades_bp.route(
    "/especialidades/<int(min=1):especialidad_id>",
    methods=["DELETE"]
)
@validar_token
@roles_requeridos("admin")
def eliminar_especialidad(especialidad_id):
    especialidades_service.eliminar_especialidad(especialidad_id)

    return success_response(
        message="Especialidad eliminada correctamente."
    )