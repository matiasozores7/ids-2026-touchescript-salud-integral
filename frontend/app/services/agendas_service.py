
from app.clients.api_client import api_request


def listar_agendas_medico(medico_id: int) -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint=f"/medicos/{medico_id}/agendas",
        authenticated=True,
    )

    return resultado.get("data") or []


def crear_agenda(datos: dict) -> dict:
    resultado = api_request(
        method="POST",
        endpoint="/agendas",
        json=datos,
        authenticated=True,
    )

    return resultado.get("data") or {}


def actualizar_agenda(agenda_id: int, datos: dict) -> None:
    api_request(
        method="PUT",
        endpoint=f"/agendas/{agenda_id}",
        json=datos,
        authenticated=True,
    )


def eliminar_agenda(agenda_id: int) -> None:
    api_request(
        method="DELETE",
        endpoint=f"/agendas/{agenda_id}",
        authenticated=True,
    )


def listar_consultorios() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/consultorios",
        params={"limit": 100, "offset": 0},
        authenticated=True,
    )

    data = resultado.get("data") or {}
    return data.get("items", [])
