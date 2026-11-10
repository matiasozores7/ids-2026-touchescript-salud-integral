from flask import render_template

from . import backoffice_bp


@backoffice_bp.get("/backoffice/check-in")
def backoffice_checkin():
    return render_template("recepcion/checkin.html")