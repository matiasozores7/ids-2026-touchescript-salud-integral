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
    return render_template("pacientes/reserva/especialidad.html")


@patient_bp.route(
    "/reservar-turno/especialidades/<int:especialidad_id>/medicos",
    methods=["GET"]
)
def reservar_medico(especialidad_id: int):
    return render_template(
        "pacientes/reserva/medico.html",
        especialidad_id=especialidad_id
    )


@patient_bp.route(
    "/reservar-turno/medicos/<int:medico_id>/fecha-hora",
    methods=["GET"]
)
def reservar_fecha_hora(medico_id: int):
    return render_template(
        "pacientes/reserva/fecha_hora.html",
        medico_id=medico_id
    )


@patient_bp.route("/reservar-turno/confirmacion", methods=["GET"])
def reservar_confirmacion():
    return render_template("pacientes/reserva/confirmacion.html")


@patient_bp.route("/reservar-turno/resultado", methods=["GET", "POST"])
def reservar_resultado():
    token = session.get("access_token")
    turno_id_raw = request.form.get("turno_id") or request.args.get("turno_id")

    if request.method == "POST" and turno_id_raw and token:
        try:
            turno_id = int(turno_id_raw)
            turno_service.reservar_turno(token, turno_id)
            flash("Turno reservado exitosamente.", "success")
            return redirect(url_for("patient.mis_turnos"))
        except (ValueError, RuntimeError) as error:
            flash(str(error), "error")

    return render_template(
        "pacientes/reserva/confirmacion.html",
        resultado=True
    )
