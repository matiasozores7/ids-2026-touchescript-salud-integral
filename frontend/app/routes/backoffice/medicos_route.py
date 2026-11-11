
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from app.services import (
    medicos_service,
    especialidades_service,
    coberturas_service
)

from app.errors.exceptions import AppError

from . import backoffice_bp


def _render_medicos():
    try:
        resultado = medicos_service.listar_medicos()
        medicos = resultado["items"]

        especialidades = especialidades_service.listar_especialidades()
        coberturas = coberturas_service.listar_coberturas()

    except AppError as exception:
        medicos = []
        especialidades = {"items": []}
        coberturas = []
        flash(str(exception), "error")

    return render_template(
        "backoffice/medicos.html",
        medicos=medicos,
        especialidades=especialidades["items"],
        coberturas=coberturas
    )


@backoffice_bp.get("/backoffice/medicos")
def backoffice_medicos():
    return _render_medicos()


@backoffice_bp.post("/backoffice/medicos")
def crear_medico():
    try:
        datos = {
            "nombre": request.form.get("nombre", "").strip(),
            "apellido": request.form.get("apellido", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", ""),
            "matricula": request.form.get("matricula", "").strip(),
            "especialidad_id": request.form.get("especialidad_id", type=int),
            "telefono": request.form.get("telefono", "").strip() or None,
            "cobertura_ids": request.form.getlist("coberturas", type=int)
        }

        medicos_service.crear_medico(datos)
        flash("Médico creado correctamente.", "success")

    except AppError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_medicos"))


@backoffice_bp.post("/backoffice/medicos/<int:medico_id>/editar")
def actualizar_medico(medico_id):
    try:
        datos = {
            "nombre": request.form.get("nombre", "").strip(),
            "apellido": request.form.get("apellido", "").strip(),
            "email": request.form.get("email", "").strip(),
            "matricula": request.form.get("matricula", "").strip(),
            "especialidad_id": request.form.get("especialidad_id", type=int),
            "telefono": request.form.get("telefono", "").strip() or None,
            "cobertura_ids": request.form.getlist("coberturas", type=int)
        }

        medicos_service.actualizar_medico(medico_id, datos)
        flash("Médico actualizado correctamente.", "success")

    except AppError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_medicos"))


@backoffice_bp.post("/backoffice/medicos/<int:medico_id>/eliminar")
def eliminar_medico(medico_id):
    try:
        medicos_service.eliminar_medico(medico_id)
        flash("Médico dado de baja correctamente.", "success")

    except AppError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_medicos"))
