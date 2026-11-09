from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError
from app.constants.roles import ROLES_VALIDOS

def obtener_usuario_actual() -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/auth/me",
        authenticated=True
    )

    data = resultado.get("data")

    if (
        not isinstance(data, dict)
        or data.get("rol") not in ROLES_VALIDOS
    ):
        raise ExternalServiceError(
            "La respuesta de autenticación tiene un formato inválido."
        )

    return data

def login_usuario(email: str, password: str) -> dict:

    resultado = api_request(
        method="POST",
        endpoint="/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    data = resultado.get("data")

    if (not isinstance(data, dict) or not isinstance(data.get("access_token"), str)
        or not data["access_token"]
    ):
        raise ExternalServiceError("La respuesta de autenticación tiene un formato inválido.")

    return data

def registrar_paciente(
    nombre: str, apellido: str, email: str,
    password: str, cobertura_id: int | None = None
) -> dict:

    resultado = api_request(
        method="POST",
        endpoint="/auth/registro",
        json={
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "password": password,
            "cobertura_id": cobertura_id
        }
    )

    data = resultado.get("data")

    if (
        not isinstance(data, dict)
        or not isinstance(data.get("access_token"), str)
        or not data["access_token"]
    ):
        raise ExternalServiceError(
            "La respuesta de registro tiene un formato inválido."
        )

    return data