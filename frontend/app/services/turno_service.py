from datetime import datetime
import requests
from flask import current_app

DIAS_SEMANA = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
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
    12: "diciembre"
}


def _headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


def _obtener_error(response) -> str:
    try:
        resultado = response.json()
    except ValueError:
        return "El servidor devolvió una respuesta inválida."

    if not isinstance(resultado, dict):
        return "No se pudo completar la operación."

    errores = resultado.get("errors", [])
    if errores and isinstance(errores[0], dict):
        return errores[0].get(
            "description",
            errores[0].get("message", "No se pudo completar la operación.")
        )

    return resultado.get("message", "No se pudo completar la operación.")


def _solicitar(metodo: str, ruta: str, access_token: str, **kwargs) -> dict:
    if not access_token:
        raise RuntimeError("No se encuentra una sesión activa.")

    url = f"{current_app.config['API_BASE_URL']}{ruta}"

    try:
        response = requests.request(
            metodo,
            url,
            headers=_headers(access_token),
            timeout=10,
            **kwargs
        )
    except requests.Timeout:
        raise RuntimeError("El servidor de turnos no respondió a tiempo.")
    except requests.RequestException:
        raise RuntimeError("No se pudo conectar con el servidor.")

    if not response.ok:
        raise RuntimeError(_obtener_error(response))

    try:
        resultado = response.json()
    except ValueError:
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    if not isinstance(resultado, dict):
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    return resultado


def _formatear_turno(t: dict) -> dict:
    fecha_hora_raw = t.get("fecha_hora")
    dt = None
    if isinstance(fecha_hora_raw, str):
        try:
            dt = datetime.fromisoformat(fecha_hora_raw)
        except ValueError:
            pass
    elif isinstance(fecha_hora_raw, datetime):
        dt = fecha_hora_raw

    dia_nombre = DIAS_SEMANA.get(dt.weekday(), "") if dt else ""
    mes_nombre = MESES.get(dt.month, "") if dt else ""
    fecha_formateada = f"{dia_nombre.lower()} {dt.day} de {mes_nombre}" if dt else ""
    fecha_larga = f"{dia_nombre} {dt.day} de {mes_nombre}" if dt else ""
    hora_formateada = dt.strftime("%H:%M") if dt else ""

    med_nom = t.get("medico_nombre") or ""
    med_ape = t.get("medico_apellido") or ""
    medico_completo = f"Dr. {med_nom} {med_ape}".strip() if med_nom or med_ape else "Profesional asignado"
    iniciales = f"{med_nom[:1]}{med_ape[:1]}".upper() if med_nom and med_ape else "MD"

    sala = t.get("consultorio_sala") or ""
    piso = t.get("consultorio_piso") or ""
    consultorio_str = f"Consultorio {sala}" + (f" · Piso {piso}" if piso else "")

    llegada_raw = t.get("fecha_hora_llegada")
    llegada_str = None
    if llegada_raw:
        try:
            dt_llegada = datetime.fromisoformat(llegada_raw) if isinstance(llegada_raw, str) else llegada_raw
            llegada_str = f"{dt_llegada.strftime('%H:%M')} h"
        except Exception:
            llegada_str = str(llegada_raw)

    pac_nom = t.get("paciente_nombre") or ""
    pac_ape = t.get("paciente_apellido") or ""
    paciente_completo = f"{pac_nom} {pac_ape}".strip() if pac_nom or pac_ape else "Paciente"

    return {
        "id": t.get("id"),
        "codigo": f"SI-{t.get('id')}",
        "dia": dia_nombre,
        "hora": hora_formateada,
        "fecha": fecha_formateada,
        "fecha_larga": fecha_larga,
        "iniciales": iniciales,
        "medico": medico_completo,
        "medico_nombre": med_nom,
        "medico_apellido": med_ape,
        "paciente": paciente_completo,
        "especialidad": t.get("especialidad_nombre") or "Clínica Médica",
        "consultorio": consultorio_str,
        "cobertura": t.get("cobertura_nombre") or "Particular",
        "indicaciones": "Llegá 15 min antes con tu comprobante o QR",
        "llegada": llegada_str,
        "estado": t.get("estado", "disponible"),
        "qr_token": t.get("qr_token"),
        "duracion": "30 min"
    }


