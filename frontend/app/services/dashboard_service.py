from app.clients.api_client import api_request


def obtener_turnos_hoy() -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/turnos-hoy",
        authenticated=True
    )

    return resultado.get("data") or {}