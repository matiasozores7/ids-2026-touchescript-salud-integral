def obtener_pacientes_en_sala_espera(connection, fecha: str | None = None):
    query = """
        SELECT 
            turnos.id AS turno_id,
            turnos.fecha_hora AS fecha_hora_turno,
            turnos.fecha_hora_llegada,
            turnos.estado,
            
            paciente_usuario.id AS paciente_usuario_id,
            paciente_usuario.nombre AS paciente_nombre,
            paciente_usuario.apellido AS paciente_apellido,
            
            medico_usuario.id AS medico_usuario_id,
            medico_usuario.nombre AS medico_nombre,
            medico_usuario.apellido AS medico_apellido,
            especialidades.nombre AS especialidad,
            
            consultorios.numero_sala AS consultorio_sala,
            consultorios.piso AS consultorio_piso

        FROM turnos
        INNER JOIN pacientes ON turnos.paciente_id = pacientes.id
        INNER JOIN usuarios AS paciente_usuario ON pacientes.usuario_id = paciente_usuario.id
        INNER JOIN medicos ON turnos.medico_id = medicos.id
        INNER JOIN usuarios AS medico_usuario ON medicos.usuario_id = medico_usuario.id
        INNER JOIN especialidades ON medicos.especialidad_id = especialidades.id
        INNER JOIN consultorios ON turnos.consultorio_id = consultorios.id
        WHERE turnos.estado = 'confirmado'
          AND paciente_usuario.rol = 'paciente'
          AND medico_usuario.rol = 'medico'
          AND paciente_usuario.activo = 1
    """
    params = []

    if fecha:
        query += " AND DATE(turnos.fecha_hora) = %s"
        params.append(fecha)
    else:
        query += " AND DATE(turnos.fecha_hora) = CURDATE()"

    query += " ORDER BY turnos.fecha_hora_llegada ASC;"

    with connection.cursor() as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()


