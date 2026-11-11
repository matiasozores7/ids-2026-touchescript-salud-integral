from app.clients.api_client import api_request
from app.errors.exceptions import NotFoundError


def listar_consultorios() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/consultorios",
        params={"limit": 100, "offset": 0},
        authenticated=True,
    )
    data = resultado.get("data") or {}
    return data.get("items", [])


def obtener_consultorio(consultorio_id: int) -> dict:
    consultorio = next(
        (
            item
            for item in listar_consultorios()
            if item.get("id") == consultorio_id
        ),
        None,
    )
    if consultorio is None:
        raise NotFoundError(
            "El consultorio no existe o se encuentra inactivo."
        )
    return consultorio


def crear_consultorio(numero_sala: str, piso: str | None) -> None:
    api_request(
        method="POST",
        endpoint="/consultorios",
        json={"numero_sala": numero_sala, "piso": piso},
        authenticated=True,
    )


def actualizar_consultorio(
    consultorio_id: int,
    numero_sala: str,
    piso: str | None,
) -> None:
    api_request(
        method="PUT",
        endpoint=f"/consultorios/{consultorio_id}",
        json={"numero_sala": numero_sala, "piso": piso},
        authenticated=True,
    )


def eliminar_consultorio(consultorio_id: int) -> None:
    api_request(
        method="DELETE",
        endpoint=f"/consultorios/{consultorio_id}",
        authenticated=True,
    )
