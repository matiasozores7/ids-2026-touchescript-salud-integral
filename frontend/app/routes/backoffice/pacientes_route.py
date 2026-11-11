
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from app.services import pacientes_service, coberturas_service
from app.errors.exceptions import AppError
from . import backoffice_bp


def _render_pacientes():
    try:
        pacientes = pacientes_service.listar_pacientes()
    except AppError as error:
        flash(error.message, "error")
        pacientes = []

    try:
        coberturas = coberturas_service.listar_coberturas()
    except AppError as error:
        flash(error.message, "error")
        coberturas = []

    return render_template(
        "backoffice/pacientes.html",
        pacientes=pacientes,
        coberturas=coberturas,
    )


@backoffice_bp.route("/backoffice/pacientes", methods=["GET", "POST"])
def backoffice_pacientes():
    if request.method == "GET":
        return _render_pacientes()

    try:
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        telefono = request.form.get("telefono", "").strip() or None

        cobertura_raw = request.form.get("cobertura_id", "").strip()

        if not cobertura_raw.isdigit() or int(cobertura_raw) <= 0:
            raise ValueError("Debe seleccionar una cobertura médica válida.")

        if not password:
            raise ValueError("La contraseña es obligatoria.")

        pacientes_service.crear_paciente(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password,
            cobertura_id=int(cobertura_raw),
            telefono=telefono
        )

        flash("Paciente creado correctamente.", "success")

    except ValueError as error:
        flash(str(error), "error")
    except AppError as error:
        flash(error.message, "error")

    return redirect(url_for("backoffice.backoffice_pacientes"))


@backoffice_bp.post("/backoffice/pacientes/<int:paciente_id>/editar")
def actualizar_paciente(paciente_id: int):
    try:
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip()
        telefono = request.form.get("telefono", "").strip() or None

        cobertura_raw = request.form.get("cobertura_id", "").strip()

        if not cobertura_raw.isdigit() or int(cobertura_raw) <= 0:
            raise ValueError("Debe seleccionar una cobertura médica válida.")

        pacientes_service.actualizar_paciente(
            paciente_id=paciente_id,
            nombre=nombre,
            apellido=apellido,
            email=email,
            cobertura_id=int(cobertura_raw),
            telefono=telefono
        )

        flash("Paciente actualizado correctamente.", "success")

    except ValueError as error:
        flash(str(error), "error")
    except AppError as error:
        flash(error.message, "error")

    return redirect(url_for("backoffice.backoffice_pacientes"))


@backoffice_bp.post("/backoffice/pacientes/<int:paciente_id>/eliminar")
def eliminar_paciente(paciente_id: int):
    try:
        pacientes_service.eliminar_paciente(paciente_id)
        flash("Paciente dado de baja correctamente.", "success")

    except AppError as error:
        flash(error.message, "error")

    return redirect(url_for("backoffice.backoffice_pacientes"))
