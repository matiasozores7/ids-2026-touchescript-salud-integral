
def buscar_usuario_por_email(connection, email: str):
    query = """
        SELECT id, nombre, apellido, email, password_hash, rol, activo
        FROM usuarios
        WHERE email = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (email,))
        return cursor.fetchone()


def crear_usuario(connection, usuario_data: dict) -> int:
    cursor = connection.cursor()
    query = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, rol, activo) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    values = (
        usuario_data.get("nombre"),
        usuario_data.get("apellido"),
        usuario_data.get("email"),
        usuario_data.get("password"),
        "paciente",
        True
    )
    
    cursor.execute(query, values)
    usuario_id = cursor.lastrowid
    cursor.close()
    
    return usuario_id

def actualizar_usuario_por_id(connection, usuario_id: int, usuario_data: dict) -> None:
    cursor = connection.cursor()
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
    cursor.execute(query, values)
    cursor.close()

def desactivar_usuario_por_id(connection, usuario_id: int) -> None:
    query = """
        UPDATE usuarios 
        SET activo = FALSE 
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (usuario_id,))
