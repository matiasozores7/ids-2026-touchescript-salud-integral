
from datetime import datetime

from flask import render_template, flash

from app.routes.patient import patient_bp
from app.services import turnos_service
from app.errors.exceptions import AppError


@patient_bp.route("/pacientes", methods=["GET"])
def patient_home():
    especialidades = []
    medicos = []
    proximo_turno = None

    try:
        especialidades = turnos_service.listar_especialidades()
        medicos = turnos_service.listar_medicos()
        turnos = turnos_service.listar_mis_turnos()

        ahora = datetime.now()

        proximos = [
            turno for turno in turnos
            if turno["estado"] in ("reservado", "confirmado")
            and datetime.fromisoformat(turno["fecha_hora"]) > ahora
        ]

        if proximos:
            proximo_turno = min(
                proximos,
                key=lambda turno: datetime.fromisoformat(turno["fecha_hora"])
            )

    except AppError as error:
        flash(error.message, "error")

    return render_template(
        "pacientes/home.html",
        especialidades=especialidades,
        medicos=medicos,
        proximo_turno=proximo_turno
    )
