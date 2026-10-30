from src.database.connection import execute_query

def buscar_medico_por_usuario_id(usuario_id: int):
    query = """
        SELECT id, usuario_id, especialidad_id
        FROM medicos
        WHERE usuario_id = %s
    """
    return execute_query(query, (usuario_id,), fetch_one=True)


def crear_medico(cursor, usuario_id: int, especialidad_id: int) -> int:
    query = """
        INSERT INTO medicos (usuario_id, especialidad_id)
        VALUES (%s, %s)
    """

    cursor.execute(query, (usuario_id, especialidad_id))

    return cursor.lastrowid