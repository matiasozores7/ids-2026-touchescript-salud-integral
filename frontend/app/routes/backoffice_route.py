from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.services import backoffice_service

backoffice_bp = Blueprint("backoffice", __name__)

COBERTURAS_DISPONIBLES = [
    {"id": 1, "nombre": "OSDE"},
    {"id": 2, "nombre": "Swiss Medical"},
    {"id": 3, "nombre": "IOMA"},
    {"id": 4, "nombre": "Particular"}
]

COBERTURA_NOMBRE_A_ID = {
    "OSDE": 1,
    "Swiss Medical": 2,
    "IOMA": 3,
    "Particular": 4
}


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


def _render_pacientes():
    try:
        resultado = backoffice_service.listar_pacientes(
            session.get("access_token")
        )
        pacientes = resultado["items"]
        total = resultado.get("total", len(pacientes))
        for p in pacientes:
            if "cobertura_id" not in p:
                p["cobertura_id"] = COBERTURA_NOMBRE_A_ID.get(p.get("cobertura_medica"), 4)
    except RuntimeError as exception:
        pacientes = []
        total = 0
        flash(str(exception), "error")

    return render_template(
        "backoffice/pacientes.html",
        pacientes=pacientes,
        total=total,
        coberturas=COBERTURAS_DISPONIBLES
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


@backoffice_bp.route("/backoffice/pacientes", methods=["GET", "POST"])
def backoffice_pacientes():
    if request.method == "GET":
        return _render_pacientes()

    try:
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip() or "Salud1234!"
        cobertura_raw = request.form.get("cobertura_id", "").strip()
        cobertura_id = int(cobertura_raw) if cobertura_raw.isdigit() else 4

        backoffice_service.crear_paciente(
            access_token=session.get("access_token"),
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password,
            cobertura_id=cobertura_id
        )
        flash("Paciente creado correctamente.", "success")
    except RuntimeError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_pacientes"))


@backoffice_bp.post("/backoffice/pacientes/<int:paciente_id>/editar")
def actualizar_paciente(paciente_id):
    try:
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        email = request.form.get("email", "").strip()
        cobertura_raw = request.form.get("cobertura_id", "").strip()
        cobertura_id = int(cobertura_raw) if cobertura_raw.isdigit() else None

        backoffice_service.actualizar_paciente(
            access_token=session.get("access_token"),
            paciente_id=paciente_id,
            nombre=nombre,
            apellido=apellido,
            email=email,
            cobertura_id=cobertura_id
        )
        flash("Paciente actualizado correctamente.", "success")
    except RuntimeError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_pacientes"))


@backoffice_bp.post("/backoffice/pacientes/<int:paciente_id>/eliminar")
def eliminar_paciente(paciente_id):
    try:
        backoffice_service.eliminar_paciente(
            session.get("access_token"),
            paciente_id
        )
        flash("Paciente dado de baja correctamente.", "success")
    except RuntimeError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_pacientes"))


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


@backoffice_bp.get("/backoffice/check-in")
def backoffice_checkin():
    return render_template("recepcion/checkin.html")
