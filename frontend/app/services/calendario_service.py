def preparar_datos_calendario(turnos: list[dict]) -> dict:
    turnos_preparados = []
    especialidades = {}
    medicos = {}

    for turno in turnos:
        fecha_hora = turno.get("fecha_hora") or ""

        paciente = " ".join(
            filter(None, [
                turno.get("paciente_nombre"),
                turno.get("paciente_apellido"),
            ])
        ) or "Sin paciente asignado"

        medico = " ".join(
            filter(None, [
                turno.get("medico_nombre"),
                turno.get("medico_apellido"),
            ])
        )

        especialidad_id = turno.get("especialidad_id")
        especialidad = turno.get("especialidad") or "Sin especialidad"

        medico_id = turno.get("medico_id")

        if especialidad_id is not None:
            especialidades[especialidad_id] = especialidad

        if medico_id is not None:
            medicos[medico_id] = medico

        turnos_preparados.append({
            "id": turno.get("turno_id"),
            "dateKey": fecha_hora[:10],
            "time": fecha_hora[11:16],
            "patient": paciente,
            "doctor": medico,
            "doctorId": medico_id,
            "specialtyId": especialidad_id,
            "specialty": especialidad,
            "office": turno.get("consultorio_sala") or "—",
            "status": turno.get("estado"),
        })

    especialidades_preparadas = [
        {"id": id, "name": nombre}
        for id, nombre in especialidades.items()
    ]

    medicos_preparados = [
        {"id": id, "name": nombre}
        for id, nombre in medicos.items()
    ]

    especialidades_preparadas.sort(key=lambda item: item["name"].casefold())
    medicos_preparados.sort(key=lambda item: item["name"].casefold())

    return {
        "turnos": turnos_preparados,
        "especialidades": especialidades_preparadas,
        "medicos": medicos_preparados,
    }
