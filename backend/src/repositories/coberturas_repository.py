def contar_coberturas(connection) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM coberturas
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()["total"]


def listar_coberturas(connection, limit: int, offset: int):
    query = """
        SELECT id, nombre
        FROM coberturas
        ORDER BY nombre
        LIMIT %s OFFSET %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()


def buscar_cobertura(connection, cobertura_id: int):
    query = """
        SELECT id, nombre
        FROM coberturas
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (cobertura_id,))
        return cursor.fetchone()


def existe_nombre(
    connection,
    nombre: str,
    excluir_id: int | None = None
) -> bool:
    if excluir_id is None:
        query = """
            SELECT id
            FROM coberturas
            WHERE nombre = %s
            LIMIT 1
        """
        params = (nombre,)
    else:
        query = """
            SELECT id
            FROM coberturas
            WHERE nombre = %s AND id <> %s
            LIMIT 1
        """
        params = (nombre, excluir_id)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone() is not None


def crear_cobertura(connection, nombre: str) -> int:
    query = """
        INSERT INTO coberturas (nombre)
        VALUES (%s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (nombre,))
        return cursor.lastrowid


def actualizar_cobertura(
    connection,
    cobertura_id: int,
    nombre: str
) -> None:
    query = """
        UPDATE coberturas
        SET nombre = %s
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (nombre, cobertura_id))


def contar_pacientes(connection, cobertura_id: int) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM pacientes
        WHERE cobertura_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (cobertura_id,))
        return cursor.fetchone()["total"]


def eliminar_cobertura(connection, cobertura_id: int) -> None:
    query = """
        DELETE FROM coberturas
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (cobertura_id,))