from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.utils.responses import success_response
from src.utils.decorators import roles_requeridos
from src.utils.pagination import get_pagination_params, generate_hateoas_links
from src.services import medico_service

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