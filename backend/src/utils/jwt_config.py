from flask_jwt_extended import JWTManager
from src.repositories import token_repository as token_repo


def configurar_jwt(app):
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def verificar_token_revocado(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        return token_repo.esta_revocado(jti)

    return jwt