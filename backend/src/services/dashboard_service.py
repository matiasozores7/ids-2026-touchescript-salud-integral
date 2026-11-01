from src.repositories.dashboard_repository import obtener_pacientes_en_sala_espera

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
