from flask import Blueprint, request

from src.services import coberturas_service
from src.utils.decorators import validar_rol
from src.utils.pagination import generate_hateoas_links, get_pagination_params
from src.utils.responses import success_response
from src.validators import coberturas_validator


coberturas_bp = Blueprint("coberturas", __name__)


@coberturas_bp.route("/coberturas", methods=["GET"])
def listar_coberturas():
    limit, offset = get_pagination_params()

    items, total = coberturas_service.listar_coberturas(limit, offset)

    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total,
        request.args
    )

    return success_response(
        data={"items": items, "total": total, "_links": links},
        message="Coberturas obtenidas correctamente."
    )


@coberturas_bp.route(
    "/coberturas/<int(min=1):cobertura_id>",
    methods=["GET"]
)
def obtener_cobertura(cobertura_id):
    cobertura = coberturas_service.obtener_cobertura(cobertura_id)

    return success_response(
        data=cobertura,
        message="Cobertura obtenida correctamente."
    )


@coberturas_bp.route("/coberturas", methods=["POST"])
@validar_rol("admin")
def crear_cobertura():
    data = request.get_json(silent=True)
    coberturas_validator.validar_creacion(data)

    cobertura_id = coberturas_service.crear_cobertura(
        nombre=data["nombre"].strip()
    )

    return success_response(
        data={"id": cobertura_id},
        message="Cobertura creada correctamente.",
        status_code=201
    )


@coberturas_bp.route(
    "/coberturas/<int(min=1):cobertura_id>",
    methods=["PUT"]
)
@validar_rol("admin")
def actualizar_cobertura(cobertura_id):
    data = request.get_json(silent=True)
    coberturas_validator.validar_actualizacion(data)

    coberturas_service.actualizar_cobertura(
        cobertura_id=cobertura_id,
        nombre=data["nombre"].strip()
    )

    return success_response(
        message="Cobertura actualizada correctamente."
    )


@coberturas_bp.route(
    "/coberturas/<int(min=1):cobertura_id>",
    methods=["DELETE"]
)
@validar_rol("admin")
def eliminar_cobertura(cobertura_id):
    coberturas_service.eliminar_cobertura(cobertura_id)

    return success_response(
        message="Cobertura eliminada correctamente."
    )