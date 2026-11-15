from flask import render_template

from app.routes.backoffice import backoffice_bp


@backoffice_bp.route("/backoffice/calendario")
def backoffice_calendario():
    return render_template("backoffice/calendario.html")