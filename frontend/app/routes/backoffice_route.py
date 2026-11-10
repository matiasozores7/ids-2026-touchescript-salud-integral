from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests

from app.services import backoffice_service

backoffice_bp = Blueprint("backoffice", __name__)

BACKEND_URL = "http://localhost:5000/api"


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
        "backoffice/specialties.html", especialidades=especialidades, total=total
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
                descripcion=request.form.get("description", "").strip() or None,
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
            descripcion=request.form.get("description", "").strip() or None,
        )
        flash("Especialidad actualizada correctamente.", "success")
    except RuntimeError as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.backoffice_specialties"))


@backoffice_bp.post("/backoffice/especialidades/<int:especialidad_id>/eliminar")
def eliminar_especialidad(especialidad_id):
    try:
        backoffice_service.eliminar_especialidad(
            session.get("access_token"), especialidad_id
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
@backoffice_bp.route(
    "/backoffice/consultorios/<int:consultorio_id>/editar", methods=["GET", "POST"]
)
def backoffice_consultorio_form(consultorio_id=None):
    return render_template("backoffice/consultorio_form.html")


@backoffice_bp.get("/backoffice/check-in")
def backoffice_checkin():
    return render_template("recepcion/checkin.html")


@backoffice_bp.route("/backoffice/coberturas", methods=["GET"])
def listar_coberturas():
    """
    Renderiza el listado de coberturas médicas en el backoffice.
    Soporta filtrado por nombre y descripción a través de query params.
    """
    token = session.get("access_token")
    if not token:
        flash("Debes iniciar sesión para acceder a esta sección.", "warning")
        return redirect(url_for("backoffice.backoffice"))

    headers = {"Authorization": f"Bearer {token}"}
    buscar_q = request.args.get("buscar", "")

    try:

        response = requests.get(f"{BACKEND_URL}/coberturas", headers=headers, timeout=5)

        if response.status_code == 200:
            json_data = response.json()

            datos_api = json_data.get("data", {})
            todas_coberturas = datos_api.get("items", [])
        else:
            todas_coberturas = []
            flash("No se pudieron recuperar las coberturas del servidor.", "error")

    except requests.exceptions.RequestException:
        todas_coberturas = []
        flash("Error de comunicación con el servicio de backend.", "error")

    if buscar_q:
        coberturas_filtradas = [
            c
            for c in todas_coberturas
            if buscar_q.lower() in c.get("nombre", "").lower()
            or buscar_q.lower() in c.get("descripcion", "").lower()
        ]
    else:
        coberturas_filtradas = todas_coberturas

    return render_template(
        "backoffice/coberturas/listado.html",
        coberturas=coberturas_filtradas,
        q_buscada=buscar_q,
    )


@backoffice_bp.route("/backoffice/coberturas/nueva", methods=["GET", "POST"])
def nueva_cobertura():
    token = session.get("access_token")
    if not token:
        return redirect(url_for("backoffice.backoffice"))

    if request.method == "POST":
        payload = {
            "nombre": request.form.get("nombre"),
            "sigla": request.form.get("sigla"),
            "activo": request.form.get("estado") == "true",
        }
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.post(
                f"{BACKEND_URL}/coberturas", json=payload, headers=headers, timeout=5
            )
            if response.status_code == 201:
                flash("Cobertura creada correctamente.", "success")
                return redirect(url_for("backoffice.listar_coberturas"))
        except Exception as exception:
            flash(str(exception), "error")

    return render_template("coberturas/formulario.html", cobertura=None)


@backoffice_bp.route("/backoffice/coberturas/editar/<int:id>", methods=["GET", "POST"])
def editar_cobertura(id):
    token = session.get("access_token")
    if not token:
        return redirect(url_for("backoffice.backoffice"))

    headers = {"Authorization": f"Bearer {token}"}

    if request.method == "POST":
        payload = {
            "nombre": request.form.get("nombre"),
            "sigla": request.form.get("sigla"),
            "activo": request.form.get("estado") == "true",
        }
        try:
            response = requests.put(
                f"{BACKEND_URL}/coberturas/{id}",
                json=payload,
                headers=headers,
                timeout=5,
            )
            if response.status_code == 200:
                flash("Cobertura actualizada correctamente.", "success")
                return redirect(url_for("backoffice.listar_coberturas"))
        except Exception as exception:
            flash(str(exception), "error")

    try:
        response = requests.get(
            f"{BACKEND_URL}/coberturas/{id}", headers=headers, timeout=5
        )
        cobertura_actual = response.json() if response.status_code == 200 else None
    except Exception:
        cobertura_actual = None

    return render_template("coberturas/formulario.html", cobertura=cobertura_actual)


@backoffice_bp.post("/backoffice/coberturas/<int:id>/eliminar")
def eliminar_cobertura(id):
    token = session.get("access_token")
    if not token:
        return redirect(url_for("backoffice.backoffice"))

    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(
            f"{BACKEND_URL}/coberturas/{id}", headers=headers, timeout=5
        )
        if response.status_code == 200:
            flash("Cobertura eliminada correctamente.", "success")
    except Exception as exception:
        flash(str(exception), "error")

    return redirect(url_for("backoffice.listar_coberturas"))