def listar_mis_turnos(access_token: str, estado: str | None = None) -> list[dict]:
    ruta = "/turnos/mis-turnos?_limit=100&_offset=0"
    if estado:
        ruta += f"&estado={estado}"

    resultado = _solicitar("GET", ruta, access_token)
    data = resultado.get("data", {})
    items = data.get("items", []) if isinstance(data, dict) else []

    return [_formatear_turno(t) for t in items]


def obtener_detalle_turno(access_token: str, turno_id: int) -> dict:
    turnos = listar_mis_turnos(access_token)
    for t in turnos:
        if t["id"] == turno_id:
            return t

    raise RuntimeError("No se encontró el turno especificado o no pertenece a tu cuenta.")


def obtener_qr_turno(access_token: str, turno_id: int) -> dict:
    resultado = _solicitar("GET", f"/turnos/{turno_id}/qr", access_token)
    data = resultado.get("data", {})
    if not isinstance(data, dict) or not data.get("qr_token"):
        raise RuntimeError("El turno todavía no tiene un código QR generado.")

    return data


def cancelar_turno(access_token: str, turno_id: int) -> None:
    _solicitar("PATCH", f"/turnos/{turno_id}/cancelar", access_token)


def realizar_checkin(access_token: str, qr_token: str) -> str:
    if not qr_token:
        raise RuntimeError("Debe ingresar un código QR válido.")

    resultado = _solicitar(
        "POST",
        "/turnos/checkin",
        access_token,
        json={"qr_token": qr_token.strip()}
    )
    return resultado.get("message", "Check-in registrado exitosamente.")


def reservar_turno(access_token: str, turno_id: int) -> dict:
    resultado = _solicitar(
        "POST",
        "/turnos",
        access_token,
        json={"turno_id": turno_id}
    )
    return resultado.get("data", {})


def obtener_dias_disponibles(access_token: str, medico_id: int) -> list:
    resultado = _solicitar(
        "GET",
        f"/medicos/{medico_id}/dias-disponibles",
        access_token
    )
    return resultado.get("data", [])


def obtener_horarios_disponibles(access_token: str, medico_id: int, fecha: str) -> list:
    resultado = _solicitar(
        "GET",
        f"/medicos/{medico_id}/horarios-disponibles?fecha={fecha}",
        access_token
    )
    return resultado.get("data", [])


def listar_especialidades(access_token: str) -> list[dict]:
    resultado = _solicitar(
        "GET",
        "/especialidades?_limit=100&_offset=0",
        access_token
    )
    data = resultado.get("data", {})
    return data.get("items", []) if isinstance(data, dict) else []


def listar_medicos(access_token: str, especialidad_id: int | None = None) -> list[dict]:
    ruta = "/medicos?_limit=100&_offset=0"
    if especialidad_id:
        ruta += f"&especialidad_id={especialidad_id}"

    resultado = _solicitar("GET", ruta, access_token)
    data = resultado.get("data", {})
    return data.get("items", []) if isinstance(data, dict) else []


def obtener_medico(access_token: str, medico_id: int) -> dict:
    resultado = _solicitar("GET", f"/medicos/{medico_id}", access_token)
    return resultado.get("data", {})


def obtener_turnos_disponibles(access_token: str, medico_id: int, fecha: str | None = None) -> list[dict]:
    ruta = f"/medicos/{medico_id}/turnos-disponibles"
    if fecha:
        ruta += f"?fecha={fecha}"

    resultado = _solicitar("GET", ruta, access_token)
    return resultado.get("data", [])
