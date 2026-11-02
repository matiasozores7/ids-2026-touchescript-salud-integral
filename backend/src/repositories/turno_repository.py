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


def existe_paciente(connection, paciente_id: int) -> bool:
    query = "SELECT id FROM pacientes WHERE id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (paciente_id,))
        return cursor.fetchone() is not None


def existe_reserva_paciente_con_medico_en_fecha(connection, paciente_id: int, medico_id: int, fecha_inicio, fecha_fin) -> bool:
    query = """
        SELECT id
        FROM turnos
        WHERE paciente_id = %s
          AND medico_id = %s
          AND fecha_hora >= %s AND fecha_hora <= %s
          AND estado IN ('reservado', 'confirmado')
        LIMIT 1
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (paciente_id, medico_id, fecha_inicio, fecha_fin))
        return cursor.fetchone() is not None


def reservar_turno(connection, turno_id: int, paciente_id: int, qr_token: str) -> int:
    query = """
        UPDATE turnos
        SET paciente_id = %s,
            estado = 'reservado',
            qr_token = %s
        WHERE id = %s AND estado = 'disponible'
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (paciente_id, qr_token, turno_id))
        return cursor.rowcount


def obtener_turno_con_detalles(connection, turno_id: int):
    query = """
        SELECT t.id, t.medico_id, t.paciente_id, t.consultorio_id, t.fecha_hora,
               t.fecha_hora_llegada, t.estado, t.qr_token,
               u_pac.nombre AS paciente_nombre, u_pac.apellido AS paciente_apellido,
               u_med.nombre AS medico_nombre, u_med.apellido AS medico_apellido,
               e.nombre AS especialidad_nombre,
               c.numero_sala AS consultorio_sala, c.piso AS consultorio_piso
        FROM turnos t
        LEFT JOIN pacientes p ON t.paciente_id = p.id
        LEFT JOIN usuarios u_pac ON p.usuario_id = u_pac.id
        JOIN medicos m ON t.medico_id = m.id
        JOIN usuarios u_med ON m.usuario_id = u_med.id
        LEFT JOIN especialidades e ON m.especialidad_id = e.id
        JOIN consultorios c ON t.consultorio_id = c.id
        WHERE t.id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (turno_id,))
        return cursor.fetchone()


def listar_turnos_paciente(connection, paciente_id: int, limit: int, offset: int, estado: str | None = None) -> list:
    if estado:
        query = """
            SELECT t.id, t.medico_id, t.paciente_id, t.consultorio_id, t.fecha_hora,
                   t.fecha_hora_llegada, t.estado, t.qr_token,
                   u_med.nombre AS medico_nombre, u_med.apellido AS medico_apellido,
                   e.nombre AS especialidad_nombre,
                   c.numero_sala AS consultorio_sala, c.piso AS consultorio_piso
            FROM turnos t
            JOIN medicos m ON t.medico_id = m.id
            JOIN usuarios u_med ON m.usuario_id = u_med.id
            LEFT JOIN especialidades e ON m.especialidad_id = e.id
            JOIN consultorios c ON t.consultorio_id = c.id
            WHERE t.paciente_id = %s AND t.estado = %s
            ORDER BY t.fecha_hora DESC
            LIMIT %s OFFSET %s
        """
        params = (paciente_id, estado, limit, offset)
    else:
        query = """
            SELECT t.id, t.medico_id, t.paciente_id, t.consultorio_id, t.fecha_hora,
                   t.fecha_hora_llegada, t.estado, t.qr_token,
                   u_med.nombre AS medico_nombre, u_med.apellido AS medico_apellido,
                   e.nombre AS especialidad_nombre,
                   c.numero_sala AS consultorio_sala, c.piso AS consultorio_piso
            FROM turnos t
            JOIN medicos m ON t.medico_id = m.id
            JOIN usuarios u_med ON m.usuario_id = u_med.id
            LEFT JOIN especialidades e ON m.especialidad_id = e.id
            JOIN consultorios c ON t.consultorio_id = c.id
            WHERE t.paciente_id = %s
            ORDER BY t.fecha_hora DESC
            LIMIT %s OFFSET %s
        """
        params = (paciente_id, limit, offset)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def contar_turnos_paciente(connection, paciente_id: int, estado: str | None = None) -> int:
    if estado:
        query = "SELECT COUNT(*) AS total FROM turnos WHERE paciente_id = %s AND estado = %s"
        params = (paciente_id, estado)
    else:
        query = "SELECT COUNT(*) AS total FROM turnos WHERE paciente_id = %s"
        params = (paciente_id,)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()["total"]
