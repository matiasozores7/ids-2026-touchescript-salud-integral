from functools import wraps
from flask_jwt_extended import get_jwt
from src.errors.exceptions import ForbiddenError


def roles_requeridos(*roles_permitidos):

    def decorador(funcion):

        @wraps(funcion)
        def funcion_decorada(*args, **kwargs):

            claims = get_jwt()
            rol_usuario = claims.get("rol")

            if rol_usuario not in roles_permitidos:
                raise ForbiddenError(
                    description="Tu rol no está autorizado para acceder a este recurso."
                )

            return funcion(*args, **kwargs)

        return funcion_decorada

    return decorador