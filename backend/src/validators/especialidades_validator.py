from src.errors.exceptions import BadRequestError
from src.constants import MAX_TEXTO_LENGTH


def validar_creacion(data):
    _validar_datos(data)


def validar_actualizacion(data):
    _validar_datos(data)


def _validar_datos(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )

    nombre = data.get("nombre")
    if not isinstance(nombre, str) or not nombre.strip():
        raise BadRequestError(
            description="El campo nombre es obligatorio y debe ser un texto."
        )

    if len(nombre.strip()) > MAX_TEXTO_LENGTH:
        raise BadRequestError(
            description=(
                f"El campo 'nombre' no puede superar los "
                f"{MAX_TEXTO_LENGTH} caracteres."
            )
        )

    descripcion = data.get("descripcion")
    if descripcion is not None and not isinstance(descripcion, str):
        raise BadRequestError(
            description="El campo descripcion debe ser un texto."
        )
