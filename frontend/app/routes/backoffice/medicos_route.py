from flask import render_template

from . import backoffice_bp


@backoffice_bp.get("/backoffice/medicos")
def backoffice_medicos():
    return render_template("backoffice/medicos.html")