
from datetime import date

from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def _listar_turnos_por_estado(estado: str) -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/turnos/administracion",
        params={
            "_limit": 100,
            "_offset": 0,
            "fecha": date.today().isoformat(),
            "estado": estado
        },
        authenticated=True
    )

    data = resultado.get("data") or {}

    if (
        not isinstance(data, dict)
        or not isinstance(data.get("items"), list)
    ):
        raise ExternalServiceError(
            "La respuesta de turnos administrativos es inválida."
        )

    return data["items"]


def listar_turnos_sala_espera() -> dict:
    en_espera = _listar_turnos_por_estado("confirmado")
    en_consulta = _listar_turnos_por_estado("en_consulta")
    por_llegar = _listar_turnos_por_estado("reservado")

    en_espera.sort(
        key=lambda turno: turno.get("fecha_hora_llegada") or ""
    )

    en_consulta.sort(
        key=lambda turno: turno.get("fecha_hora_llegada") or ""
    )

    por_llegar.sort(
        key=lambda turno: turno.get("fecha_hora") or ""
    )

    return {
        "en_espera": en_espera,
        "en_consulta": en_consulta,
        "por_llegar": por_llegar
    }


def llamar_paciente(turno_id: int) -> None:
    api_request(
        method="PATCH",
        endpoint=f"/turnos/{turno_id}/estado",
        json={"estado": "en_consulta"},
        authenticated=True
    )


def finalizar_atencion(turno_id: int) -> None:
    api_request(
        method="PATCH",
        endpoint=f"/turnos/{turno_id}/estado",
        json={"estado": "atendido"},
        authenticated=True
    )
