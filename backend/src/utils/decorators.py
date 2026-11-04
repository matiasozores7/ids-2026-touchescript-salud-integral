from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from src.errors.exceptions import ForbiddenError


def validar_token(funcion=None):
    """
    Decorador independiente para validar el token JWT en la solicitud.
    Puede utilizarse como @validar_token o @validar_token().
    Retorna 401 Unauthorized si el token no está presente, es inválido,
    ha expirado o ha sido revocado.
    """
    def decorador(fn):
        @wraps(fn)
        def funcion_decorada(*args, **kwargs):
            verify_jwt_in_request()
            return fn(*args, **kwargs)

        return funcion_decorada

    if funcion is not None:
        return decorador(funcion)
    return decorador


def validar_rol(*roles_permitidos):
    """
    Decorador independiente para validar el rol del usuario autenticado.
    Acepta uno o varios roles como argumentos posicionales o en una lista:
    @validar_rol('admin', 'recepcionista') o @validar_rol(['admin', 'medico'])
    Garantiza que el token sea validado primero (401 si falta o es inválido)
    y lanza ForbiddenError (403) si el rol del usuario no está autorizado.
    """
    roles_limpios = []
    for rol in roles_permitidos:
        if isinstance(rol, (list, tuple, set)):
            roles_limpios.extend([str(r).strip() for r in rol])
        elif rol is not None:
            roles_limpios.append(str(rol).strip())

    def decorador(fn):
        @wraps(fn)
        def funcion_decorada(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt() or {}
            rol_usuario = claims.get("rol")

            if rol_usuario not in roles_limpios:
                raise ForbiddenError(
                    description="Tu rol no está autorizado para acceder a este recurso."
                )

            return fn(*args, **kwargs)

        return funcion_decorada

    return decorador


# Alias para máxima flexibilidad y compatibilidad con código existente
token_requerido = validar_token
roles_requeridos = validar_rol
rol_requerido = validar_rol