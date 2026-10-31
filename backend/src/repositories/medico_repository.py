
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
    

def contar_medicos(connection) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE u.activo = TRUE
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()["total"]


def listar_medicos(connection, limit, offset):
    query = """
        SELECT m.id, u.nombre, u.apellido, u.email,
               m.especialidad_id, e.nombre AS especialidad
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        JOIN especialidades e ON e.id = m.especialidad_id
        WHERE u.activo = TRUE
        ORDER BY u.apellido, u.nombre
        LIMIT %s OFFSET %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()