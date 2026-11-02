def obtener_medico_activo(connection, medico_id):
    query = """
        SELECT m.id
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        WHERE m.id = %s AND u.activo = TRUE
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        return cursor.fetchone()


def obtener_consultorio_activo(connection, consultorio_id):
    query = "SELECT id FROM consultorios WHERE id = %s AND activo = TRUE"
    with connection.cursor() as cursor:
        cursor.execute(query, (consultorio_id,))
        return cursor.fetchone()


def existe_conflicto(connection, datos, agenda_id=None):
    query = """
        SELECT id
        FROM agendas
        WHERE dia_semana = %s
          AND (
                (medico_id = %s AND hora_inicio < %s AND hora_fin > %s)
                OR
                (consultorio_id = %s AND hora_inicio < %s AND hora_fin > %s)
              )
    """
    params = (
        datos["dia_semana"],
        datos["medico_id"], datos["hora_fin"], datos["hora_inicio"],
        datos["consultorio_id"], datos["hora_fin"], datos["hora_inicio"]
    )

    if agenda_id:
        query += " AND id <> %s"
        params += (agenda_id,)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchone() is not None


def crear(connection, datos):
    query = """
        INSERT INTO agendas
        (medico_id, consultorio_id, dia_semana, hora_inicio, hora_fin, duracion_turno)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (
            datos["medico_id"], datos["consultorio_id"],
            datos["dia_semana"], datos["hora_inicio"],
            datos["hora_fin"], datos["duracion_turno"]
        ))
        return cursor.lastrowid


def obtener(connection, agenda_id):
    query = """
        SELECT a.id, a.medico_id, a.consultorio_id, a.dia_semana,
               a.hora_inicio, a.hora_fin, a.duracion_turno,
               c.numero_sala, c.piso
        FROM agendas a
        JOIN consultorios c ON c.id = a.consultorio_id
        WHERE a.id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (agenda_id,))
        return cursor.fetchone()


def listar_por_medico(connection, medico_id):
    query = """
        SELECT a.id, a.medico_id, a.consultorio_id, a.dia_semana,
               a.hora_inicio, a.hora_fin, a.duracion_turno,
               c.numero_sala, c.piso
        FROM agendas a
        JOIN consultorios c ON c.id = a.consultorio_id
        WHERE a.medico_id = %s
        ORDER BY FIELD(
            a.dia_semana,
            'Lunes', 'Martes', 'Miercoles', 'Jueves',
            'Viernes', 'Sabado', 'Domingo'
        ), a.hora_inicio
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (medico_id,))
        return cursor.fetchall()


def actualizar(connection, agenda_id, datos):
    query = """
        UPDATE agendas
        SET medico_id = %s,
            consultorio_id = %s,
            dia_semana = %s,
            hora_inicio = %s,
            hora_fin = %s,
            duracion_turno = %s
        WHERE id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (
            datos["medico_id"], datos["consultorio_id"],
            datos["dia_semana"], datos["hora_inicio"],
            datos["hora_fin"], datos["duracion_turno"],
            agenda_id
        ))


def eliminar(connection, agenda_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM agendas WHERE id = %s", (agenda_id,))
def listar_medicos_por_especialidad(connection, especialidad_id):
    query = """
        SELECT m.id, u.nombre, u.apellido, u.email,
               e.id AS especialidad_id, e.nombre AS especialidad
        FROM medicos m
        JOIN usuarios u ON u.id = m.usuario_id
        JOIN especialidades e ON e.id = m.especialidad_id
        WHERE m.especialidad_id = %s
          AND u.activo = TRUE
        ORDER BY u.apellido, u.nombre
    """
    with connection.cursor() as cursor:
        cursor.execute(query, (especialidad_id,))
        return cursor.fetchall()


def existe_especialidad(connection, especialidad_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id FROM especialidades WHERE id = %s",
            (especialidad_id,)
        )
        return cursor.fetchone() is not None