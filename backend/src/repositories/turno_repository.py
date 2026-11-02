def obtener_turno_por_id(connection, turno_id: int):
    query = """
        SELECT id, medico_id, paciente_id, consultorio_id, fecha_hora, fecha_hora_llegada, estado, qr_token
        FROM turnos
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (turno_id,))
        return cursor.fetchone()


def actualizar_estado_turno(connection, turno_id: int, nuevo_estado: str) -> int:
    query = """
        UPDATE turnos
        SET estado = %s
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (nuevo_estado, turno_id))
        return cursor.rowcount


def existe_turno_en_horario(connection, medico_id: int, consultorio_id: int, fecha_hora) -> bool:
    query = """
        SELECT id
        FROM turnos
        WHERE fecha_hora = %s
          AND (medico_id = %s OR consultorio_id = %s)
          AND estado != 'cancelado'
        LIMIT 1
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (fecha_hora, medico_id, consultorio_id))
        return cursor.fetchone() is not None


def insertar_turno(connection, medico_id: int, consultorio_id: int, fecha_hora, estado: str = "disponible") -> int:
    query = """
        INSERT INTO turnos (medico_id, paciente_id, consultorio_id, fecha_hora, estado, qr_token)
        VALUES (%s, NULL, %s, %s, %s, NULL)
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id, consultorio_id, fecha_hora, estado))
        return cursor.lastrowid


def obtener_agendas_para_generacion(connection, medico_id: int | None = None) -> list:
    if medico_id is not None:
        query = """
            SELECT a.id, a.medico_id, a.consultorio_id, a.dia_semana,
                   a.hora_inicio, a.hora_fin, a.duracion_turno
            FROM agendas a
            JOIN medicos m ON a.medico_id = m.id
            JOIN usuarios u ON m.usuario_id = u.id
            JOIN consultorios c ON a.consultorio_id = c.id
            WHERE u.activo = TRUE AND c.activo = TRUE AND a.medico_id = %s
        """
        params = (medico_id,)
    else:
        query = """
            SELECT a.id, a.medico_id, a.consultorio_id, a.dia_semana,
                   a.hora_inicio, a.hora_fin, a.duracion_turno
            FROM agendas a
            JOIN medicos m ON a.medico_id = m.id
            JOIN usuarios u ON m.usuario_id = u.id
            JOIN consultorios c ON a.consultorio_id = c.id
            WHERE u.activo = TRUE AND c.activo = TRUE
        """
        params = ()

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()
