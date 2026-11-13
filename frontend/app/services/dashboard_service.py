from app.clients.api_client import api_request


def obtener_turnos_hoy() -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/turnos-hoy",
        authenticated=True
    )

    return resultado.get("data") or {}

def obtener_sala_espera() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/sala-espera",
        authenticated=True
    )

    return resultado.get("data") or []

def obtener_ausentismo() -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/ausentismo",
        authenticated=True
    )

    return resultado.get("data") or {}

def obtener_turnos_por_hora() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/turnos-por-hora",
        authenticated=True
    )

    return resultado.get("data") or []