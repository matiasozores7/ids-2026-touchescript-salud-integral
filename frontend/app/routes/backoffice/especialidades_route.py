
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.services import especialidades_service
from app.errors.exceptions import ExternalServiceError

from . import backoffice_bp


def _render_especialidades():
    try:
        resultado = especialidades_service.listar_especialidades()
        especialidades = resultado["items"]
        total = resultado.get("total", len(especialidades))

    except ExternalServiceError as exception:
        especialidades = []
        total = 0
        flash(str(exception), "error")

    return render_template(
        "backoffice/specialties.html",
        especialidades=especialidades,
        total=total
    )


@backoffice_bp.route("/backoffice/especialidades", methods=["GET", "POST"])
def backoffice_specialties():
    if request.method == "GET":
        return _render_especialidades()

    try:
        especialidades_service.crear_especialidad(
            nombre=request.form.get("name", "").strip(),
            descripcion=request.form.get("description", "").strip() or None
        )
        flash("Especialidad creada correctamente.", "success")

    except ExternalServiceError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_specialties"))


@backoffice_bp.post("/backoffice/especialidades/<int:especialidad_id>/editar")
def actualizar_especialidad(especialidad_id):
    try:
        especialidades_service.actualizar_especialidad(
            especialidad_id=especialidad_id,
            nombre=request.form.get("name", "").strip(),
            descripcion=request.form.get("description", "").strip() or None
        )
        flash("Especialidad actualizada correctamente.", "success")

    except ExternalServiceError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_specialties"))


@backoffice_bp.post("/backoffice/especialidades/<int:especialidad_id>/eliminar")
def eliminar_especialidad(especialidad_id):
    try:
        especialidades_service.eliminar_especialidad(especialidad_id)
        flash("Especialidad eliminada correctamente.", "success")

    except ExternalServiceError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_specialties"))
