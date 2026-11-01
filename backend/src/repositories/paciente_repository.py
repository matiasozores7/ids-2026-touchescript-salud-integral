
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

def obtener_todos_los_pacientes(connection):
    query = """
        SELECT
            pacientes.id AS paciente_id,
            usuarios.id AS usuario_id,
            usuarios.nombre AS nombre,
            usuarios.apellido AS apellido,
            usuarios.email AS email,
            coberturas.nombre AS cobertura_medica
        FROM pacientes
        INNER JOIN usuarios ON pacientes.usuario_id = usuarios.id
        LEFT JOIN coberturas ON pacientes.cobertura_id = coberturas.id
        WHERE usuarios.activo = 1;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
