from src.database.connection import execute_query

def buscar_paciente_por_usuario_id(usuario_id: int):
    query = """
        SELECT id, usuario_id, cobertura_id
        FROM pacientes
        WHERE usuario_id = %s
    """
    return execute_query(query, (usuario_id,), fetch_one=True)

def crear_paciente(cursor, usuario_id, cobertura_id=None) -> int:
    query = """
        INSERT INTO pacientes (usuario_id, cobertura_id)
        VALUES (%s, %s)
    """

    cursor.execute(query, (usuario_id, cobertura_id))
    return cursor.lastrowid