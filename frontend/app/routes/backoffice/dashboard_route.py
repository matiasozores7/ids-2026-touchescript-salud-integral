from flask import render_template

from . import backoffice_bp


@backoffice_bp.get("/backoffice")
def dashboard():
    return render_template("backoffice/backoffice.html")