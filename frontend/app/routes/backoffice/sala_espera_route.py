
from flask import render_template, redirect, url_for, flash

from . import backoffice_bp

from app.services import sala_espera_service
from app.errors.exceptions import AppError


@backoffice_bp.get("/backoffice/sala-espera")
def backoffice_sala_espera():
    try:
        turnos = sala_espera_service.listar_turnos_sala_espera()

    except AppError as error:
        flash(str(error), "error")

        turnos = {
            "en_espera": [],
            "en_consulta": [],
            "por_llegar": []
        }

    return render_template(
        "backoffice/sala_espera.html",
        en_espera=turnos["en_espera"],
        en_consulta=turnos["en_consulta"],
        por_llegar=turnos["por_llegar"]
    )


@backoffice_bp.post("/backoffice/sala-espera/<int:turno_id>/llamar")
def llamar_paciente(turno_id):
    try:
        sala_espera_service.llamar_paciente(turno_id)

        flash(
            "Paciente llamado correctamente.",
            "success"
        )

    except AppError as error:
        flash(str(error), "error")

    return redirect(url_for("backoffice.backoffice_sala_espera"))


@backoffice_bp.post("/backoffice/sala-espera/<int:turno_id>/finalizar")
def finalizar_atencion(turno_id):
    try:
        sala_espera_service.finalizar_atencion(turno_id)

        flash(
            "Atención finalizada correctamente.",
            "success"
        )

    except AppError as error:
        flash(str(error), "error")

    return redirect(url_for("backoffice.backoffice_sala_espera"))
