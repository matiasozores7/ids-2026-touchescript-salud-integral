
from flask import flash, redirect, render_template, request, url_for

from app.errors.exceptions import AppError
from app.services import consultorio_service
from app.routes.backoffice import backoffice_bp


def _render_consultorios():
    try:
        consultorios = consultorio_service.listar_consultorios()
    except AppError as error:
        flash(error.message, "error")
        consultorios = []

    return render_template(
        "backoffice/consultorios.html",
        consultorios=consultorios,
    )


@backoffice_bp.get("/consultorios")
def listar_consultorios():
    return _render_consultorios()


@backoffice_bp.route("/consultorios/nuevo", methods=["GET", "POST"])
@backoffice_bp.route(
    "/consultorios/<int:consultorio_id>/editar",
    methods=["GET", "POST"]
)
def formulario_consultorio(consultorio_id: int | None = None):
    consultorio = None

    if consultorio_id is not None:
        try:
            consultorio = consultorio_service.obtener_consultorio(
                consultorio_id
            )
        except AppError as error:
            flash(error.message, "error")
            return redirect(url_for("backoffice.listar_consultorios"))

    if request.method == "POST":
        try:
            numero_sala = request.form.get("numero_sala", "").strip()
            piso = request.form.get("piso", "").strip() or None

            if consultorio_id is None:
                consultorio_service.crear_consultorio(numero_sala, piso)
            else:
                consultorio_service.actualizar_consultorio(
                    consultorio_id,
                    numero_sala,
                    piso,
                )

        except AppError as error:
            flash(error.message, "error")
        else:
            flash("Consultorio guardado correctamente.", "success")
            return redirect(url_for("backoffice.listar_consultorios"))

    return render_template(
        "backoffice/consultorio_form.html",
        consultorio=consultorio,
    )


@backoffice_bp.post("/consultorios/<int:consultorio_id>/eliminar")
def eliminar_consultorio(consultorio_id: int):
    try:
        consultorio_service.eliminar_consultorio(consultorio_id)
    except AppError as error:
        flash(error.message, "error")
    else:
        flash("Consultorio dado de baja correctamente.", "success")

    return redirect(url_for("backoffice.listar_consultorios"))
