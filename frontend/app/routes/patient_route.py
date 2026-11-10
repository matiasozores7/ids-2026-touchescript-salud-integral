
from flask import Blueprint, render_template

patient_bp = Blueprint("patient", __name__)


@patient_bp.route("/pacientes", methods=["GET", "POST"])
def patient_home():
    return render_template("pacientes/home.html")


@patient_bp.route("/mis-turnos", methods=["GET"])
def mis_turnos():
    return render_template("pacientes/mis_turnos.html")


@patient_bp.route("/mis-turnos/<int:turno_id>", methods=["GET"])
def detalle_turno(turno_id):
    return render_template(
        "pacientes/detalle_turno.html",
        turno_id=turno_id
    )


@patient_bp.route("/qr/<int:turno_id>", methods=["GET"])
def qr_turno(turno_id):
    return render_template(
        "pacientes/qr_turno.html",
        turno_id=turno_id
    )


@patient_bp.route("/reservar-turno", methods=["GET"])
def reservar_especialidad():
    return render_template("pacientes/reserva/especialidad.html")


@patient_bp.route(
    "/reservar-turno/especialidades/<int:especialidad_id>/medicos",
    methods=["GET"]
)
def reservar_medico(especialidad_id):
    return render_template(
        "pacientes/reserva/medico.html",
        especialidad_id=especialidad_id
    )


@patient_bp.route(
    "/reservar-turno/medicos/<int:medico_id>/fecha-hora",
    methods=["GET"]
)
def reservar_fecha_hora(medico_id):
    return render_template(
        "pacientes/reserva/fecha_hora.html",
        medico_id=medico_id
    )


@patient_bp.route("/reservar-turno/confirmacion", methods=["GET"])
def reservar_confirmacion():
    return render_template("pacientes/reserva/confirmacion.html")


@patient_bp.route("/reservar-turno/resultado", methods=["GET", "POST"])
def reservar_resultado():
    return render_template(
        "pacientes/reserva/confirmacion.html",
        resultado=True
    )
