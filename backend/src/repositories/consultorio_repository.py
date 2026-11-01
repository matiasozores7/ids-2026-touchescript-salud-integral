def listar_consultorios_activos(connection):
    query = """
        SELECT id, numero_sala, piso, activo
        FROM consultorios
        WHERE activo = TRUE
        ORDER BY id
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def crear_consultorio(connection, numero_sala: str, piso: str | None) -> int:
    query = """
        INSERT INTO consultorios (numero_sala, piso)
        VALUES (%s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (numero_sala, piso))
        return cursor.lastrowid


def buscar_consultorio_activo(connection, consultorio_id: int):
    query = """
        SELECT id
        FROM consultorios
        WHERE id = %s AND activo = TRUE
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (consultorio_id,))
        return cursor.fetchone()


def actualizar_consultorio(
    connection,
    consultorio_id: int,
    numero_sala: str,
    piso: str | None
) -> None:
    query = """
        UPDATE consultorios
        SET numero_sala = %s, piso = %s
        WHERE id = %s AND activo = TRUE
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (numero_sala, piso, consultorio_id))
