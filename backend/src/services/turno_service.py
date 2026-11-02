from datetime import date, datetime, time, timedelta

from src.constants_turnos import (
    DIAS_SEMANA_MAPA,
    ESTADO_DISPONIBLE,
    TRANSICIONES_VALIDAS,
)
from src.database.connection import transaction
from src.errors.exceptions import ConflictError, NotFoundError
from src.repositories import turno_repository as turno_repo


def _serializar_valor(valor):
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, time):
        return valor.strftime("%H:%M:%S")
    if isinstance(valor, timedelta):
        segundos = int(valor.total_seconds())
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segs = segundos % 60
        return f"{horas:02d}:{minutos:02d}:{segs:02d}"
    return valor


def _serializar_turno(turno: dict | None) -> dict | None:
    if turno is None:
        return None
    return {clave: _serializar_valor(valor) for clave, valor in turno.items()}


def actualizar_estado(turno_id: int, nuevo_estado: str) -> dict:
    with transaction() as connection:
        turno = turno_repo.obtener_turno_por_id(connection, turno_id)
        if turno is None:
            raise NotFoundError(description="No se encontró el turno especificado.")

        estado_actual = turno["estado"]

        if estado_actual == nuevo_estado:
            return _serializar_turno(turno)

        transiciones_permitidas = TRANSICIONES_VALIDAS.get(estado_actual, set())
        if nuevo_estado not in transiciones_permitidas:
            raise ConflictError(
                description=(
                    f"No es posible cambiar el estado del turno de '{estado_actual}' a "
                    f"'{nuevo_estado}'. Transición no permitida."
                )
            )

        turno_repo.actualizar_estado_turno(connection, turno_id, nuevo_estado)
        actualizado = turno_repo.obtener_turno_por_id(connection, turno_id)

    return _serializar_turno(actualizado)


def _time_a_segundos(valor_time) -> int:
    if isinstance(valor_time, timedelta):
        return int(valor_time.total_seconds())
    if isinstance(valor_time, time):
        return valor_time.hour * 3600 + valor_time.minute * 60 + valor_time.second
    if isinstance(valor_time, str):
        partes = [int(p) for p in valor_time.split(":")]
        if len(partes) == 3:
            return partes[0] * 3600 + partes[1] * 60 + partes[2]
        if len(partes) == 2:
            return partes[0] * 3600 + partes[1] * 60
    return 0


def _segundos_a_time(segundos: int) -> time:
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    return time(hour=horas, minute=minutos, second=segs)


def generar_turnos(fecha_inicio_str: str, fecha_fin_str: str, medico_id: int | None = None) -> int:
    fecha_inicio = datetime.strptime(fecha_inicio_str.strip(), "%Y-%m-%d").date()
    fecha_fin = datetime.strptime(fecha_fin_str.strip(), "%Y-%m-%d").date()

    turnos_creados = 0

    with transaction() as connection:
        agendas = turno_repo.obtener_agendas_para_generacion(connection, medico_id)
        if not agendas:
            return 0

        dias_total = (fecha_fin - fecha_inicio).days + 1

        for i in range(dias_total):
            dia_actual = fecha_inicio + timedelta(days=i)
            dia_semana_nombre = DIAS_SEMANA_MAPA.get(dia_actual.weekday())

            agendas_dia = [a for a in agendas if a["dia_semana"] == dia_semana_nombre]

            for agenda in agendas_dia:
                segundos_inicio = _time_a_segundos(agenda["hora_inicio"])
                segundos_fin = _time_a_segundos(agenda["hora_fin"])
                duracion_segundos = agenda["duracion_turno"] * 60

                if duracion_segundos <= 0:
                    continue

                actual_segundos = segundos_inicio
                while actual_segundos + duracion_segundos <= segundos_fin:
                    hora_slot = _segundos_a_time(actual_segundos)
                    fecha_hora_slot = datetime.combine(dia_actual, hora_slot)

                    hay_conflicto = turno_repo.existe_turno_en_horario(
                        connection,
                        medico_id=agenda["medico_id"],
                        consultorio_id=agenda["consultorio_id"],
                        fecha_hora=fecha_hora_slot,
                    )

                    if not hay_conflicto:
                        turno_repo.insertar_turno(
                            connection,
                            medico_id=agenda["medico_id"],
                            consultorio_id=agenda["consultorio_id"],
                            fecha_hora=fecha_hora_slot,
                            estado=ESTADO_DISPONIBLE,
                        )
                        turnos_creados += 1

                    actual_segundos += duracion_segundos

    return turnos_creados
