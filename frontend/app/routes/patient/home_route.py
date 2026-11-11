from flask import render_template

from app.routes.patient import patient_bp


@patient_bp.route("/pacientes", methods=["GET", "POST"])
def patient_home():
    return render_template("pacientes/home.html")