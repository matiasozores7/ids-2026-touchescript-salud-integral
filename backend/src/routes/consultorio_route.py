from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services import consultorio_service
from src.utils.decorators import roles_requeridos
from src.utils.pagination import generate_hateoas_links, get_pagination_params
from src.validators import consultorio_validator
from src.utils.responses import success_response


consultorios_bp = Blueprint("consultorios", __name__)


@consultorios_bp.route("/consultorios", methods=["GET"])
@jwt_required()
@roles_requeridos("admin")
def listar_consultorios():
    limit, offset = get_pagination_params()
    items, total = consultorio_service.listar_consultorios(limit, offset)
    links = generate_hateoas_links(
        request.base_url,
        limit,
        offset,
        total,
        request.args
    )

    return success_response(
        data={"items": items, "total": total, "_links": links},
        message="Consultorios obtenidos correctamente."
    )


@consultorios_bp.route("/consultorios", methods=["POST"])
@jwt_required()
@roles_requeridos("admin")
def crear_consultorio():
    data = request.get_json(silent=True)
    consultorio_validator.validar_creacion(data)

    consultorio_id = consultorio_service.crear_consultorio(
        numero_sala=data["numero_sala"].strip(),
        piso=data["piso"].strip() if data.get("piso") is not None else None
    )

    return success_response(
        data={"id": consultorio_id},
        message="Consultorio creado correctamente.",
        status_code=201
    )


@consultorios_bp.route("/consultorios/<int(min=1):consultorio_id>", methods=["PUT"])
@jwt_required()
@roles_requeridos("admin")
def actualizar_consultorio(consultorio_id):
    data = request.get_json(silent=True)
    consultorio_validator.validar_actualizacion(data)

    consultorio_service.actualizar_consultorio(
        consultorio_id=consultorio_id,
        numero_sala=data["numero_sala"].strip(),
        piso=data["piso"].strip() if data.get("piso") is not None else None
    )

    return success_response(
        message="Consultorio actualizado correctamente."
    )


@consultorios_bp.route("/consultorios/<int(min=1):consultorio_id>", methods=["DELETE"])
@jwt_required()
@roles_requeridos("admin")
def eliminar_consultorio(consultorio_id):
    consultorio_service.eliminar_consultorio(consultorio_id)

    return success_response(
        message="Consultorio dado de baja correctamente."
    )
