
from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from app.routes.patient import patient_bp
from app.services import turnos_service
from app.errors.exceptions import AppError


MESES = {
    1: "enero", 2: "febrero", 3: "marzo",
    4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre",
    10: "octubre", 11: "noviembre", 12: "diciembre",
}

DIAS_SEMANA = {
    0: "Lunes", 1: "Martes", 2: "Miércoles",
    3: "Jueves", 4: "Viernes", 5: "Sábado",
    6: "Domingo",
}


@patient_bp.route("/reservar-turno", methods=["GET"])
def reservar_especialidad():
    try:
        especialidades = turnos_service.listar_especialidades()
    except AppError as error:
        flash(error.message, "error")
        especialidades = []

    return render_template(
        "pacientes/reserva/especialidad.html",
        especialidades=especialidades,
    )


@patient_bp.route(
    "/reservar-turno/especialidades/<int:especialidad_id>/medicos",
    methods=["GET"]
)
def reservar_medico(especialidad_id):
    try:
        medicos = turnos_service.listar_medicos(especialidad_id)
    except AppError as error:
        flash(error.message, "error")
        medicos = []

    return render_template(
        "pacientes/reserva/medico.html",
        especialidad_id=especialidad_id,
        medicos=medicos,
    )


@patient_bp.route(
    "/reservar-turno/medicos/<int:medico_id>/fecha-hora",
    methods=["GET"]
)
def reservar_fecha_hora(medico_id):
    try:
        medico = turnos_service.obtener_medico(medico_id)
        turnos = turnos_service.listar_turnos_disponibles(medico_id)

        fechas_dict = {}
        turnos_lista = []

        for turno in turnos:
            fecha_hora = datetime.fromisoformat(turno["fecha_hora"])

            fecha = fecha_hora.strftime("%Y-%m-%d")
            hora = fecha_hora.strftime("%H:%M")

            if fecha not in fechas_dict:
                fechas_dict[fecha] = {
                    "valor": fecha,
                    "dia": DIAS_SEMANA[fecha_hora.weekday()][:3],
                    "num": fecha_hora.day,
                    "libres": 0,
                }

            fechas_dict[fecha]["libres"] += 1

            turnos_lista.append({
                "id": turno["id"],
                "fecha": fecha,
                "hora": hora,
                "consultorio": (
                    f"Consultorio {turno.get('consultorio_sala', '')}"
                ),
            })

    except (AppError, KeyError, ValueError) as error:
        mensaje = (
            error.message if isinstance(error, AppError)
            else "No se pudieron interpretar los turnos disponibles."
        )
        flash(mensaje, "error")
        medico = {}
        fechas_dict = {}
        turnos_lista = []

    return render_template(
        "pacientes/reserva/fecha_hora.html",
        medico_id=medico_id,
        medico=medico,
        fechas=list(fechas_dict.values()),
        turnos_lista=turnos_lista,
    )


@patient_bp.route("/reservar-turno/confirmacion", methods=["GET"])
def reservar_confirmacion():
    medico_id = request.args.get("medico_id", type=int)
    turno_id = request.args.get("turno_id", type=int)
    fecha = request.args.get("fecha", "")
    hora = request.args.get("hora", "")

    if not all((medico_id, turno_id, fecha, hora)):
        flash("La selección del turno está incompleta.", "error")
        return redirect(url_for("patient.reservar_especialidad"))

    try:
        fecha_hora = datetime.fromisoformat(f"{fecha}T{hora}")

        if fecha_hora <= datetime.now():
            flash("El turno seleccionado ya pasó.", "error")
            return redirect(
                url_for(
                    "patient.reservar_fecha_hora",
                    medico_id=medico_id,
                )
            )

        medico = turnos_service.obtener_medico(medico_id)

        fecha_formateada = (
            f"{DIAS_SEMANA[fecha_hora.weekday()]} "
            f"{fecha_hora.day} de {MESES[fecha_hora.month]}"
        )

    except (AppError, ValueError) as error:
        mensaje = (
            error.message if isinstance(error, AppError)
            else "La fecha u hora seleccionada no es válida."
        )
        flash(mensaje, "error")
        return redirect(
            url_for(
                "patient.reservar_fecha_hora",
                medico_id=medico_id,
            )
        )

    return render_template(
        "pacientes/reserva/confirmacion.html",
        medico_id=medico_id,
        turno_id=turno_id,
        medico=medico,
        fecha=fecha,
        fecha_formateada=fecha_formateada,
        hora=hora,
    )


@patient_bp.route("/reservar-turno/resultado", methods=["POST"])
def reservar_resultado():
    turno_id = request.form.get("turno_id", type=int)
    medico_id = request.form.get("medico_id", type=int)

    if not turno_id:
        flash("No se especificó un turno válido.", "error")
        return redirect(url_for("patient.reservar_especialidad"))

    try:
        turnos_service.reservar_turno(turno_id)
        flash("Turno reservado exitosamente.", "success")
        return redirect(url_for("patient.mis_turnos"))

    except AppError as error:
        flash(error.message, "error")

        if medico_id:
            return redirect(
                url_for(
                    "patient.reservar_fecha_hora",
                    medico_id=medico_id,
                )
            )

        return redirect(url_for("patient.reservar_especialidad"))
