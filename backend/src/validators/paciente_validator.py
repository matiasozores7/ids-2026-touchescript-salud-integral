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
    _validar_telefono(data)

    if not data.get("cobertura_id"):
        raise BadRequestError(
            description="El campo 'cobertura_id' es obligatorio.",
            message="Faltan campos obligatorios."
        )


def validar_datos_actualizacion_paciente(data: dict):
    if not isinstance(data, dict) or not data:
        raise BadRequestError(
            description="El cuerpo de la petición debe contener al menos un campo modificable."
        )

    campos_modificables = [
        "nombre", "apellido", "email", "telefono", "cobertura_id"
    ]

    if not any(campo in data for campo in campos_modificables):
        raise BadRequestError(
            description="Debe enviar al menos un campo modificable."
        )

    _validar_campos_requeridos(
        data,
        [campo for campo in ["nombre", "apellido", "email"] if campo in data]
    )
    _validar_telefono(data)

    if "cobertura_id" in data:
        cobertura_id = data["cobertura_id"]

        if not isinstance(cobertura_id, int) or isinstance(cobertura_id, bool) or cobertura_id <= 0:
            raise BadRequestError(
                description="El campo 'cobertura_id' debe ser un identificador válido."
            )


def _validar_telefono(data: dict):
    telefono = data.get("telefono")
    if telefono is not None and (
        not isinstance(telefono, str) or not telefono.strip()
    ):
        raise BadRequestError(
            description="El campo 'telefono' debe ser texto no vacío."
        )
    if isinstance(telefono, str) and len(telefono.strip()) > 30:
        raise BadRequestError(
            description="El teléfono no puede superar los 30 caracteres."
        )