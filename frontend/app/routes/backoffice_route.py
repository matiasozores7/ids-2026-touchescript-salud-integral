from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.services import backoffice_service, turno_service

backoffice_bp = Blueprint("backoffice", __name__)


def _render_especialidades():
    try:
        resultado = backoffice_service.listar_especialidades(
            session.get("access_token")
        )
        especialidades = resultado["items"]
        total = resultado.get("total", len(especialidades))
    except RuntimeError as exception:
        especialidades = []
        total = 0
        flash(str(exception), "error")

    return render_template(
        "backoffice/specialties.html",
        especialidades=especialidades,
        total=total
    )


@backoffice_bp.route("/backoffice")
def backoffice():
    return render_template("backoffice/backoffice.html")


@backoffice_bp.route("/backoffice/especialidades", methods=["GET", "POST"])
def backoffice_specialties():
    if request.method == "GET":
        response = _render_especialidades()
    else:
        try:
            backoffice_service.crear_especialidad(
                access_token=session.get("access_token"),
                nombre=request.form.get("name", "").strip(),
                descripcion=request.form.get("description", "").strip() or None
            )
            flash("Especialidad creada correctamente.", "success")
        except RuntimeError as exception:
            flash(str(exception), "error")
        response = redirect(url_for("backoffice.backoffice_specialties"))

    return response


@backoffice_bp.post("/backoffice/especialidades/<int:especialidad_id>/editar")
def actualizar_especialidad(especialidad_id):
    try:
        backoffice_service.actualizar_especialidad(
            access_token=session.get("access_token"),
            especialidad_id=especialidad_id,
            nombre=request.form.get("name", "").strip(),
            descripcion=request.form.get("description", "").strip() or None
        )
        flash("Especialidad actualizada correctamente.", "success")
    except RuntimeError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_specialties"))


@backoffice_bp.post("/backoffice/especialidades/<int:especialidad_id>/eliminar")
def eliminar_especialidad(especialidad_id):
    try:
        backoffice_service.eliminar_especialidad(
            session.get("access_token"),
            especialidad_id
        )
        flash("Especialidad eliminada correctamente.", "success")
    except RuntimeError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_specialties"))


@backoffice_bp.get("/backoffice/medicos")
def backoffice_medicos():
    return render_template("backoffice/medicos.html")

@backoffice_bp.get("/backoffice/consultorios")
def backoffice_consultorios():
    return render_template("backoffice/consultorios.html")

@backoffice_bp.route("/backoffice/consultorios/nuevo", methods=["GET", "POST"])
@backoffice_bp.route("/backoffice/consultorios/<int:consultorio_id>/editar", methods=["GET", "POST"])
def backoffice_consultorio_form(consultorio_id=None):
    return render_template("backoffice/consultorio_form.html")

@backoffice_bp.route("/backoffice/check-in", methods=["GET", "POST"])
def backoffice_checkin():
    if request.method == "POST":
        qr_code = request.form.get("qr_code", "").strip()
        try:
            mensaje = turno_service.realizar_checkin(
                access_token=session.get("access_token"),
                qr_token=qr_code
            )
            flash(mensaje or "Check-in registrado exitosamente.", "success")
        except RuntimeError as exception:
            flash(str(exception), "error")

        return redirect(url_for("backoffice.backoffice_checkin"))

    return render_template("recepcion/checkin.html")