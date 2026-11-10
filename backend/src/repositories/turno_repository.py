from datetime import timedelta


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


def cancelar_turno(connection, turno_id: int) -> int:
    query = """
        UPDATE turnos
        SET estado = 'cancelado'
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (turno_id,))
        return cursor.rowcount


def obtener_turno_por_qr(connection, qr_token: str):
    query = """
        SELECT t.id, t.medico_id, t.paciente_id, t.consultorio_id, t.fecha_hora,
               t.fecha_hora_llegada, t.estado, t.qr_token,
               u_pac.nombre AS paciente_nombre, u_pac.apellido AS paciente_apellido,
               u_med.nombre AS medico_nombre, u_med.apellido AS medico_apellido,
               c.numero_sala AS consultorio_sala
        FROM turnos t
        LEFT JOIN pacientes p ON t.paciente_id = p.id
        LEFT JOIN usuarios u_pac ON p.usuario_id = u_pac.id
        JOIN medicos m ON t.medico_id = m.id
        JOIN usuarios u_med ON m.usuario_id = u_med.id
        JOIN consultorios c ON t.consultorio_id = c.id
        WHERE t.qr_token = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (qr_token,))
        return cursor.fetchone()


def confirmar_checkin(connection, turno_id: int, fecha_hora_llegada) -> int:
    query = """
        UPDATE turnos
        SET estado = 'confirmado',
            fecha_hora_llegada = %s
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (fecha_hora_llegada, turno_id))
        return cursor.rowcount


def marcar_atendido(connection, turno_id: int) -> int:
    query = """
        UPDATE turnos
        SET estado = 'atendido'
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (turno_id,))
        return cursor.rowcount


def marcar_turnos_ausentes_expirados(connection, fecha_limite) -> int:
    query = """
        UPDATE turnos
        SET estado = 'ausente'
        WHERE estado = 'reservado'
          AND fecha_hora < %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (fecha_limite,))
        return cursor.rowcount


def obtener_dias_disponibles(connection, medico_id: int):
    query = """
        SELECT DISTINCT dia_semana
        FROM agendas
        WHERE medico_id = %s
        ORDER BY FIELD(
            dia_semana,
            'Lunes', 'Martes', 'Miercoles',
            'Jueves', 'Viernes', 'Sabado', 'Domingo'
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        filas = cursor.fetchall()

    return [
        fila["dia_semana"] if isinstance(fila, dict) else fila[0]
        for fila in filas
    ]


def obtener_horarios_disponibles(connection, medico_id: int, fecha: str):
    query = """
        SELECT hora_inicio, hora_fin
        FROM agendas
        WHERE medico_id = %s
          AND dia_semana = CASE DAYOFWEEK(%s)
              WHEN 1 THEN 'Domingo'
              WHEN 2 THEN 'Lunes'
              WHEN 3 THEN 'Martes'
              WHEN 4 THEN 'Miercoles'
              WHEN 5 THEN 'Jueves'
              WHEN 6 THEN 'Viernes'
              WHEN 7 THEN 'Sabado'
          END
        ORDER BY hora_inicio
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id, fecha))
        filas = cursor.fetchall()

    horarios = []

    for fila in filas:
        inicio = fila["hora_inicio"] if isinstance(fila, dict) else fila[0]
        fin = fila["hora_fin"] if isinstance(fila, dict) else fila[1]

        if isinstance(inicio, timedelta):
            inicio = str(inicio)

        if isinstance(fin, timedelta):
            fin = str(fin)

        horarios.append({
            "hora_inicio": str(inicio),
            "hora_fin": str(fin)
        })

    return horarios


def obtener_turnos_disponibles(connection, medico_id: int, fecha: str | None = None) -> list:
    query = """
        SELECT t.id, t.medico_id, t.consultorio_id, t.fecha_hora, t.estado,
               c.numero_sala AS consultorio_sala, c.piso AS consultorio_piso
        FROM turnos t
        JOIN consultorios c ON t.consultorio_id = c.id
        WHERE t.medico_id = %s
          AND t.estado = 'disponible'
          AND t.fecha_hora > NOW()
    """
    params = [medico_id]

    if fecha:
        query += " AND DATE(t.fecha_hora) = %s"
        params.append(fecha)

    query += " ORDER BY t.fecha_hora ASC"

    with connection.cursor() as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
