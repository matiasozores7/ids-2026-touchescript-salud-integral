def contar_especialidades(connection) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM especialidades
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()["total"]



def listar_especialidades(connection, limit: int, offset: int):
    query = """
        SELECT
            e.id,
            e.nombre,
            e.descripcion,
            (
                SELECT COUNT(*)
                FROM medicos m
                JOIN usuarios u ON u.id = m.usuario_id
                WHERE m.especialidad_id = e.id
                  AND u.activo = TRUE
            ) AS cantidad_medicos
        FROM especialidades e
        ORDER BY e.nombre
        LIMIT %s OFFSET %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()



def existe_nombre(connection, nombre: str) -> bool:
    query = """
        SELECT id
        FROM especialidades
        WHERE nombre = %s
        LIMIT 1
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (nombre,))
        return cursor.fetchone() is not None


def crear_especialidad(connection, nombre: str, descripcion: str | None) -> int:
    query = """
        INSERT INTO especialidades (nombre, descripcion)
        VALUES (%s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (nombre, descripcion))
        return cursor.lastrowid


def buscar_especialidad(connection, especialidad_id: int):
    query = """
        SELECT id
        FROM especialidades
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (especialidad_id,))
        return cursor.fetchone()


def actualizar_especialidad(
    connection,
    especialidad_id: int,
    nombre: str,
    descripcion: str | None
) -> None:
    query = """
        UPDATE especialidades
        SET nombre = %s, descripcion = %s
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (nombre, descripcion, especialidad_id))


def contar_medicos(connection, especialidad_id: int) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM medicos
        WHERE especialidad_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (especialidad_id,))
        return cursor.fetchone()["total"]


def eliminar_especialidad(connection, especialidad_id: int) -> None:
    query = """
        DELETE FROM especialidades
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (especialidad_id,))
