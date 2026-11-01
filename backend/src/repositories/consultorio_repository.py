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
