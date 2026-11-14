from flask import flash, redirect, render_template, request, url_for

from app.errors.exceptions import AppError
from app.services.coberturas_service import listar_coberturas, crear_cobertura, actualizar_cobertura, eliminar_cobertura
from app.routes.backoffice import backoffice_bp


@backoffice_bp.route("/coberturas")
def backoffice_coberturas():
    limit = request.args.get("_limit", 10, type=int)
    offset = request.args.get("_offset", 0, type=int)

    resultado = listar_coberturas(limit, offset)

    return render_template(
        "backoffice/coberturas.html",
        coberturas=resultado["items"],
        total=resultado["total"],
        links=resultado["_links"]
    )


@backoffice_bp.post("/coberturas/nueva")
def crear_cobertura_frontend():
    nombre = request.form.get("nombre", "").strip()

    if not nombre:
        flash("El nombre de la cobertura es obligatorio.", "error")
        return redirect(url_for("backoffice.backoffice_coberturas"))

    try:
        crear_cobertura(nombre)
    except AppError as error:
        flash(error.message, "error")
    else:
        flash("Cobertura creada correctamente.", "success")

    return redirect(url_for("backoffice.backoffice_coberturas"))


@backoffice_bp.post("/coberturas/<int:cobertura_id>/editar")
def editar_cobertura_frontend(cobertura_id: int):
    nombre = request.form.get("nombre", "").strip()

    if not nombre:
        flash("El nombre de la cobertura es obligatorio.", "error")
        return redirect(url_for("backoffice.backoffice_coberturas"))

    try:
        actualizar_cobertura(cobertura_id, nombre)
    except AppError as error:
        flash(error.message, "error")
    else:
        flash("Cobertura actualizada correctamente.", "success")

    return redirect(url_for("backoffice.backoffice_coberturas"))

@backoffice_bp.post("/coberturas/<int:cobertura_id>/eliminar")
def eliminar_cobertura_frontend(cobertura_id: int):
    try:
        eliminar_cobertura(cobertura_id)
    except AppError as error:
        flash(error.message, "error")
    else:
        flash("Cobertura eliminada correctamente.", "success")

    return redirect(url_for("backoffice.backoffice_coberturas"))