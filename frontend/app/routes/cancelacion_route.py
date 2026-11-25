from datetime import datetime

from flask import Blueprint, render_template, request, url_for

from app.errors.exceptions import AppError
from app.services import turnos_service
from app.utils.date_format import fecha_larga


cancelacion_bp = Blueprint("cancelacion", __name__)


def _formatear_turno(turno: dict) -> dict:
    fecha_hora = datetime.fromisoformat(turno["fecha_hora"])
    turno["fecha_formateada"] = fecha_larga(fecha_hora)
    turno["hora_formateada"] = fecha_hora.strftime("%H:%M")
    turno["medico_completo"] = " ".join(
        parte
        for parte in (
            "Dr.",
            turno.get("medico_nombre") or "",
            turno.get("medico_apellido") or "",
        )
        if parte
    )
    sala = turno.get("consultorio_sala") or "Sin asignar"
    piso = turno.get("consultorio_piso")
    turno["consultorio_completo"] = f"Consultorio {sala}"
    if piso is not None:
        turno["consultorio_completo"] += f", piso {piso}"
    return turno


@cancelacion_bp.route("/cancelar-reserva", methods=["GET"])
def mostrar_confirmacion_cancelar():
    turno_id = request.args.get("turno_id", type=int)
    token = request.args.get("token", "").strip()

    if not turno_id or not token:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error="El enlace de cancelación está incompleto o no es válido.",
            turno=None,
            token="",
        )

    try:
        turno = turnos_service.obtener_detalle_publico(turno_id, token)
        return render_template(
            "pacientes/cancelar_reserva.html",
            error=None,
            turno=_formatear_turno(turno),
            token=token,
        )
    except AppError as error:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error=error.message,
            turno=None,
            token="",
        )
    except (KeyError, TypeError, ValueError):
        return render_template(
            "pacientes/cancelar_reserva.html",
            error="No se pudo interpretar la información del turno.",
            turno=None,
            token="",
        )


@cancelacion_bp.route("/cancelar-reserva", methods=["POST"])
def procesar_cancelacion():
    turno_id = request.form.get("turno_id", type=int)
    token = request.form.get("token", "").strip()

    if not turno_id or not token:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error="Los datos de cancelación están incompletos.",
            turno=None,
            token="",
        )

    try:
        turnos_service.cancelar_turno_con_token(turno_id, token)
    except AppError as error:
        return render_template(
            "pacientes/cancelar_reserva.html",
            error=error.message,
            turno=None,
            token="",
        )

    return render_template(
        "pacientes/cancelar_reserva_exito.html",
        inicio_url=url_for("auth.mostrar_login"),
    )
