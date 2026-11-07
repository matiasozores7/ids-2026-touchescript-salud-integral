from datetime import datetime
from src.errors.exceptions import BadRequestError


DIAS_VALIDOS = {
    "Lunes", "Martes", "Miercoles", "Jueves",
    "Viernes", "Sabado", "Domingo"
}


def validar(datos):
    requeridos = {
        "medico_id", "consultorio_id", "dia_semana",
        "hora_inicio", "hora_fin", "duracion_turno"
    }

    faltantes = requeridos - datos.keys()
    if faltantes:
        raise BadRequestError(
            description=f"Faltan campos requeridos: {', '.join(faltantes)}."
        )

    if datos["dia_semana"] not in DIAS_VALIDOS:
        raise BadRequestError(description="El día de la semana no es válido.")

    try:
        inicio = datetime.strptime(datos["hora_inicio"], "%H:%M:%S")
        fin = datetime.strptime(datos["hora_fin"], "%H:%M:%S")
    except (TypeError, ValueError):
        raise BadRequestError(
            description="Las horas deben tener el formato HH:MM:SS."
        )

    if inicio >= fin:
        raise BadRequestError(
            description="La hora de inicio debe ser menor que la hora de fin."
        )

    if not isinstance(datos["duracion_turno"], int) or datos["duracion_turno"] <= 0:
        raise BadRequestError(
            description="La duración del turno debe ser un entero positivo."
        )

    if not isinstance(datos["medico_id"], int) or datos["medico_id"] <= 0:
        raise BadRequestError(description="El médico no es válido.")

    if not isinstance(datos["consultorio_id"], int) or datos["consultorio_id"] <= 0:
        raise BadRequestError(description="El consultorio no es válido.")