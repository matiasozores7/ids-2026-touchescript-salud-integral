from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.services import turno_service

patient_bp = Blueprint("patient", __name__)

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
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
    12: "diciembre"
}


@patient_bp.route("/pacientes", methods=["GET", "POST"])
def patient_home():
    token = session.get("access_token")
    proximo_turno = None

    if token:
        try:
            turnos = turno_service.listar_mis_turnos(token)
            proximos = [t for t in turnos if t["estado"] in ("reservado", "confirmado")]
            if proximos:
                proximo_turno = proximos[0]
        except RuntimeError:
            pass

    return render_template("pacientes/home.html", proximo_turno=proximo_turno)


@patient_bp.route("/mis-turnos", methods=["GET"])
def mis_turnos():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para ver tus turnos.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turnos = turno_service.listar_mis_turnos(token)
        proximos = [t for t in turnos if t["estado"] in ("reservado", "confirmado")]
        historial = [t for t in turnos if t["estado"] in ("atendido", "cancelado", "ausente")]
    except RuntimeError as error:
        proximos = []
        historial = []
        flash(str(error), "error")

    return render_template(
        "pacientes/mis_turnos.html",
        proximos=proximos,
        historial=historial
    )


@patient_bp.route("/mis-turnos/<int:turno_id>", methods=["GET"])
def detalle_turno(turno_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para ver el detalle del turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turno = turno_service.obtener_detalle_turno(token, turno_id)
    except RuntimeError as error:
        flash(str(error), "error")
        return redirect(url_for("patient.mis_turnos"))

    return render_template("pacientes/detalle_turno.html", turno=turno, turno_id=turno_id)


@patient_bp.route("/qr/<int:turno_id>", methods=["GET"])
def qr_turno(turno_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para ver el código QR.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turno = turno_service.obtener_detalle_turno(token, turno_id)
        qr_data = turno_service.obtener_qr_turno(token, turno_id)
        qr_token = qr_data.get("qr_token")
    except RuntimeError as error:
        flash(str(error), "error")
        return redirect(url_for("patient.mis_turnos"))

    return render_template(
        "pacientes/qr_turno.html",
        turno=turno,
        turno_id=turno_id,
        qr_token=qr_token
    )


@patient_bp.route("/mis-turnos/<int:turno_id>/cancelar", methods=["POST"])
def cancelar_turno_paciente(turno_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para cancelar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        turno_service.cancelar_turno(token, turno_id)
        flash("Turno cancelado exitosamente.", "success")
    except RuntimeError as error:
        flash(str(error), "error")

    return redirect(url_for("patient.mis_turnos"))


@patient_bp.route("/reservar-turno", methods=["GET"])
def reservar_especialidad():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        especialidades = turno_service.listar_especialidades(token)
    except RuntimeError as error:
        flash(str(error), "error")
        especialidades = []

    return render_template(
        "pacientes/reserva/especialidad.html",
        especialidades=especialidades
    )


@patient_bp.route(
    "/reservar-turno/especialidades/<int:especialidad_id>/medicos",
    methods=["GET"]
)
def reservar_medico(especialidad_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        medicos = turno_service.listar_medicos(token, especialidad_id=especialidad_id)
    except RuntimeError as error:
        flash(str(error), "error")
        medicos = []

    return render_template(
        "pacientes/reserva/medico.html",
        especialidad_id=especialidad_id,
        medicos=medicos
    )


@patient_bp.route(
    "/reservar-turno/medicos/<int:medico_id>/fecha-hora",
    methods=["GET"]
)
def reservar_fecha_hora(medico_id: int):
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    try:
        medico = turno_service.obtener_medico(token, medico_id)
        turnos_disponibles_raw = turno_service.obtener_turnos_disponibles(token, medico_id)
    except RuntimeError as error:
        flash(str(error), "error")
        medico = {}
        turnos_disponibles_raw = []

    fechas_dict = {}
    turnos_lista = []

    for t in turnos_disponibles_raw:
        fecha_hora_str = t.get("fecha_hora")
        if not fecha_hora_str:
            continue
        try:
            dt = datetime.fromisoformat(fecha_hora_str)
        except ValueError:
            continue

        fecha_val = dt.strftime("%Y-%m-%d")
        hora_val = dt.strftime("%H:%M")
        dia_semana_nombre = DIAS_SEMANA.get(dt.weekday(), "")[:3]

        if fecha_val not in fechas_dict:
            fechas_dict[fecha_val] = {
                "valor": fecha_val,
                "dia": dia_semana_nombre,
                "num": dt.day,
                "libres": 0
            }
        fechas_dict[fecha_val]["libres"] += 1

        turnos_lista.append({
            "id": t.get("id"),
            "fecha": fecha_val,
            "hora": hora_val,
            "consultorio": f"Consultorio {t.get('consultorio_sala', '')}"
        })

    fechas = list(fechas_dict.values())

    return render_template(
        "pacientes/reserva/fecha_hora.html",
        medico_id=medico_id,
        medico=medico,
        fechas=fechas,
        turnos_lista=turnos_lista
    )


@patient_bp.route("/reservar-turno/confirmacion", methods=["GET"])
def reservar_confirmacion():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para confirmar tu turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    medico_id = request.args.get("medico_id", type=int)
    turno_id = request.args.get("turno_id", type=int)
    fecha = request.args.get("fecha")
    hora = request.args.get("hora")

    medico = {}
    if medico_id:
        try:
            medico = turno_service.obtener_medico(token, medico_id)
        except RuntimeError:
            pass

    fecha_formateada = None
    if fecha:
        try:
            dt = datetime.fromisoformat(fecha)
            dia_nombre = DIAS_SEMANA.get(dt.weekday(), "")
            mes_nombre = MESES.get(dt.month, "")
            fecha_formateada = f"{dia_nombre} {dt.day} de {mes_nombre}"
        except Exception:
            pass

    return render_template(
        "pacientes/reserva/confirmacion.html",
        medico_id=medico_id,
        turno_id=turno_id,
        medico=medico,
        fecha=fecha,
        fecha_formateada=fecha_formateada,
        hora=hora
    )


@patient_bp.route("/reservar-turno/resultado", methods=["GET", "POST"])
def reservar_resultado():
    token = session.get("access_token")
    if not token:
        flash("Debés iniciar sesión para reservar un turno.", "error")
        return redirect(url_for("auth.mostrar_login"))

    turno_id_raw = request.form.get("turno_id") or request.args.get("turno_id")

    if request.method == "POST" and turno_id_raw:
        try:
            turno_id = int(turno_id_raw)
            turno_service.reservar_turno(token, turno_id)
            flash("Turno reservado exitosamente.", "success")
            return redirect(url_for("patient.mis_turnos"))
        except (ValueError, RuntimeError) as error:
            flash(str(error), "error")
            medico_id = request.form.get("medico_id")
            if medico_id:
                return redirect(url_for("patient.reservar_fecha_hora", medico_id=medico_id))
            return redirect(url_for("patient.reservar_especialidad"))

    return render_template(
        "pacientes/reserva/confirmacion.html",
        resultado=True
    )
