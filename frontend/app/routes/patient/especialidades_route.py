from flask import render_template, flash

from app.routes.patient import patient_bp
from app.services import turnos_service
from app.errors.exceptions import AppError


@patient_bp.route("/especialidades", methods=["GET"])
def listar_especialidades():
    especialidades = []

    try:
        especialidades = turnos_service.listar_especialidades()

    except AppError as error:
        flash(error.message, "error")

    return render_template(
        "pacientes/especialidades.html",
        especialidades=especialidades
    )