from src.errors.exceptions import BadRequestError


def validar_creacion(data: dict):
    _validar_data(data)
    _validar_nombre(data)


def validar_actualizacion(data: dict):
    _validar_data(data)
    _validar_nombre(data)


def _validar_data(data: dict):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )


def _validar_nombre(data: dict):
    nombre = data.get("nombre")

    if not isinstance(nombre, str) or not nombre.strip():
        raise BadRequestError(
            description="El nombre de la cobertura es obligatorio."
        )

    if len(nombre.strip()) > 100:
        raise BadRequestError(
            description="El nombre no puede superar los 100 caracteres."
        )