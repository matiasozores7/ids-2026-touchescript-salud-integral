from datetime import date, datetime, time, timedelta

from src.constants_turnos import (
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
