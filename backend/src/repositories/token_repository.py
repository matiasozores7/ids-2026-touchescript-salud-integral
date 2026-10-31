
def revocar_token(connection, jti: str, fecha_expiracion):
    query = """
        INSERT INTO tokens_revocados (jti, fecha_expiracion)
        VALUES (%s, %s)
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (jti, fecha_expiracion))


def esta_revocado(connection, jti: str) -> bool:
    query = """
        SELECT jti
        FROM tokens_revocados
        WHERE jti = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (jti,))
        resultado = cursor.fetchone()

        return resultado is not None
