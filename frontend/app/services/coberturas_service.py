from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def listar_coberturas(limit: int = 10, offset: int = 0) -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/coberturas",
        params={
            "_limit": limit,
            "_offset": offset
        }
    )

    data = resultado.get("data")

    if not isinstance(data, dict):
        raise ExternalServiceError(
            "La respuesta de coberturas tiene un formato inválido."
        )

    items = data.get("items")
    total = data.get("total")
    links = data.get("_links")

    if (
        not isinstance(items, list)
        or not isinstance(total, int)
        or not isinstance(links, dict)
    ):
        raise ExternalServiceError(
            "La respuesta de coberturas tiene un formato inválido."
        )

    return {
        "items": items,
        "total": total,
        "_links": links
    }


def crear_cobertura(nombre: str) -> None:
    api_request(
        method="POST",
        endpoint="/coberturas",
        json={"nombre": nombre},
        authenticated=True,
    )


def actualizar_cobertura(cobertura_id: int, nombre: str) -> None:
    api_request(
        method="PUT",
        endpoint=f"/coberturas/{cobertura_id}",
        json={"nombre": nombre},
        authenticated=True,
    )


def eliminar_cobertura(cobertura_id: int) -> None:
    api_request(
        method="DELETE",
        endpoint=f"/coberturas/{cobertura_id}",
        authenticated=True,
    )
