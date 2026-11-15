from datetime import date, timedelta

from flask import render_template, request

from app.routes.backoffice import backoffice_bp
from app.services.turnos_service import (
    listar_turnos_calendario,
    listar_especialidades,
    listar_medicos,
)


@backoffice_bp.route("/backoffice/calendario")
def backoffice_calendario():
    fecha_inicio_param = request.args.get("fecha_inicio")

    if fecha_inicio_param:
        fecha_inicio = date.fromisoformat(fecha_inicio_param)
    else:
        hoy = date.today()
        fecha_inicio = hoy - timedelta(days=hoy.weekday())

    # El calendario muestra de lunes a sábado.
    if fecha_inicio.weekday() != 0:
        fecha_inicio -= timedelta(days=fecha_inicio.weekday())

    fecha_fin = fecha_inicio + timedelta(days=5)

    especialidad_id = request.args.get("especialidad_id", type=int)
    medico_id = request.args.get("medico_id", type=int)

    turnos = listar_turnos_calendario(
        fecha_inicio=fecha_inicio.isoformat(),
        fecha_fin=fecha_fin.isoformat(),
        especialidad_id=especialidad_id,
        medico_id=medico_id,
    )

    especialidades = listar_especialidades()
    medicos = listar_medicos()

    return render_template(
        "backoffice/calendario.html",
        turnos=turnos,
        especialidades=especialidades,
        medicos=medicos,
        fecha_inicio=fecha_inicio.isoformat(),
        fecha_fin=fecha_fin.isoformat(),
    )