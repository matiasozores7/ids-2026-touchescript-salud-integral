import uuid
from datetime import date, datetime, time, timedelta

from src.constants_turnos import (
    DIAS_SEMANA_MAPA,
    ESTADO_ATENDIDO,
    ESTADO_AUSENTE,
    ESTADO_CANCELADO,
    ESTADO_CONFIRMADO,
    ESTADO_DISPONIBLE,
    ESTADO_RESERVADO,
    TRANSICIONES_VALIDAS,
    VENTANA_CHECKIN_MINUTOS,
)
from src.database.connection import transaction
from src.errors.exceptions import ConflictError, ForbiddenError, NotFoundError
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


def reservar_turno(turno_id: int, paciente_id: int) -> dict:
    with transaction() as connection:
        if not turno_repo.existe_paciente(connection, paciente_id):
            raise NotFoundError(description="El paciente especificado no existe.")

        turno = turno_repo.obtener_turno_por_id(connection, turno_id)
        if turno is None:
            raise NotFoundError(description="No se encontró el turno especificado.")

        if turno["estado"] != ESTADO_DISPONIBLE:
            raise ConflictError(
                description="El turno seleccionado ya no se encuentra disponible (doble reserva evitada)."
            )

        fecha_turno = turno["fecha_hora"]
        if isinstance(fecha_turno, str):
            fecha_turno = datetime.fromisoformat(fecha_turno)

        inicio_dia = datetime.combine(fecha_turno.date(), time.min)
        fin_dia = datetime.combine(fecha_turno.date(), time.max)

        ya_tiene_turno = turno_repo.existe_reserva_paciente_con_medico_en_fecha(
            connection,
            paciente_id=paciente_id,
            medico_id=turno["medico_id"],
            fecha_inicio=inicio_dia,
            fecha_fin=fin_dia,
        )

        if ya_tiene_turno:
            raise ConflictError(
                description="El paciente ya posee un turno reservado con este médico en la misma fecha."
            )

        qr_token = f"QR-{uuid.uuid4().hex}"

        filas_afectadas = turno_repo.reservar_turno(
            connection,
            turno_id=turno_id,
            paciente_id=paciente_id,
            qr_token=qr_token,
        )

        if filas_afectadas == 0:
            raise ConflictError(
                description="No fue posible reservar el turno porque su estado cambió de forma concurrente."
            )

        reservado = turno_repo.obtener_turno_con_detalles(connection, turno_id)

    return _serializar_turno(reservado)


def listar_mis_turnos(paciente_id: int, limit: int, offset: int, estado: str | None = None):
    with transaction() as connection:
        if not turno_repo.existe_paciente(connection, paciente_id):
            raise NotFoundError(description="No existe el paciente consultado.")

        total = turno_repo.contar_turnos_paciente(connection, paciente_id, estado)
        items = turno_repo.listar_turnos_paciente(connection, paciente_id, limit, offset, estado)

    items_serializados = [_serializar_turno(item) for item in items]
    return items_serializados, total


def cancelar_turno(turno_id: int, paciente_id: int | None = None, es_admin: bool = False) -> dict:
    with transaction() as connection:
        turno = turno_repo.obtener_turno_por_id(connection, turno_id)
        if turno is None:
            raise NotFoundError(description="No se encontró el turno especificado.")

        if not es_admin and paciente_id is not None:
            if turno["paciente_id"] != paciente_id:
                raise ForbiddenError(
                    description="No tenés permiso para cancelar un turno que no te pertenece."
                )

        estado_actual = turno["estado"]

        if estado_actual == ESTADO_CANCELADO:
            raise ConflictError(description="El turno ya se encuentra cancelado.")

        if estado_actual == ESTADO_ATENDIDO:
            raise ConflictError(
                description="No es posible cancelar un turno que ya ha sido atendido."
            )

        if estado_actual == ESTADO_AUSENTE:
            raise ConflictError(
                description="No es posible cancelar un turno marcado como ausente."
            )

        turno_repo.cancelar_turno(connection, turno_id)
        cancelado = turno_repo.obtener_turno_por_id(connection, turno_id)

    return _serializar_turno(cancelado)


def realizar_checkin(qr_token: str) -> dict:
    with transaction() as connection:
        turno = turno_repo.obtener_turno_por_qr(connection, qr_token)
        if turno is None:
            raise NotFoundError(
                description="Código QR inválido o no correspondiente a ningún turno."
            )

        estado_actual = turno["estado"]

        if estado_actual == ESTADO_CANCELADO:
            raise ConflictError(description="El turno se encuentra cancelado.")

        if estado_actual in (ESTADO_CONFIRMADO, ESTADO_ATENDIDO):
            raise ConflictError(
                description="El código QR ya fue utilizado anteriormente (check-in previo o turno atendido)."
            )

        if estado_actual == ESTADO_AUSENTE:
            raise ConflictError(
                description="El turno ha sido marcado como ausente y no admite check-in."
            )

        if estado_actual != ESTADO_RESERVADO:
            raise ConflictError(
                description=f"El turno no puede recibir check-in desde su estado actual '{estado_actual}'."
            )

        ahora = datetime.now()
        fecha_turno = turno["fecha_hora"]
        if isinstance(fecha_turno, str):
            fecha_turno = datetime.fromisoformat(fecha_turno)

        ventana_inicio = fecha_turno - timedelta(minutes=VENTANA_CHECKIN_MINUTOS)
        ventana_fin = fecha_turno + timedelta(minutes=VENTANA_CHECKIN_MINUTOS)

        if ahora < ventana_inicio:
            raise ConflictError(
                description="Aún no comenzó la ventana de check-in (habilitada desde 15 minutos antes del turno)."
            )

        if ahora > ventana_fin:
            turno_repo.actualizar_estado_turno(connection, turno["id"], ESTADO_AUSENTE)
            raise ConflictError(
                description="La ventana horaria de check-in ha expirado (+15 minutos). El turno ha sido marcado como ausente."
            )

        turno_repo.confirmar_checkin(connection, turno["id"], ahora)
        confirmado = turno_repo.obtener_turno_con_detalles(connection, turno["id"])

    return _serializar_turno(confirmado)


def marcar_atendido(turno_id: int) -> dict:
    with transaction() as connection:
        turno = turno_repo.obtener_turno_por_id(connection, turno_id)
        if turno is None:
            raise NotFoundError(description="No se encontró el turno especificado.")

        estado_actual = turno["estado"]

        if estado_actual == ESTADO_ATENDIDO:
            raise ConflictError(description="El turno ya se encuentra en estado atendido.")

        if estado_actual != ESTADO_CONFIRMADO:
            raise ConflictError(
                description=(
                    f"Solo se pueden marcar como atendidos los turnos con check-in confirmado "
                    f"(en sala de espera). Estado actual: '{estado_actual}'."
                )
            )

        turno_repo.marcar_atendido(connection, turno_id)
        atendido = turno_repo.obtener_turno_con_detalles(connection, turno_id)

    return _serializar_turno(atendido)
