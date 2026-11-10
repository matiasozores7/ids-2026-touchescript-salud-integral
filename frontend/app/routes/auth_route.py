from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    get_flashed_messages,
    abort
)

from app.services import auth_service, coberturas_service
from app.errors.exceptions import AppError, AuthenticationError
from app.constants.roles import PACIENTE, ADMIN

auth_bp = Blueprint("auth", __name__)

RUTAS_POR_ROL = {
    PACIENTE: "patient.patient_home",
    ADMIN: "backoffice.dashboard"
}

@auth_bp.before_request
def verificar_sesion():
    if not session.get("access_token"):
        return

    try:
        usuario = auth_service.obtener_usuario_actual()

    except AuthenticationError:
        session.clear()
        return

    endpoint = RUTAS_POR_ROL.get(usuario.get("rol"))

    if endpoint is None:
        abort(403)

    return redirect(url_for(endpoint))

@auth_bp.route("/", methods=["GET"])
def index():
    return redirect(url_for("auth.mostrar_login"))

@auth_bp.route("/login", methods=["GET"])
def mostrar_login():
    mensajes = get_flashed_messages(category_filter=["error"])
    return render_template("login.html", error=mensajes[0] if mensajes else None)


@auth_bp.route("/login", methods=["POST"])
def iniciar_sesion():
    role = request.form.get("role", "paciente")
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    # Si se seleccionó perfil de recepción o administración, ingresa directamente al Backoffice
    if role in {"recepcion", "administracion"}:
        session["role"] = role
        return redirect(url_for("backoffice.backoffice"))

    try:
        resultado = auth_service.login_usuario(email=email, password=password)
        session.clear()
        session["access_token"] = resultado["access_token"]
        return redirect(url_for("auth.mostrar_login"))

    except AppError as error:
        flash(error.message, "error")
        return redirect(url_for("auth.mostrar_login"))

@auth_bp.route("/registro", methods=["GET"])
def mostrar_registro():
    mensajes = get_flashed_messages(category_filter=["error"])

    try:
        coberturas = coberturas_service.listar_coberturas()

    except AppError:
        coberturas = []
        if not mensajes:
            mensajes = ["No se pudieron cargar las coberturas. Intentá nuevamente."]

    return render_template(
        "pacientes/register.html",
        coberturas=coberturas,
        error=mensajes[0] if mensajes else None
    )


@auth_bp.route("/registro", methods=["POST"])
def registrar_paciente():
    cobertura_id = request.form.get("cobertura_id") or None

    if cobertura_id is not None:
        try:
            cobertura_id = int(cobertura_id)
        except ValueError:
            flash("La cobertura seleccionada no es válida.", "error")
            return redirect(url_for("auth.mostrar_registro"))

    try:
        resultado = auth_service.registrar_paciente(
            nombre=request.form.get("nombre", "").strip(),
            apellido=request.form.get("apellido", "").strip(),
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", ""),
            cobertura_id=cobertura_id
        )
        session.clear()
        session["access_token"] = resultado["access_token"]

        return redirect(url_for("patient.patient_home"))

    except AppError as error:
        flash(error.message, "error")
        return redirect(url_for("auth.mostrar_registro"))
