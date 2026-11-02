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
