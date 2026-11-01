from src.errors.exceptions import BadRequestError


def validar_creacion(data: dict):
    _validar_tipo_data(data)

    numero_sala = data.get("numero_sala")
    if not isinstance(numero_sala, str) or not numero_sala.strip():
        raise BadRequestError(
            description="El campo numero_sala es obligatorio y debe ser un texto."
        )

    piso = data.get("piso")
    if piso is not None and not isinstance(piso, str):
        raise BadRequestError(
            description="El campo piso debe ser un texto."
        )


def validar_actualizacion(data: dict):
    _validar_tipo_data(data)

    numero_sala = data.get("numero_sala")
    if not isinstance(numero_sala, str) or not numero_sala.strip():
        raise BadRequestError(
            description="El campo numero_sala es obligatorio y debe ser un texto."
        )

    piso = data.get("piso")
    if piso is not None and not isinstance(piso, str):
        raise BadRequestError(
            description="El campo piso debe ser un texto."
        )


def _validar_tipo_data(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )
