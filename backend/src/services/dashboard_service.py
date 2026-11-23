from src.database.connection import transaction
from src.repositories.dashboard_repository import (
    obtener_pacientes_en_sala_espera,
    obtener_estadisticas_ausentismo,
    obtener_estadisticas_turnos_hoy,
    obtener_turnos_por_hora,
    obtener_proximos_turnos,
    obtener_estadisticas_generales
)


def obtener_sala_espera_service(fecha: str | None = None) -> list[dict]:
    with transaction() as connection:
        turnos = obtener_pacientes_en_sala_espera(connection, fecha)

    for turno in turnos:
        if turno.get("fecha_hora_turno") and turno.get("fecha_hora_llegada"):
            diferencia = turno["fecha_hora_turno"] - turno["fecha_hora_llegada"]
            minutos = int(diferencia.total_seconds() / 60)

            if minutos > 0:
                turno["puntualidad"] = f"Llegó {minutos} min antes"
            elif minutos < 0:
                turno["puntualidad"] = f"Llegó {abs(minutos)} min tarde"
            else:
                turno["puntualidad"] = "Llegó puntual"

    return turnos

def obtener_ausentismo_service(fecha: str | None = None) -> dict:
    with transaction() as connection:
        medicos_data = obtener_estadisticas_ausentismo(connection, fecha)

    total_general = 0
    ausentes_general = 0
    asistieron_general = 0
    cancelados_general = 0

    for m in medicos_data:
        agendados = m.get("turnos_agendados", 0)
        ausentes = m.get("ausentes", 0) or 0
        asistieron = m.get("asistieron", 0) or 0
        cancelados = m.get("cancelados", 0) or 0

        if agendados > 0:
            m["porcentaje_ausentismo"] = round((ausentes / agendados) * 100, 2)
        else:
            m["porcentaje_ausentismo"] = 0.0

        total_general += agendados
        ausentes_general += ausentes
        asistieron_general += asistieron
        cancelados_general += cancelados

    porcentaje_general = round((ausentes_general / total_general) * 100, 2) if total_general > 0 else 0.0

    return {
        "resumen_general": {
            "total_turnos_agendados": total_general,
            "asistieron": asistieron_general,
            "ausentes": ausentes_general,
            "cancelados": cancelados_general,
            "porcentaje_ausentismo": porcentaje_general
        },
        "por_medico": medicos_data
    }

def obtener_turnos_hoy_service() -> dict:
    with transaction() as connection:
        return obtener_estadisticas_turnos_hoy(connection)

def obtener_turnos_por_hora_service() -> list[dict]:
    with transaction() as connection:
        resultados = obtener_turnos_por_hora(connection)

    turnos_por_hora = {
        resultado["hora"]: resultado["total"]
        for resultado in resultados
    }

    return [
        {
            "hora": f"{hora:02d}:00",
            "total": turnos_por_hora.get(hora, 0)
        }
        for hora in range(8, 19)
    ]

def obtener_proximos_turnos_service(limite: int = 3) -> list[dict]:
    with transaction() as connection:
        return obtener_proximos_turnos(connection, limite)

def obtener_estadisticas_generales_service() -> dict:
    with transaction() as connection:
        return obtener_estadisticas_generales(connection)