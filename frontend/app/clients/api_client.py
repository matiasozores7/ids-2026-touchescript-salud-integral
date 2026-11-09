import requests

from flask import current_app, session

from app.errors.exceptions import (
    AppError,
    ValidationError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ExternalServiceError,
    ServiceUnavailableError,
    ServiceTimeoutError
)


HTTP_ERRORS = {
    400: ValidationError,
    401: AuthenticationError,
    403: ForbiddenError,
    404: NotFoundError,
    409: ConflictError,
    502: ExternalServiceError,
    503: ServiceUnavailableError,
    504: ServiceTimeoutError
}


def api_request(
    method: str,
    endpoint: str,
    *,
    json: dict | None = None,
    params: dict | None = None,
    authenticated: bool = False
) -> dict:

    base_url = current_app.config["API_BASE_URL"].rstrip("/")
    url = f"{base_url}/{endpoint.lstrip('/')}"

    headers = {}

    if authenticated:
        token = session.get("access_token")

        if not token:
            raise AuthenticationError()

        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.request(
            method=method,
            url=url,
            json=json,
            params=params,
            headers=headers,
            timeout=10
        )

    except requests.Timeout:
        raise ServiceTimeoutError()

    except requests.ConnectionError:
        raise ServiceUnavailableError()

    except requests.RequestException:
        raise ExternalServiceError()

    try:
        resultado = response.json()
    except ValueError:
        raise ExternalServiceError(
            "El servidor devolvió una respuesta inválida."
        )

    if not isinstance(resultado, dict):
        raise ExternalServiceError(
            "El formato de respuesta del servidor es inválido."
        )

    if not response.ok:
        errors = resultado.get("errors", [])

        mensaje = "No se pudo completar la operación."

        if errors and isinstance(errors[0], dict):
            mensaje = (
                errors[0].get("description")
                or errors[0].get("message")
                or mensaje
            )

        exception_class = HTTP_ERRORS.get(
            response.status_code,
            ExternalServiceError
        )

        raise exception_class(mensaje)

    return resultado