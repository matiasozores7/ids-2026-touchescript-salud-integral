from app.clients.api_client import api_request
from email.utils import parsedate_to_datetime
from zoneinfo import ZoneInfo

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

def obtener_proximos_turnos() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/proximos-turnos",
        authenticated=True
    )

    turnos = resultado.get("data") or []
    zona_horaria = ZoneInfo("America/Argentina/Buenos_Aires")

    for turno in turnos:
        fecha = parsedate_to_datetime(turno["fecha_hora_turno"])
        fecha_local = fecha.astimezone(zona_horaria)

        turno["hora"] = fecha_local.strftime("%H:%M")
        turno["fecha"] = fecha_local.strftime("%d/%m")

    return turnos

def obtener_estadisticas_generales() -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/dashboard/estadisticas-generales",
        authenticated=True
    )

    return resultado.get("data") or {}