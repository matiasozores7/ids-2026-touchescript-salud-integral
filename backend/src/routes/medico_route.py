from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.utils.responses import success_response
from src.utils.decorators import roles_requeridos
from src.utils.pagination import get_pagination_params, generate_hateoas_links
from src.services import medico_service
from src.validators import medico_validator

medico_bp = Blueprint("medicos", __name__)

@medico_bp.route("/medicos", methods=["GET"])
@jwt_required()
@roles_requeridos("admin")
def listar_medicos():
    limit, offset = get_pagination_params()

    items, total = medico_service.listar_medicos(limit, offset)
    links = generate_hateoas_links(request.base_url, limit, offset, total, request.args)

    return success_response(
        data={"items": items, "total": total, "_links": links},
        message="Listado de médicos"
    )

@medico_bp.route("/medicos", methods=["POST"])
@jwt_required()
@roles_requeridos("admin")
def crear_medico():
    data = request.get_json() or {}
    medico_validator.validar_creacion(data)

    resultado = medico_service.crear_medico(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        password=data["password"],
        especialidad_id=data["especialidad_id"]
    )

    return success_response(
        data=resultado,
        message="Médico creado exitosamente",
        status_code=201
    )