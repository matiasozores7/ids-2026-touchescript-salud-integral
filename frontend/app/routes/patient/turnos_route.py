from flask import render_template, flash
from app.routes.patient import patient_bp
from app.services import turnos_service
from app.errors.exceptions import AppError

@patient_bp.route("/mis-turnos", methods=["GET"])
def mis_turnos():
    try:
        turnos = turnos_service.listar_mis_turnos()

        proximos = [
            turno for turno in turnos
            if turno["estado"] in ("reservado", "confirmado")
        ]

        historial = [
            turno for turno in turnos
            if turno["estado"] in ("atendido", "cancelado", "ausente")
        ]

    except AppError as error:
        proximos = []
        historial = []
        flash(error.message, "error")

    return render_template(
        "pacientes/mis_turnos.html",
        proximos=proximos,
        historial=historial,
    )

@patient_bp.route("/qr/<int:turno_id>", methods=["GET"])
def qr_turno(turno_id):
    return render_template(
        "pacientes/qr_turno.html",
        turno_id=turno_id
    )