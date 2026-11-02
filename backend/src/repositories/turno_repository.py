def obtener_turno_por_id(connection, turno_id: int):
    query = """
        SELECT id, medico_id, paciente_id, consultorio_id, fecha_hora, fecha_hora_llegada, estado, qr_token
        FROM turnos
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (turno_id,))
        return cursor.fetchone()


def actualizar_estado_turno(connection, turno_id: int, nuevo_estado: str) -> int:
    query = """
        UPDATE turnos
        SET estado = %s
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (nuevo_estado, turno_id))
        return cursor.rowcount
