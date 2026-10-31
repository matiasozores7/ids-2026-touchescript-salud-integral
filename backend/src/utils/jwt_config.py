from flask_jwt_extended import JWTManager
from flask import jsonify

from src.database.connection import transaction
from src.repositories import token_repository as token_repo


def _respuesta_error_jwt(message: str, description: str):
    return jsonify({
        "status": "error",
        "message": message,
        "description": description
    }), 401


def configurar_jwt(app):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def verificar_token_revocado(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        with transaction() as connection:
            return token_repo.esta_revocado(connection, jti)

    @jwt.revoked_token_loader
    def token_revocado(jwt_header, jwt_payload):
        return _respuesta_error_jwt(
            message="Sesión revocada.",
            description="El token utilizado ya no es válido. Iniciá sesión nuevamente."
        )

    @jwt.expired_token_loader
    def token_expirado(jwt_header, jwt_payload):
        return _respuesta_error_jwt(
            message="Sesión expirada.",
            description="El token ha expirado. Iniciá sesión nuevamente."
        )

    @jwt.invalid_token_loader
    def token_invalido(error):
        return _respuesta_error_jwt(
            message="Token inválido.",
            description="El token proporcionado no es válido."
        )

    @jwt.unauthorized_loader
    def token_ausente(error):
        return _respuesta_error_jwt(
            message="Autenticación requerida.",
            description="Debés proporcionar un token de acceso para utilizar este recurso."
        )

    @jwt.needs_fresh_token_loader
    def token_no_reciente(jwt_header, jwt_payload):
        return _respuesta_error_jwt(
            message="Se requiere una sesión reciente.",
            description="Debés autenticarte nuevamente para realizar esta operación."
        )

    return jwt