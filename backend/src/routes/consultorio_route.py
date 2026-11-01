from flask import Blueprint, request

from src.services import consultorio_service
from src.validators import consultorio_validator
from src.utils.responses import success_response


consultorios_bp = Blueprint("consultorios", __name__)


@consultorios_bp.route("/consultorios", methods=["GET"])
def listar_consultorios():
    consultorios = consultorio_service.listar_consultorios()

    return success_response(
        data=consultorios,
        message="Consultorios obtenidos correctamente."
    )


@consultorios_bp.route("/consultorios", methods=["POST"])
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
