from src.database.connection import execute_query, get_db_connection

def buscar_usuario_por_email(email: str):
    query = """
        SELECT id, nombre, apellido, email, password_hash, rol
        FROM usuarios
        WHERE email = %s
    """
    return execute_query(query, (email,), fetch_one=True)

def crear_usuario(cursor, nombre, apellido, email, password_hash, rol="paciente"):
    query = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, rol)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (nombre, apellido, email, password_hash, rol))
    return cursor.lastrowid