from flask import render_template

from . import backoffice_bp
from app.services.dashboard_service import (
    obtener_turnos_hoy,
    obtener_sala_espera
)


@backoffice_bp.get("/backoffice")
def dashboard():
    turnos_hoy = obtener_turnos_hoy()
    pacientes_sala_espera = obtener_sala_espera()

    return render_template(
        "backoffice/backoffice.html",
        turnos_hoy=turnos_hoy,
        pacientes_sala_espera=pacientes_sala_espera
    )