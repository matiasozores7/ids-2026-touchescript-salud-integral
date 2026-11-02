
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


def actualizar_usuario_por_id(connection, usuario_id: int, usuario_data: dict) -> None:
    query = """
        UPDATE usuarios
        SET nombre = %s, apellido = %s, email = %s
        WHERE id = %s
    """
    values = (
        usuario_data.get("nombre"),
        usuario_data.get("apellido"),
        usuario_data.get("email"),
        usuario_id
    )

    with connection.cursor() as cursor:
        cursor.execute(query, values)


def desactivar_usuario_por_id(connection, usuario_id: int) -> None:
    query = """
        UPDATE usuarios
        SET activo = FALSE
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id,))
