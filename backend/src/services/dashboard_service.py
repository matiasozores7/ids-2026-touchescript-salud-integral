from src.database.connection import transaction
from src.repositories.dashboard_repository import (
    obtener_pacientes_en_sala_espera,
    obtener_turnos_por_medico_y_especialidad,
    obtener_ocupacion_consultorios,
    obtener_estadisticas_ausentismo,
    obtener_estadisticas_tiempo_espera,
    obtener_estadisticas_turnos_hoy,
    obtener_turnos_por_hora
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


def obtener_turnos_por_medico_especialidad_service(fecha: str | None = None) -> list[dict]:
    with transaction() as connection:
        return obtener_turnos_por_medico_y_especialidad(connection, fecha)


def obtener_ocupacion_consultorios_service(fecha: str | None = None) -> list[dict]:
    with transaction() as connection:
        consultorios = obtener_ocupacion_consultorios(connection, fecha)

    for c in consultorios:
        total = c.get("total_turnos", 0)
        ocupados = c.get("turnos_ocupados", 0) or 0

        if total > 0:
            c["porcentaje_ocupacion"] = round((ocupados / total) * 100, 2)
        else:
            c["porcentaje_ocupacion"] = 0.0

    return consultorios


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


def obtener_tiempo_espera_service(fecha: str | None = None) -> dict:
    with transaction() as connection:
        medicos_data = obtener_estadisticas_tiempo_espera(connection, fecha)

    suma_tiempos = 0.0
    total_pacientes = 0

    for m in medicos_data:
        pacientes = m.get("pacientes_evaluados", 0)
        promedio = float(m.get("tiempo_promedio_minutos") or 0.0)

        m["tiempo_espera_promedio_minutos"] = round(promedio, 1)

        suma_tiempos += (promedio * pacientes)
        total_pacientes += pacientes

    promedio_general = round(suma_tiempos / total_pacientes, 1) if total_pacientes > 0 else 0.0

    return {
        "promedio_general_minutos": promedio_general,
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