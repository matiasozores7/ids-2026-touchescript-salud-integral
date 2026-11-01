from flask import Blueprint

from src.database.connection import get_db_connection
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
