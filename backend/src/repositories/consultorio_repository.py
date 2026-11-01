def listar_consultorios_activos(connection):
    query = """
        SELECT id, numero_sala, piso, activo
        FROM consultorios
        WHERE activo = TRUE
        ORDER BY id
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
