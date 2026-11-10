from flask import render_template

from app.routes.patient import patient_bp


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