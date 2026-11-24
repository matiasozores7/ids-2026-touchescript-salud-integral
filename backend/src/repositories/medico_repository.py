def buscar_medico_por_usuario_id(connection, usuario_id: int):
    query = """
        SELECT id, usuario_id, especialidad_id, matricula
        FROM medicos
        WHERE usuario_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id,))
        return cursor.fetchone()


def crear_medico(
    connection,
    usuario_id: int,
    especialidad_id: int,
    matricula: str
) -> int:
    query = """
        INSERT INTO medicos (usuario_id, especialidad_id, matricula)
        VALUES (%s, %s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id, especialidad_id, matricula))
        return cursor.lastrowid


def buscar_medico_por_matricula(connection, matricula: str, excluir_id=None):
    query = """
        SELECT id
        FROM medicos
        WHERE matricula = %s
    """
    params = [matricula]

    if excluir_id is not None:
        query += " AND id <> %s"
        params.append(excluir_id)

    with connection.cursor() as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchone()


def _agregar_filtro_cobertura_paciente(query, params, paciente_id):
    if paciente_id is not None:
        query += """
            AND EXISTS (
                SELECT 1
                FROM pacientes p
                JOIN medicos_coberturas mc ON mc.cobertura_id = p.cobertura_id
                WHERE p.id = %s AND mc.medico_id = m.id
            )
        """
        params.append(paciente_id)

    return query


def contar_medicos(connection, especialidad_id=None, paciente_id=None):
    query = """
        SELECT COUNT(*) AS total
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE u.activo = TRUE
    """

    params = []

    if especialidad_id is not None:
        query += " AND m.especialidad_id = %s"
        params.append(especialidad_id)

    query = _agregar_filtro_cobertura_paciente(query, params, paciente_id)

    with connection.cursor() as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchone()["total"]


def listar_medicos(
    connection,
    limit: int,
    offset: int,
    especialidad_id: int | None = None,
    paciente_id: int | None = None
):
    query = """
        SELECT m.id, u.nombre, u.apellido, u.email, u.telefono,
               m.especialidad_id, m.matricula,
               e.nombre AS especialidad
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        JOIN especialidades e ON e.id = m.especialidad_id
        WHERE u.activo = TRUE
    """

    params = []

    if especialidad_id is not None:
        query += " AND m.especialidad_id = %s"
        params.append(especialidad_id)

    query = _agregar_filtro_cobertura_paciente(query, params, paciente_id)

    query += """
        ORDER BY u.apellido, u.nombre
        LIMIT %s OFFSET %s
    """

    params.extend([limit, offset])

    with connection.cursor() as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()


def existe_especialidad(connection, especialidad_id: int) -> bool:
    query = "SELECT id FROM especialidades WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (especialidad_id,))
        return cursor.fetchone() is not None


def obtener_medico_por_id(connection, medico_id: int):
    query = """
        SELECT m.id, m.usuario_id, u.nombre, u.apellido, u.email,
               u.telefono, u.activo, m.especialidad_id, m.matricula,
               e.nombre AS especialidad
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        JOIN especialidades e ON e.id = m.especialidad_id
        WHERE m.id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        return cursor.fetchone()


def actualizar_medico(connection, medico_id: int, usuario_id: int,
                      nombre: str, apellido: str, email: str,
                      telefono: str | None, especialidad_id: int,
                      matricula: str):
    query_usuario = """
        UPDATE usuarios
        SET nombre = %s, apellido = %s, email = %s, telefono = %s
        WHERE id = %s
    """
    query_medico = """
        UPDATE medicos
        SET especialidad_id = %s, matricula = %s
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query_usuario,
            (nombre, apellido, email, telefono, usuario_id)
        )
        cursor.execute(query_medico, (especialidad_id, matricula, medico_id))


def listar_coberturas(connection, medico_id: int):
    query = """
        SELECT c.id, c.nombre
        FROM medicos_coberturas mc
        JOIN coberturas c ON c.id = mc.cobertura_id
        WHERE mc.medico_id = %s
        ORDER BY c.nombre
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        return cursor.fetchall()


def reemplazar_coberturas(connection, medico_id: int, cobertura_ids: list[int]):
    delete_query = "DELETE FROM medicos_coberturas WHERE medico_id = %s"
    insert_query = """
        INSERT INTO medicos_coberturas (medico_id, cobertura_id)
        VALUES (%s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(delete_query, (medico_id,))
        cursor.executemany(
            insert_query,
            [(medico_id, cobertura_id) for cobertura_id in cobertura_ids]
        )


def contar_turnos_pendientes(connection, medico_id: int) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM turnos
        WHERE medico_id = %s
          AND estado IN ('reservado', 'confirmado')
          AND fecha_hora >= NOW()
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        return cursor.fetchone()["total"]


def desactivar_usuario(connection, usuario_id: int):
    query = "UPDATE usuarios SET activo = FALSE WHERE id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id,))

def listar_por_especialidad(connection, especialidad_id: int):
    query = """
        SELECT m.id, u.nombre, u.apellido, u.email,
               e.id AS especialidad_id, e.nombre AS especialidad
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        JOIN especialidades e ON e.id = m.especialidad_id
        WHERE m.especialidad_id = %s
          AND u.activo = TRUE
        ORDER BY u.apellido, u.nombre
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (especialidad_id,))
        return cursor.fetchall()

def obtener_medico_activo(connection, medico_id):
    query = """
        SELECT m.id
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE m.id = %s AND u.activo = TRUE
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        return cursor.fetchone()