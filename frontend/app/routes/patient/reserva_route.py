from flask import render_template

from app.routes.patient import patient_bp


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