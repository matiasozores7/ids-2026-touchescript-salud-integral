
from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def listar_medicos(especialidad_id: int | None = None) -> dict:
    params = {
        "_limit": 100,
        "_offset": 0
    }

    if especialidad_id is not None:
        params["especialidad_id"] = especialidad_id

    resultado = api_request(
        method="GET",
        endpoint="/medicos",
        params=params,
        authenticated=True
    )

    data = resultado.get("data")

    if (
        not isinstance(data, dict)
        or not isinstance(data.get("items"), list)
    ):
        raise ExternalServiceError(
            "La respuesta de médicos tiene un formato inválido."
        )

    return data


def crear_medico(datos: dict) -> None:
    api_request(
        method="POST",
        endpoint="/medicos",
        json=datos,
        authenticated=True
    )


def actualizar_medico(medico_id: int, datos: dict) -> None:
    api_request(
        method="PATCH",
        endpoint=f"/medicos/{medico_id}",
        json=datos,
        authenticated=True
    )


def eliminar_medico(medico_id: int) -> None:
    api_request(
        method="DELETE",
        endpoint=f"/medicos/{medico_id}",
        authenticated=True
    )
