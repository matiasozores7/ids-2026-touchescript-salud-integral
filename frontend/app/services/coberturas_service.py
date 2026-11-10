from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def listar_coberturas() -> list:
    resultado = api_request(
        method="GET",
        endpoint="/coberturas"
    )

    data = resultado.get("data")

    if not isinstance(data, dict):
        raise ExternalServiceError(
            "La respuesta de coberturas tiene un formato inválido."
        )

    items = data.get("items")

    if not isinstance(items, list):
        raise ExternalServiceError(
            "La respuesta de coberturas tiene un formato inválido."
        )

    return items