
from flask import render_template, request, flash, redirect, url_for

from app.routes.backoffice import backoffice_bp
from app.errors.exceptions import AppError
from app.services import agendas_service
from app.services.turnos_service import (
    listar_medicos,
    listar_especialidades,
)


DIAS_SEMANA = [
    "Lunes",
    "Martes",
    "Miercoles",
    "Jueves",
    "Viernes",
    "Sabado",
]


def preparar_agenda_semanal(agendas):
    agenda_por_dia = []

    for dia in DIAS_SEMANA:
        bloques = []

        for agenda in agendas:
            if agenda["dia_semana"].lower() != dia.lower():
                continue

            hora_inicio = agenda["hora_inicio"][:5]
            hora_fin = agenda["hora_fin"][:5]
            duracion = agenda["duracion_turno"]

            inicio_minutos = (
                int(hora_inicio[:2]) * 60
                + int(hora_inicio[3:5])
            )

            fin_minutos = (
                int(hora_fin[:2]) * 60
                + int(hora_fin[3:5])
            )

            cantidad_turnos = (
                (fin_minutos - inicio_minutos) // duracion
            )

            bloques.append({
                **agenda,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "cantidad_turnos": cantidad_turnos,
            })

        agenda_por_dia.append({
            "dia": dia,
            "bloques": bloques,
        })

    return agenda_por_dia


@backoffice_bp.route("/backoffice/agendas")
def backoffice_agendas():
    try:
        medicos = listar_medicos()
        especialidades = listar_especialidades()
        consultorios = agendas_service.listar_consultorios()

        medico_id = request.args.get("medico_id", type=int)

        medico_seleccionado = next(
            (
                medico for medico in medicos
                if medico["id"] == medico_id
            ),
            medicos[0] if medicos else None,
        )

        agendas = []

        if medico_seleccionado:
            agendas = agendas_service.listar_agendas_medico(
                medico_seleccionado["id"]
            )

        for medico in medicos:
            bloques = agendas_service.listar_agendas_medico(
                medico["id"]
            )
            medico["cantidad_bloques"] = len(bloques)

        agenda_semanal = preparar_agenda_semanal(agendas)

    except AppError as exception:
        medicos = []
        especialidades = []
        consultorios = []
        medico_seleccionado = None
        agendas = []
        agenda_semanal = preparar_agenda_semanal([])

        flash(str(exception), "error")

    return render_template(
        "backoffice/agendas.html",
        medicos=medicos,
        especialidades=especialidades,
        consultorios=consultorios,
        medico_seleccionado=medico_seleccionado,
        agendas=agendas,
        agenda_semanal=agenda_semanal,
    )


@backoffice_bp.post("/backoffice/agendas/nuevo")
def crear_agenda():
    medico_id = request.form.get("medico_id", type=int)

    try:
        hora_inicio = request.form.get("hora_inicio", "")
        hora_fin = request.form.get("hora_fin", "")

        datos = {
            "medico_id": medico_id,
            "consultorio_id": request.form.get(
                "consultorio_id", type=int
            ),
            "dia_semana": request.form.get("dia_semana", ""),
            "hora_inicio": f"{hora_inicio}:00" if hora_inicio else "",
            "hora_fin": f"{hora_fin}:00" if hora_fin else "",
            "duracion_turno": request.form.get(
                "duracion_turno", type=int
            ),
        }

        agendas_service.crear_agenda(datos)

    except AppError as exception:
        flash(str(exception), "error")
    else:
        flash("Bloque horario creado correctamente.", "success")

    return redirect(
        url_for(
            "backoffice.backoffice_agendas",
            medico_id=medico_id,
        )
    )


@backoffice_bp.post("/backoffice/agendas/<int:agenda_id>/editar")
def editar_agenda(agenda_id):
    medico_id = request.form.get("medico_id", type=int)

    try:
        hora_inicio = request.form.get("hora_inicio", "")
        hora_fin = request.form.get("hora_fin", "")

        datos = {
            "medico_id": medico_id,
            "consultorio_id": request.form.get(
                "consultorio_id", type=int
            ),
            "dia_semana": request.form.get("dia_semana", ""),
            "hora_inicio": f"{hora_inicio}:00" if hora_inicio else "",
            "hora_fin": f"{hora_fin}:00" if hora_fin else "",
            "duracion_turno": request.form.get(
                "duracion_turno", type=int
            ),
        }

        agendas_service.actualizar_agenda(agenda_id, datos)

    except AppError as exception:
        flash(str(exception), "error")
    else:
        flash("Bloque horario actualizado correctamente.", "success")

    return redirect(
        url_for(
            "backoffice.backoffice_agendas",
            medico_id=medico_id,
        )
    )


@backoffice_bp.post("/backoffice/agendas/<int:agenda_id>/eliminar")
def eliminar_agenda(agenda_id):
    medico_id = request.form.get("medico_id", type=int)

    try:
        agendas_service.eliminar_agenda(agenda_id)

    except AppError as exception:
        flash(str(exception), "error")
    else:
        flash("Bloque horario eliminado correctamente.", "success")

    return redirect(
        url_for(
            "backoffice.backoffice_agendas",
            medico_id=medico_id,
        )
    )