def obtener_turnos_por_medico_y_especialidad(connection, fecha: str | None = None):
    filtro_fecha = "AND DATE(turnos.fecha_hora) = %s" if fecha else "AND DATE(turnos.fecha_hora) = CURDATE()"
    params = (fecha,) if fecha else ()

    query = f"""
        SELECT 
            medicos.id AS medico_id,
            usuarios.nombre AS medico_nombre,
            usuarios.apellido AS medico_apellido,
            especialidades.id AS especialidad_id,
            especialidades.nombre AS especialidad,
            COUNT(turnos.id) AS total_turnos,
            SUM(CASE WHEN turnos.estado = 'disponible' THEN 1 ELSE 0 END) AS turnos_disponibles,
            SUM(CASE WHEN turnos.estado = 'reservado' THEN 1 ELSE 0 END) AS turnos_reservados,
            SUM(CASE WHEN turnos.estado = 'confirmado' THEN 1 ELSE 0 END) AS turnos_confirmados,
            SUM(CASE WHEN turnos.estado = 'atendido' THEN 1 ELSE 0 END) AS turnos_atendidos,
            SUM(CASE WHEN turnos.estado = 'cancelado' THEN 1 ELSE 0 END) AS turnos_cancelados
        FROM medicos
        INNER JOIN usuarios ON medicos.usuario_id = usuarios.id
        INNER JOIN especialidades ON medicos.especialidad_id = especialidades.id
        LEFT JOIN turnos ON turnos.medico_id = medicos.id {filtro_fecha}
        WHERE usuarios.rol = 'medico'
          AND usuarios.activo = 1
        GROUP BY 
            medicos.id, 
            usuarios.nombre, 
            usuarios.apellido, 
            especialidades.id, 
            especialidades.nombre
        ORDER BY total_turnos DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def obtener_ocupacion_consultorios(connection, fecha: str | None = None):
    filtro_fecha = "AND DATE(turnos.fecha_hora) = %s" if fecha else "AND DATE(turnos.fecha_hora) = CURDATE()"
    params = (fecha,) if fecha else ()

    query = f"""
        SELECT 
            consultorios.id AS consultorio_id,
            consultorios.numero_sala,
            consultorios.piso,
            COUNT(turnos.id) AS total_turnos,
            SUM(CASE WHEN turnos.estado IN ('reservado', 'confirmado', 'atendido') THEN 1 ELSE 0 END) AS turnos_ocupados,
            SUM(CASE WHEN turnos.estado IN ('disponible', 'ausente', 'cancelado') THEN 1 ELSE 0 END) AS turnos_libres
        FROM consultorios
        LEFT JOIN turnos ON turnos.consultorio_id = consultorios.id {filtro_fecha}
        GROUP BY consultorios.id, consultorios.numero_sala, consultorios.piso
        ORDER BY consultorios.id ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def obtener_estadisticas_ausentismo(connection, fecha: str | None = None):
    filtro_fecha = "AND DATE(turnos.fecha_hora) = %s" if fecha else "AND DATE(turnos.fecha_hora) = CURDATE()"
    params = (fecha,) if fecha else ()

    query = f"""
        SELECT 
            medicos.id AS medico_id,
            usuarios.nombre AS medico_nombre,
            usuarios.apellido AS medico_apellido,
            especialidades.nombre AS especialidad,
            COUNT(turnos.id) AS turnos_agendados,
            SUM(CASE WHEN turnos.estado = 'ausente' THEN 1 ELSE 0 END) AS ausentes,
            SUM(CASE WHEN turnos.estado IN ('confirmado', 'atendido') THEN 1 ELSE 0 END) AS asistieron,
            SUM(CASE WHEN turnos.estado = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
        FROM medicos
        INNER JOIN usuarios ON medicos.usuario_id = usuarios.id
        INNER JOIN especialidades ON medicos.especialidad_id = especialidades.id
        INNER JOIN turnos ON turnos.medico_id = medicos.id {filtro_fecha}
        WHERE usuarios.rol = 'medico'
          AND turnos.estado != 'disponible'
        GROUP BY medicos.id, usuarios.nombre, usuarios.apellido, especialidades.nombre
        ORDER BY ausentes DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def obtener_estadisticas_tiempo_espera(connection, fecha: str | None = None):
    filtro_fecha = "AND DATE(turnos.fecha_hora) = %s" if fecha else "AND DATE(turnos.fecha_hora) = CURDATE()"
    params = (fecha,) if fecha else ()

    query = f"""
        SELECT 
            medicos.id AS medico_id,
            usuarios.nombre AS medico_nombre,
            usuarios.apellido AS medico_apellido,
            especialidades.nombre AS especialidad,
            COUNT(turnos.id) AS pacientes_evaluados,
            AVG(TIMESTAMPDIFF(MINUTE, turnos.fecha_hora_llegada, turnos.fecha_hora)) AS tiempo_promedio_minutos
        FROM medicos
        INNER JOIN usuarios ON medicos.usuario_id = usuarios.id
        INNER JOIN especialidades ON medicos.especialidad_id = especialidades.id
        INNER JOIN turnos ON turnos.medico_id = medicos.id {filtro_fecha}
        WHERE usuarios.rol = 'medico'
          AND turnos.fecha_hora_llegada IS NOT NULL
        GROUP BY medicos.id, usuarios.nombre, usuarios.apellido, especialidades.nombre
        ORDER BY tiempo_promedio_minutos DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def obtener_estadisticas_turnos_hoy(connection) -> dict:
    query = """
        SELECT
            COUNT(*) AS total,
            SUM(CASE
                WHEN estado = 'atendido' THEN 1
                ELSE 0
            END) AS atendidos
        FROM turnos
        WHERE fecha_hora >= CURDATE()
          AND fecha_hora < CURDATE() + INTERVAL 1 DAY
          AND estado IN ('reservado', 'confirmado', 'atendido', 'ausente')
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        resultado = cursor.fetchone()

    return {
        "total": resultado["total"],
        "atendidos": resultado["atendidos"] or 0
    }

def obtener_turnos_por_hora(connection):
    query = """
        SELECT
            HOUR(fecha_hora) AS hora,
            COUNT(*) AS total
        FROM turnos
        WHERE fecha_hora >= CURDATE() + INTERVAL 8 HOUR
          AND fecha_hora < CURDATE() + INTERVAL 19 HOUR
          AND estado IN ('reservado', 'confirmado', 'atendido', 'ausente')
        GROUP BY HOUR(fecha_hora)
        ORDER BY hora ASC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def obtener_proximos_turnos(connection, limite: int = 3):
    query = """
        SELECT
            turnos.id AS turno_id,
            turnos.fecha_hora AS fecha_hora_turno,
            turnos.estado,

            paciente_usuario.nombre AS paciente_nombre,
            paciente_usuario.apellido AS paciente_apellido,

            medico_usuario.nombre AS medico_nombre,
            medico_usuario.apellido AS medico_apellido,

            especialidades.nombre AS especialidad,

            consultorios.numero_sala AS consultorio_sala,
            consultorios.piso AS consultorio_piso

        FROM turnos
        INNER JOIN pacientes
            ON turnos.paciente_id = pacientes.id
        INNER JOIN usuarios AS paciente_usuario
            ON pacientes.usuario_id = paciente_usuario.id
        INNER JOIN medicos
            ON turnos.medico_id = medicos.id
        INNER JOIN usuarios AS medico_usuario
            ON medicos.usuario_id = medico_usuario.id
        INNER JOIN especialidades
            ON medicos.especialidad_id = especialidades.id
        INNER JOIN consultorios
            ON turnos.consultorio_id = consultorios.id

        WHERE turnos.fecha_hora >= NOW()
          AND turnos.estado IN ('reservado', 'confirmado')
          AND turnos.fecha_hora_llegada IS NULL
          AND paciente_usuario.rol = 'paciente'
          AND paciente_usuario.activo = 1
          AND medico_usuario.rol = 'medico'
          AND medico_usuario.activo = 1

        ORDER BY turnos.fecha_hora ASC
        LIMIT %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limite,))
        return cursor.fetchall()

def obtener_estadisticas_generales(connection) -> dict:
    query = """
        SELECT
            (
                SELECT COUNT(*)
                FROM pacientes
                INNER JOIN usuarios
                    ON pacientes.usuario_id = usuarios.id
                WHERE usuarios.rol = 'paciente'
                  AND usuarios.activo = 1
            ) AS pacientes_registrados,

            (
                SELECT COUNT(*)
                FROM medicos
                INNER JOIN usuarios
                    ON medicos.usuario_id = usuarios.id
                WHERE usuarios.rol = 'medico'
                  AND usuarios.activo = 1
            ) AS profesionales_activos,

            (
                SELECT COUNT(*)
                FROM turnos
                WHERE fecha_hora >= NOW()
                  AND estado = 'reservado'
            ) AS turnos_futuros_reservados;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()