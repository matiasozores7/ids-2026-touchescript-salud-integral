from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services import turnos_service
from app.errors.exceptions import AppError

cancelacion_bp = Blueprint("cancelacion", __name__)

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


@cancelacion_bp.route("/cancelar-reserva", methods=["GET"])
def mostrar_confirmacion_cancelar():
    turno_id = request.args.get("turno_id", type=int)
    token = request.args.get("token", "").strip()

    if not turno_id or not token:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error="El enlace de cancelación es incompleto o no contiene un token válido.",
            turno=None,
            token=token,
            turno_id=turno_id,
        )

    try:
        turno = turnos_service.obtener_detalle_publico(turno_id, token)

        # Formatear fecha y hora para visualización amigable
        fecha_hora_raw = turno.get("fecha_hora")
        if fecha_hora_raw:
            try:
                dt = datetime.fromisoformat(fecha_hora_raw)
                turno["fecha_formateada"] = f"{DIAS_SEMANA.get(dt.weekday(), '')} {dt.day} de {MESES.get(dt.month, '')} de {dt.year}"
                turno["hora_formateada"] = dt.strftime("%H:%M")
            except Exception:
                turno["fecha_formateada"] = str(fecha_hora_raw)
                turno["hora_formateada"] = ""

        medico_nom = turno.get("medico_nombre") or ""
        medico_ape = turno.get("medico_apellido") or ""
        turno["medico_completo"] = f"Dr. {medico_nom} {medico_ape}".strip()

        sala = turno.get("consultorio_sala") or "-"
        piso = turno.get("consultorio_piso") or "-"
        turno["consultorio_completo"] = f"Consultorio {sala} (Piso {piso})"

        return render_template(
            "pacientes/cancelar_reserva.html",
            error=None,
            turno=turno,
            token=token,
            turno_id=turno_id,
        )

    except AppError as err:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error=err.message,
            turno=None,
            token=token,
            turno_id=turno_id,
        )


@cancelacion_bp.route("/cancelar-reserva", methods=["POST"])
def procesar_cancelacion():
    turno_id = request.form.get("turno_id", type=int)
    token = request.form.get("token", "").strip()

    if not turno_id or not token:
        flash("Datos de cancelación incompletos.", "error")
        return redirect(url_for("cancelacion.mostrar_confirmacion_cancelar", turno_id=turno_id, token=token))

    try:
        turnos_service.cancelar_turno_con_token(turno_id, token)
        return render_template(
            "pacientes/cancelar_reserva_exito.html",
            turno_id=turno_id,
        )
    except AppError as err:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error=err.message,
            turno=None,
            token=token,
            turno_id=turno_id,
        )

