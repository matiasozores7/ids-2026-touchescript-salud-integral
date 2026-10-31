
def buscar_usuario_por_email(connection, email: str):
    query = """
        SELECT id, nombre, apellido, email, password_hash, rol, activo
        FROM usuarios
        WHERE email = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (email,))
        return cursor.fetchone()


def crear_usuario(connection, nombre, apellido, email, password_hash, rol="paciente"):
    query = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, rol)
        VALUES (%s, %s, %s, %s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (nombre, apellido, email, password_hash, rol))
        return cursor.lastrowid