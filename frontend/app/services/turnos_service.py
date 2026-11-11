from datetime import datetime

from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo",
}

MESES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def _formatear_turno(turno: dict) -> dict:
    fecha_hora = datetime.fromisoformat(turno["fecha_hora"])

    medico_nombre = turno.get("medico_nombre") or ""
    medico_apellido = turno.get("medico_apellido") or ""

    medico = (
        f"Dr. {medico_nombre} {medico_apellido}".strip()
        if medico_nombre or medico_apellido
        else "Profesional asignado"
    )

    iniciales = (
        f"{medico_nombre[:1]}{medico_apellido[:1]}".upper()
        if medico_nombre and medico_apellido
        else "MD"
    )

    dia = DIAS_SEMANA[fecha_hora.weekday()]
    mes = MESES[fecha_hora.month]

    return {
        **turno,
        "dia": dia,
        "hora": fecha_hora.strftime("%H:%M"),
        "fecha": f"{dia.lower()} {fecha_hora.day} de {mes}",
        "iniciales": iniciales,
        "medico": medico,
    }


def listar_mis_turnos() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/turnos/mis-turnos",
        params={"limit": 100, "offset": 0},
        authenticated=True,
    )

    data = resultado.get("data") or {}
    items = data.get("items", [])

    return [_formatear_turno(turno) for turno in items]

def listar_especialidades() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/especialidades",
        params={"limit": 100, "offset": 0},
        authenticated=True,
    )

    data = resultado.get("data") or {}
    return data.get("items", [])


def listar_medicos(especialidad_id: int | None = None) -> list[dict]:
    params = {
        "limit": 100,
        "offset": 0,
    }

    if especialidad_id is not None:
        params["especialidad_id"] = especialidad_id

    resultado = api_request(
        method="GET",
        endpoint="/medicos",
        params=params,
        authenticated=True,
    )

    data = resultado.get("data") or {}
    return data.get("items", [])


def obtener_medico(medico_id: int) -> dict:
    resultado = api_request(
        method="GET",
        endpoint=f"/medicos/{medico_id}",
        authenticated=True,
    )

    return resultado.get("data") or {}


def listar_turnos_disponibles(medico_id: int) -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint=f"/medicos/{medico_id}/turnos-disponibles",
        authenticated=True,
    )

    return resultado.get("data") or []


def reservar_turno(turno_id: int) -> dict:
    resultado = api_request(
        method="POST",
        endpoint="/turnos",
        json={"turno_id": turno_id},
        authenticated=True,
    )

    return resultado.get("data") or {}

def obtener_detalle_turno(turno_id: int) -> dict:
    resultado = api_request(
        method="GET",
        endpoint=f"/turnos/mis-turnos/{turno_id}",
        authenticated=True
    )

    return resultado.get("data") or {}

def cancelar_turno(turno_id: int) -> None:
    api_request(
        method="PATCH",
        endpoint=f"/turnos/{turno_id}/cancelar",
        authenticated=True
    )

def obtener_qr_turno(turno_id: int) -> str:
    resultado = api_request(
        method="GET",
        endpoint=f"/turnos/{turno_id}/qr",
        authenticated=True,
    )

    data = resultado.get("data") or {}
    qr_token = data.get("qr_token")

    if not qr_token:
        raise ExternalServiceError(
            "No se pudo obtener el código QR del turno."
        )

    return qr_token