from flask import Blueprint, request

from src.services import reportes_service
from src.utils.decorators import validar_rol
from src.utils.responses import success_response


reportes_bp = Blueprint("reportes", __name__)


@reportes_bp.route("/reportes", methods=["GET"])
@validar_rol("admin")
def obtener_reporte():
    periodo = request.args.get("period", default=28, type=int)

    datos = reportes_service.obtener_reportes(periodo)

    return success_response(
        data=datos,
        message="Reporte obtenido exitosamente"
    )