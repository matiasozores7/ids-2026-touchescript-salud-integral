from flask import flash, render_template, request

from app.errors.exceptions import AppError
from app.routes.backoffice import backoffice_bp
from app.services.reportes_service import obtener_reportes


@backoffice_bp.route("/backoffice/reportes")
def backoffice_reportes():
    periodo = request.args.get("period", 28, type=int)

    if periodo not in (7, 14, 28):
        periodo = 28

    try:
        resultado = obtener_reportes(periodo)
    except AppError as error:
        flash(error.message, "error")
        resultado = {
            "report_data": {
                "specialties": {"labels": [], "values": []},
                "appointmentResults": {
                    "labels": ["Atendido", "Ausente", "Cancelado"],
                    "values": [0, 0, 0],
                },
                "occupancy": {"labels": [], "values": []},
                "waiting": {"labels": [], "values": []},
                "professionals": {"labels": [], "values": []},
            },
            "total_turnos": 0,
            "ausentismo_general": 0,
            "espera_promedio": 0,
        }

    return render_template(
        "backoffice/reportes.html",
        report_data=resultado["report_data"],
        total_turnos=resultado["total_turnos"],
        ausentismo_general=resultado["ausentismo_general"],
        espera_promedio=resultado["espera_promedio"],
        periodo=periodo,
    )