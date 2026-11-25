def contar_turnos(connection, periodo: int) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM turnos
        WHERE fecha_hora >= (CURDATE() - INTERVAL %s DAY)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        resultado = cursor.fetchone()
        return resultado["total"] if resultado else 0


def obtener_ausentismo_general(connection, periodo: int) -> float:
    query = """
        SELECT ROUND(
            SUM(estado = 'ausente') * 100 /
            NULLIF(SUM(estado IN ('atendido', 'ausente')), 0),
            1
        ) AS value
        FROM turnos
        WHERE fecha_hora >= (CURDATE() - INTERVAL %s DAY)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        resultado = cursor.fetchone()
        return float(resultado["value"] or 0) if resultado else 0


def obtener_espera_promedio(connection, periodo: int) -> float:
    query = """
        SELECT ROUND(
            AVG(GREATEST(
                TIMESTAMPDIFF(MINUTE, fecha_hora_llegada, fecha_hora),
                0
            )),
            1
        ) AS value
        FROM turnos
        WHERE fecha_hora >= (CURDATE() - INTERVAL %s DAY)
          AND estado = 'atendido'
          AND fecha_hora_llegada IS NOT NULL
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        resultado = cursor.fetchone()
        return float(resultado["value"] or 0) if resultado else 0


def obtener_ausentismo_por_especialidad(connection, periodo: int) -> list:
    query = """
        SELECT
            especialidades.nombre AS label,
            ROUND(
                SUM(turnos.estado = 'ausente') * 100 /
                NULLIF(
                    SUM(turnos.estado IN ('atendido', 'ausente')),
                    0
                ),
                1
            ) AS value
        FROM turnos
        INNER JOIN medicos ON medicos.id = turnos.medico_id
        INNER JOIN especialidades
            ON especialidades.id = medicos.especialidad_id
        WHERE turnos.fecha_hora >=
              (CURDATE() - INTERVAL %s DAY)
        GROUP BY especialidades.id, especialidades.nombre
        HAVING value IS NOT NULL
        ORDER BY value DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        return cursor.fetchall()


def obtener_resultados_turnos(connection, periodo: int) -> dict:
    query = """
        SELECT
            SUM(estado = 'atendido') AS atendido,
            SUM(estado = 'ausente') AS ausente,
            SUM(estado = 'cancelado') AS cancelado
        FROM turnos
        WHERE fecha_hora >= (CURDATE() - INTERVAL %s DAY)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        resultado = cursor.fetchone()

    if not resultado:
        resultado = {}

    return {
        "labels": ["Atendido", "Ausente", "Cancelado"],
        "values": [
            int(resultado.get("atendido") or 0),
            int(resultado.get("ausente") or 0),
            int(resultado.get("cancelado") or 0)
        ]
    }


def obtener_ocupacion_consultorios(connection, periodo: int) -> list:
    query = """
        SELECT
            consultorios.numero_sala AS label,
            ROUND(
                SUM(turnos.estado IN (
                    'reservado',
                    'confirmado',
                    'atendido',
                    'ausente'
                )) * 100 / NULLIF(COUNT(*), 0),
                1
            ) AS value
        FROM turnos
        INNER JOIN consultorios
            ON consultorios.id = turnos.consultorio_id
        WHERE turnos.fecha_hora >=
              (CURDATE() - INTERVAL %s DAY)
        GROUP BY consultorios.id, consultorios.numero_sala
        HAVING value IS NOT NULL
        ORDER BY consultorios.numero_sala
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        return cursor.fetchall()


def obtener_espera_diaria(connection, periodo: int) -> list:
    query = """
        SELECT
            DATE_FORMAT(turnos.fecha_hora, '%%d/%%m') AS label,
            ROUND(
                AVG(GREATEST(
                    TIMESTAMPDIFF(
                        MINUTE,
                        turnos.fecha_hora_llegada,
                        turnos.fecha_hora
                    ),
                    0
                )),
                1
            ) AS value
        FROM turnos
        WHERE turnos.fecha_hora >=
              (CURDATE() - INTERVAL %s DAY)
          AND turnos.estado = 'atendido'
          AND turnos.fecha_hora_llegada IS NOT NULL
        GROUP BY DATE(turnos.fecha_hora)
        ORDER BY DATE(turnos.fecha_hora)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        return cursor.fetchall()


def obtener_espera_por_profesional(connection, periodo: int) -> list:
    query = """
        SELECT
            CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS label,
            ROUND(
                AVG(GREATEST(
                    TIMESTAMPDIFF(
                        MINUTE,
                        turnos.fecha_hora_llegada,
                        turnos.fecha_hora
                    ),
                    0
                )),
                1
            ) AS value
        FROM turnos
        INNER JOIN medicos ON medicos.id = turnos.medico_id
        INNER JOIN usuarios ON usuarios.id = medicos.usuario_id
        WHERE turnos.fecha_hora >=
              (CURDATE() - INTERVAL %s DAY)
          AND turnos.estado = 'atendido'
          AND turnos.fecha_hora_llegada IS NOT NULL
        GROUP BY medicos.id, usuarios.nombre, usuarios.apellido
        HAVING value IS NOT NULL
        ORDER BY value DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (periodo,))
        return cursor.fetchall()