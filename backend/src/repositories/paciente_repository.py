
def buscar_paciente_por_usuario_id(connection, usuario_id: int):
    query = """
        SELECT id, usuario_id, cobertura_id
        FROM pacientes
        WHERE usuario_id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id,))
        return cursor.fetchone()


def crear_paciente(connection, usuario_id: int, cobertura_id=None) -> int:
    query = """
        INSERT INTO pacientes (usuario_id, cobertura_id)
        VALUES (%s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id, cobertura_id))
        return cursor.lastrowid
