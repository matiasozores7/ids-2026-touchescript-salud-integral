from flask import render_template

from . import backoffice_bp


@backoffice_bp.get("/backoffice/consultorios")
def backoffice_consultorios():
    return render_template("backoffice/consultorios.html")


@backoffice_bp.route("/backoffice/consultorios/nuevo", methods=["GET", "POST"])
@backoffice_bp.route(
    "/backoffice/consultorios/<int:consultorio_id>/editar",
    methods=["GET", "POST"]
)
def backoffice_consultorio_form(consultorio_id=None):
    return render_template("backoffice/consultorio_form.html")