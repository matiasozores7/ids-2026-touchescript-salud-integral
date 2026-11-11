
from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def listar_especialidades() -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/especialidades?_limit=100&_offset=0",
        authenticated=True
    )

    data = resultado.get("data")

    if (
        not isinstance(data, dict)
        or not isinstance(data.get("items"), list)
    ):
        raise ExternalServiceError(
            "La respuesta de especialidades tiene un formato inválido."
        )

    return data


def crear_especialidad(
    nombre: str,
    descripcion: str | None = None
) -> None:
    api_request(
        method="POST",
        endpoint="/especialidades",
        json={
            "nombre": nombre,
            "descripcion": descripcion
        },
        authenticated=True
    )


def actualizar_especialidad(
    especialidad_id: int,
    nombre: str,
    descripcion: str | None = None
) -> None:
    api_request(
        method="PUT",
        endpoint=f"/especialidades/{especialidad_id}",
        json={
            "nombre": nombre,
            "descripcion": descripcion
        },
        authenticated=True
    )


def eliminar_especialidad(especialidad_id: int) -> None:
    api_request(
        method="DELETE",
        endpoint=f"/especialidades/{especialidad_id}",
        authenticated=True
    )
