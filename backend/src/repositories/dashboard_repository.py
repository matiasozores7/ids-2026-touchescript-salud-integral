def obtener_pacientes_en_sala_espera(connection, fecha: str | None = None):
    query = """
        SELECT 
            turnos.id AS turno_id,
            turnos.fecha_hora AS fecha_hora_turno,
            turnos.fecha_hora_llegada,
            turnos.estado,
            
            -- Datos del Paciente
            paciente_usuario.id AS paciente_usuario_id,
            paciente_usuario.nombre AS paciente_nombre,
            paciente_usuario.apellido AS paciente_apellido,
            
            -- Datos del Médico y su Especialidad
            medico_usuario.id AS medico_usuario_id,
            medico_usuario.nombre AS medico_nombre,
            medico_usuario.apellido AS medico_apellido,
            especialidades.nombre AS especialidad,
            
            -- Consultorio y Ubicación
            consultorios.numero_sala AS consultorio_sala,
            consultorios.piso AS consultorio_piso

        FROM turnos
        INNER JOIN pacientes ON turnos.paciente_id = pacientes.id
        INNER JOIN usuarios AS paciente_usuario ON pacientes.usuario_id = paciente_usuario.id
        INNER JOIN medicos ON turnos.medico_id = medicos.id
        INNER JOIN usuarios AS medico_usuario ON medicos.usuario_id = medico_usuario.id
        INNER JOIN especialidades ON medicos.especialidad_id = especialidades.id
        INNER JOIN consultorios ON turnos.consultorio_id = consultorios.id
        WHERE turnos.estado = 'confirmado'
          AND paciente_usuario.rol = 'paciente'
          AND medico_usuario.rol = 'medico'
          AND paciente_usuario.activo = 1
    """
    params = []

    if fecha:
        query += " AND DATE(turnos.fecha_hora) = %s"
        params.append(fecha)
    else:
        query += " AND DATE(turnos.fecha_hora) = CURDATE()"

    query += " ORDER BY turnos.fecha_hora_llegada ASC;"

    with connection.cursor() as cursor:
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
