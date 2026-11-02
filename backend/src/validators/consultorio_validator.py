from src.errors.exceptions import BadRequestError

MAX_TEXTO_LENGTH = 20


def validar_creacion(data: dict):
    _validar_tipo_data(data)

    numero_sala = data.get("numero_sala")
    if not isinstance(numero_sala, str) or not numero_sala.strip():
        raise BadRequestError(
            description="El campo numero_sala es obligatorio y debe ser un texto."
        )
    _validar_largo("numero_sala", numero_sala)

    piso = data.get("piso")
    if piso is not None and not isinstance(piso, str):
        raise BadRequestError(
            description="El campo piso debe ser un texto."
        )
    if piso is not None:
        _validar_largo("piso", piso)


def validar_actualizacion(data: dict):
    _validar_tipo_data(data)

    numero_sala = data.get("numero_sala")
    if not isinstance(numero_sala, str) or not numero_sala.strip():
        raise BadRequestError(
            description="El campo numero_sala es obligatorio y debe ser un texto."
        )
    _validar_largo("numero_sala", numero_sala)

    piso = data.get("piso")
    if piso is not None and not isinstance(piso, str):
        raise BadRequestError(
            description="El campo piso debe ser un texto."
        )
    if piso is not None:
        _validar_largo("piso", piso)


def _validar_tipo_data(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )


def _validar_largo(campo: str, valor: str):
    if len(valor.strip()) > MAX_TEXTO_LENGTH:
        raise BadRequestError(
            description=(
                f"El campo '{campo}' no puede superar los "
                f"{MAX_TEXTO_LENGTH} caracteres."
            )
        )
