import re
from src.constants import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_TEXTO_LENGTH,
    REGEX_EMAIL,
)
from src.errors.exceptions import BadRequestError

CAMPOS_MODIFICABLES = ["nombre", "apellido", "email", "especialidad_id"]


def validar_creacion(data):
    _validar_tipo_data(data)
    _validar_campos_obligatorios(data, ["nombre", "apellido", "email", "password"])
    _validar_datos_personales(data)
    _validar_password(data["password"])
    _validar_especialidad_id(data.get("especialidad_id"))


def validar_modificacion_parcial(data):
    _validar_tipo_data(data)

    if not any(campo in data for campo in CAMPOS_MODIFICABLES):
        raise BadRequestError(
            description=f"Debe enviar al menos uno de estos campos: {', '.join(CAMPOS_MODIFICABLES)}."
        )

    # Solo se validan los campos de texto que efectivamente llegaron
    _validar_campos_obligatorios(
        data, [c for c in ["nombre", "apellido", "email"] if c in data]
    )
    _validar_datos_personales(data)

    if "especialidad_id" in data:
        _validar_especialidad_id(data["especialidad_id"])


def _validar_tipo_data(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )


def _validar_campos_obligatorios(data, campos):
    for campo in campos:
        valor = data.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            raise BadRequestError(
                description=f"El campo '{campo}' es obligatorio.",
                message="Faltan campos obligatorios."
            )


def _validar_datos_personales(data):
    # Largo máximo según las columnas VARCHAR(100) de la tabla usuarios
    for campo in ["nombre", "apellido", "email"]:
        if campo in data and len(data[campo].strip()) > MAX_TEXTO_LENGTH:
            raise BadRequestError(
                description=f"El campo '{campo}' no puede superar los {MAX_TEXTO_LENGTH} caracteres."
            )

    if "email" in data and not re.fullmatch(REGEX_EMAIL, data["email"].strip()):
        raise BadRequestError(description="El formato del email no es válido.")


def _validar_password(password):
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise BadRequestError(
            description=(
                f"La contraseña debe tener entre "
                f"{MIN_PASSWORD_LENGTH} y {MAX_PASSWORD_LENGTH} caracteres."
            )
        )


def _validar_especialidad_id(especialidad_id):
    # bool es subclase de int, por eso se descarta explícitamente
    if (
        isinstance(especialidad_id, bool)
        or not isinstance(especialidad_id, int)
        or especialidad_id <= 0
    ):
        raise BadRequestError(
            description="El campo 'especialidad_id' es obligatorio y debe ser un entero positivo."
        )