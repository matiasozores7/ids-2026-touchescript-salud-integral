from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from app.services import auth_service

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@auth_bp.route("/login", methods=["GET"])
def mostrar_login():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def iniciar_sesion():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    try:
        resultado = auth_service.login_usuario(
            email=email,
            password=password
        )

        session["access_token"] = resultado["access_token"]

        return redirect(url_for("patient.patient_home"))

    except RuntimeError as error:
        print("LOGIN: error:", error)

        return render_template(
            "login.html",
            error=str(error)
        )

@auth_bp.route("/registro", methods=["GET"])
def mostrar_registro():
    return render_template("pacientes/register.html")


@auth_bp.route("/registro", methods=["POST"])
def registrar_paciente():
    cobertura_raw = request.form.get("cobertura_id", "").strip()

    try:
        cobertura_id = int(cobertura_raw) if cobertura_raw else None
    except ValueError:
        return render_template(
            "pacientes/register.html",
            error="La cobertura seleccionada no es válida."
        )

    try:
        resultado = auth_service.registrar_paciente(
            nombre=request.form.get("nombre", "").strip(),
            apellido=request.form.get("apellido", "").strip(),
            email=request.form.get("email", "").strip(),
            password=request.form.get("password", ""),
            cobertura_id=cobertura_id
        )

        session["access_token"] = resultado["access_token"]

        return redirect(url_for("patient.patient_home"))

    except RuntimeError as error:
        return render_template(
            "pacientes/register.html",
            error=str(error)
        )