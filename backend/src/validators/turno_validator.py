from datetime import datetime
from src.constants_turnos import ESTADOS_VALIDOS
from src.errors.exceptions import BadRequestError


def _validar_tipo_diccionario(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )


def validar_actualizacion_estado(data: dict) -> None:
    _validar_tipo_diccionario(data)

    estado = data.get("estado")
    if not isinstance(estado, str) or not estado.strip():
        raise BadRequestError(
            description="El campo 'estado' es obligatorio y debe ser un texto."
        )

    estado_limpio = estado.strip().lower()
    if estado_limpio not in ESTADOS_VALIDOS:
        raise BadRequestError(
            description=(
                f"El estado '{estado}' no es válido. Estados permitidos: "
                f"{', '.join(ESTADOS_VALIDOS)}."
            )
        )


def validar_generacion_turnos(data: dict) -> None:
    _validar_tipo_diccionario(data)

    fecha_inicio_str = data.get("fecha_inicio")
    fecha_fin_str = data.get("fecha_fin")

    if not isinstance(fecha_inicio_str, str) or not fecha_inicio_str.strip():
        raise BadRequestError(
            description="El campo 'fecha_inicio' es obligatorio y debe tener formato YYYY-MM-DD."
        )

    if not isinstance(fecha_fin_str, str) or not fecha_fin_str.strip():
        raise BadRequestError(
            description="El campo 'fecha_fin' es obligatorio y debe tener formato YYYY-MM-DD."
        )

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise BadRequestError(
            description="El formato de 'fecha_inicio' debe ser YYYY-MM-DD."
        )

    try:
        fecha_fin = datetime.strptime(fecha_fin_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise BadRequestError(
            description="El formato de 'fecha_fin' debe ser YYYY-MM-DD."
        )

    if fecha_inicio > fecha_fin:
        raise BadRequestError(
            description="La 'fecha_inicio' no puede ser posterior a la 'fecha_fin'."
        )

    medico_id = data.get("medico_id")
    if medico_id is not None:
        if not isinstance(medico_id, int) or medico_id <= 0:
            raise BadRequestError(
                description="El campo 'medico_id' debe ser un número entero positivo."
            )
