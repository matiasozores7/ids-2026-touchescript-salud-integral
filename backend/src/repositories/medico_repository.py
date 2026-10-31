
def buscar_medico_por_usuario_id(connection, usuario_id: int):
    query = """
        SELECT id, usuario_id, especialidad_id
        FROM medicos
        WHERE usuario_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id,))
        return cursor.fetchone()


def crear_medico(connection, usuario_id: int, especialidad_id: int) -> int:
    query = """
        INSERT INTO medicos (usuario_id, especialidad_id)
        VALUES (%s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id, especialidad_id))
        return cursor.lastrowid
