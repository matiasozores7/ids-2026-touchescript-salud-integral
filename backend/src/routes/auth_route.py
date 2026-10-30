from flask import Blueprint, request, jsonify

from src.utils.responses import success_response
from src.validators import auth_validator
from src.services import auth_service
from src.utils.decorators import roles_requeridos
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/registro", methods=["POST"])
def registrar_usuario():
    data = request.get_json() or {}
    auth_validator.validar_registro(data)

    resultado = auth_service.registrar_paciente(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        password=data["password"],
        cobertura_id=data.get("cobertura_id")
    )

    return success_response(data=resultado, message="Usuario registrado exitosamente", status_code=201)

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    auth_validator.validar_login(data)
    resultado = auth_service.login_usuario(email=data["email"], password=data["password"])
    
    return success_response(data=resultado, message="Inicio de sesión exitoso")   


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    claims = get_jwt()
    auth_service.logout_usuario(jti=claims["jti"], exp=claims["exp"])

    return success_response(message="Sesión cerrada exitosamente")

# Endpoint para probar autenticidad y autorización por roles, a futuro eliminar este endpoint
@auth_bp.route("/auth/protegido", methods=["GET"])
@jwt_required()
@roles_requeridos("paciente")
def ruta_protegida():
    usuario_id = get_jwt_identity()
    claims = get_jwt()

    return jsonify({
        "status": "ok",
        "message": "Token válido",
        "data": {
            "usuario_id": usuario_id,
            "rol": claims.get("rol"),
            "perfil_id": claims.get("perfil_id")
        }
    }), 200