from src.errors.exceptions import BadRequestError


def _validar_campos_requeridos(data: dict, campos: list):
    for campo in campos:
        valor = data.get(campo)

        if not isinstance(valor, str) or not valor.strip():
            raise BadRequestError(
                description=f"El campo '{campo}' es obligatorio.",
                message="Faltan campos obligatorios."
            )


def validar_datos_paciente(data: dict):
    if not data:
        raise BadRequestError(
            description="El cuerpo de la petición (JSON) está vacío.",
            message="Faltan campos obligatorios."
        )

    _validar_campos_requeridos(data, ["nombre", "apellido", "email", "password"])

    if not data.get("cobertura_id"):
        raise BadRequestError(
            description="El campo 'cobertura_id' es obligatorio.",
            message="Faltan campos obligatorios."
        )


def validar_datos_actualizacion_paciente(data: dict):
    if not data:
        raise BadRequestError(
            description="El cuerpo de la petición (JSON) está vacío.",
            message="Faltan campos obligatorios."
        )

    _validar_campos_requeridos(data, ["nombre", "apellido", "email"])

    if not data.get("cobertura_id"):
        raise BadRequestError(
            description="El campo 'cobertura_id' es obligatorio.",
            message="Faltan campos obligatorios."
        )
