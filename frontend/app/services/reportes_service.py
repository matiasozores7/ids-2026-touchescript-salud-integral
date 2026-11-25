from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def obtener_reportes(periodo: int) -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/reportes",
        params={"period": periodo},
        authenticated=True,
    )

    data = resultado.get("data")
    if not isinstance(data, dict):
        raise ExternalServiceError(
            "La respuesta de reportes tiene un formato inválido."
        )

    return data
