
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

def contar_pacientes(connection) -> int:
    query = """
        SELECT COUNT(*) AS total
        FROM pacientes
        INNER JOIN usuarios ON pacientes.usuario_id = usuarios.id
        WHERE usuarios.activo = 1
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchone()["total"]


def listar_pacientes(connection, limit: int, offset: int) -> list:
    query = """
        SELECT
            pacientes.id AS paciente_id,
            usuarios.id AS usuario_id,
            usuarios.nombre AS nombre,
            usuarios.apellido AS apellido,
            usuarios.email AS email,
            usuarios.telefono AS telefono,
            coberturas.nombre AS cobertura_medica
        FROM pacientes
        INNER JOIN usuarios ON pacientes.usuario_id = usuarios.id
        LEFT JOIN coberturas ON pacientes.cobertura_id = coberturas.id
        WHERE usuarios.activo = 1
        ORDER BY usuarios.apellido, usuarios.nombre, pacientes.id
        LIMIT %s OFFSET %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()

def insertar_paciente(connection, usuario_id: int, cobertura_id: int) -> int:
    cursor = connection.cursor()
    query = """
        INSERT INTO pacientes (usuario_id, cobertura_id) 
        VALUES (%s, %s)
    """
    values = (usuario_id, cobertura_id)
    
    cursor.execute(query, values)
    paciente_id = cursor.lastrowid
    cursor.close()
    
    return paciente_id

def obtener_usuario_id_por_paciente_id(connection, paciente_id: int) -> int | None:
    query = "SELECT usuario_id FROM pacientes WHERE id = %s"
    
    with connection.cursor() as cursor:
        cursor.execute(query, (paciente_id,))
        resultado = cursor.fetchone()
    if resultado:
        return resultado.get("usuario_id")
    return None

def buscar_paciente_por_id(connection, paciente_id: int) -> dict | None:
    query = """
        SELECT
            pacientes.id AS paciente_id,
            pacientes.usuario_id,
            pacientes.cobertura_id,
            usuarios.nombre,
            usuarios.apellido,
            usuarios.email,
            usuarios.telefono,
            usuarios.activo
        FROM pacientes
        INNER JOIN usuarios ON pacientes.usuario_id = usuarios.id
        WHERE pacientes.id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (paciente_id,))
        return cursor.fetchone()

def actualizar_paciente_por_id(connection, paciente_id: int, cobertura_id: int) -> None:
    cursor = connection.cursor()
    query = """
        UPDATE pacientes 
        SET cobertura_id = %s 
        WHERE id = %s
    """
    values = (cobertura_id, paciente_id)
    cursor.execute(query, values)
    cursor.close()