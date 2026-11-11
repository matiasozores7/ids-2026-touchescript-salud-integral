from flask import render_template, flash, redirect, url_for
from app.routes.patient import patient_bp
from app.services import turnos_service
from app.errors.exceptions import AppError
from datetime import datetime

MESES = {
    1: "enero", 2: "febrero", 3: "marzo",
    4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre",
    10: "octubre", 11: "noviembre", 12: "diciembre"
}

DIAS = [
    "lunes", "martes", "miércoles", "jueves",
    "viernes", "sábado", "domingo"
]

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

@patient_bp.route("/mis-turnos/<int:turno_id>", methods=["GET"])
def detalle_turno(turno_id):
    try:
        turno = turnos_service.obtener_detalle_turno(turno_id)

        fecha_hora = datetime.fromisoformat(turno["fecha_hora"])

        turno["fecha_larga"] = (
            f"{DIAS[fecha_hora.weekday()].capitalize()} "
            f"{fecha_hora.day} de {MESES[fecha_hora.month]}"
        )

        turno["hora"] = fecha_hora.strftime("%H:%M")
        turno["medico"] = (
            f"{turno['medico_nombre']} {turno['medico_apellido']}"
        )
        turno["especialidad"] = turno["especialidad_nombre"]
        turno["iniciales"] = (
            turno["medico_nombre"][0]
            + turno["medico_apellido"][0]
        )
        turno["consultorio"] = (
            f"Consultorio {turno['consultorio_sala']}"
        )
        turno["piso"] = turno["consultorio_piso"]
        turno["llegada"] = turno["fecha_hora_llegada"]

    except AppError as error:
        flash(error.message, "error")
        return redirect(url_for("patient.mis_turnos"))

    except (KeyError, ValueError, TypeError):
        flash("No se pudo interpretar la información del turno.", "error")
        return redirect(url_for("patient.mis_turnos"))

    return render_template(
        "pacientes/detalle_turno.html",
        turno=turno
    )

@patient_bp.route("/mis-turnos/<int:turno_id>/cancelar", methods=["POST"])
def cancelar_turno(turno_id):
    try:
        turnos_service.cancelar_turno(turno_id)
        flash("El turno fue cancelado exitosamente.", "success")

    except AppError as error:
        flash(error.message, "error")

    return redirect(
        url_for("patient.detalle_turno", turno_id=turno_id)
    )

@patient_bp.route("/qr/<int:turno_id>", methods=["GET"])
def qr_turno(turno_id):
    try:
        turno = turnos_service.obtener_detalle_turno(turno_id)
        qr_token = turnos_service.obtener_qr_turno(turno_id)

        fecha_hora = datetime.fromisoformat(turno["fecha_hora"])

        turno["fecha_larga"] = (
            f"{DIAS[fecha_hora.weekday()]} "
            f"{fecha_hora.day} de {MESES[fecha_hora.month]}"
        )

        turno["hora"] = fecha_hora.strftime("%H:%M")

        turno["medico"] = (
            f"{turno['medico_nombre']} {turno['medico_apellido']}"
        )

        turno["paciente"] = (
            f"{turno['paciente_nombre']} {turno['paciente_apellido']}"
        )

        turno["consultorio"] = (
            f"Consultorio {turno['consultorio_sala']}"
        )

        return render_template(
            "pacientes/qr_turno.html",
            turno=turno,
            qr_token=qr_token,
        )

    except AppError as error:
        flash(error.message, "error")
        return redirect(
            url_for("patient.detalle_turno", turno_id=turno_id)
        )

    except (KeyError, ValueError, TypeError):
        flash(
            "No se pudo obtener la información del comprobante.",
            "error",
        )
        return redirect(
            url_for("patient.detalle_turno", turno_id=turno_id)
        )