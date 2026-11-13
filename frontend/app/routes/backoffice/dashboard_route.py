from flask import render_template

from . import backoffice_bp
from app.services.dashboard_service import obtener_turnos_hoy


@backoffice_bp.get("/backoffice")
def dashboard():
    turnos_hoy = obtener_turnos_hoy()

    return render_template(
        "backoffice/backoffice.html",
        turnos_hoy=turnos_hoy
    )