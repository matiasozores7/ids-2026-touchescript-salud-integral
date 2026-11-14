from flask import render_template

from . import backoffice_bp
from app.services.dashboard_service import (
    obtener_turnos_hoy,
    obtener_sala_espera,
    obtener_ausentismo,
    obtener_turnos_por_hora,
    obtener_proximos_turnos,
    obtener_estadisticas_generales
)


@backoffice_bp.get("/backoffice")
def dashboard():
    turnos_hoy = obtener_turnos_hoy()
    pacientes_sala_espera = obtener_sala_espera()
    estadisticas_ausentismo = obtener_ausentismo()
    turnos_por_hora = obtener_turnos_por_hora()
    proximos_turnos = obtener_proximos_turnos()
    estadisticas_generales = obtener_estadisticas_generales()

    return render_template(
        "backoffice/backoffice.html",
        turnos_hoy=turnos_hoy,
        pacientes_sala_espera=pacientes_sala_espera,
        estadisticas_ausentismo=estadisticas_ausentismo,
        turnos_por_hora=turnos_por_hora,
        proximos_turnos=proximos_turnos,
        estadisticas_generales=estadisticas_generales
    )