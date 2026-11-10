from flask import render_template

from . import backoffice_bp


@backoffice_bp.get("/backoffice/pacientes")
def backoffice_pacientes():
    return render_template("backoffice/pacientes.html")