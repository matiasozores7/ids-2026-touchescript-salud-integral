from src.repositories.dashboard_repository import (
    obtener_pacientes_en_sala_espera,
    obtener_turnos_por_medico_y_especialidad,
    obtener_ocupacion_consultorios
)

def obtener_sala_espera_service(connection, fecha: str | None = None) -> list[dict]:
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


def obtener_turnos_por_medico_especialidad_service(connection, fecha: str | None = None) -> list[dict]:
    return obtener_turnos_por_medico_y_especialidad(connection, fecha)


def obtener_ocupacion_consultorios_service(connection, fecha: str | None = None) -> list[dict]:
    consultorios = obtener_ocupacion_consultorios(connection, fecha)

    
    for c in consultorios:
        total = c.get("total_turnos", 0)
        ocupados = c.get("turnos_ocupados", 0) or 0

        if total > 0:
            c["porcentaje_ocupacion"] = round((ocupados / total) * 100, 2)
        else:
            c["porcentaje_ocupacion"] = 0.0

    return consultorios
