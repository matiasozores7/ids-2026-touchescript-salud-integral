from flask import Blueprint, request

from src.database.connection import get_db_connection
from src.errors.exceptions import BadRequestError
from src.repositories import consultorio_repository as consultorio_repo
from src.utils.responses import success_response


consultorios_bp = Blueprint("consultorios", __name__)


@consultorios_bp.route("/consultorios", methods=["GET"])
def listar_consultorios():
    connection = get_db_connection()

    try:
        consultorios = consultorio_repo.listar_consultorios_activos(connection)
    finally:
        connection.close()

    return success_response(
        data=consultorios,
        message="Consultorios obtenidos correctamente."
    )


@consultorios_bp.route("/consultorios", methods=["POST"])
def crear_consultorio():
    data = request.get_json() or {}
    numero_sala = data.get("numero_sala")

    if not isinstance(numero_sala, str) or not numero_sala.strip():
        raise BadRequestError(
            description="El campo numero_sala es obligatorio y debe ser un texto."
        )

    piso = data.get("piso")
    if piso is not None and not isinstance(piso, str):
        raise BadRequestError(
            description="El campo piso debe ser un texto."
        )

    connection = get_db_connection()

    try:
        consultorio_id = consultorio_repo.crear_consultorio(
            connection,
            numero_sala=numero_sala.strip(),
            piso=piso.strip() if piso is not None else None
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return success_response(
        data={"id": consultorio_id},
        message="Consultorio creado correctamente.",
        status_code=201
    )
