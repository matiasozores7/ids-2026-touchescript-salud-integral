from flask import render_template, flash, request

from app.routes.patient import patient_bp
from app.services import turnos_service
from app.errors.exceptions import AppError


@patient_bp.route("/profesionales", methods=["GET"])
def listar_profesionales():
    medicos = []
    especialidades = []

    especialidad_id = request.args.get("especialidad_id", type=int)
    busqueda = request.args.get("q", "").strip()

    try:
        medicos = turnos_service.listar_medicos(especialidad_id)
        especialidades = turnos_service.listar_especialidades()

        if busqueda:
            termino = busqueda.casefold()

            medicos = [
                medico for medico in medicos
                if termino in medico.get("nombre", "").casefold()
                or termino in medico.get("apellido", "").casefold()
            ]

    except AppError as error:
        flash(error.message, "error")

    return render_template(
        "pacientes/profesionales.html",
        medicos=medicos,
        especialidades=especialidades,
        especialidad_id=especialidad_id,
        busqueda=busqueda
    )