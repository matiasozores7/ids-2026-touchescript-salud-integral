from src.database.connection import execute_query

def revocar_token(jti: str, fecha_expiracion):
    query = """
        INSERT INTO tokens_revocados (jti, fecha_expiracion)
        VALUES (%s, %s)
    """

    execute_query(query, (jti, fecha_expiracion))

def esta_revocado(jti: str) -> bool:
    query = """
        SELECT jti
        FROM tokens_revocados
        WHERE jti = %s
    """

    resultado = execute_query(query, (jti,), fetch_one=True)

    return resultado is not None