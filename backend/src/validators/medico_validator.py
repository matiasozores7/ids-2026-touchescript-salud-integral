import re
from src.constants import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_TEXTO_LENGTH,
    REGEX_EMAIL,
)
from src.errors.exceptions import BadRequestError


def validar_creacion(data):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )

    for campo in ["nombre", "apellido", "email", "password"]:
        valor = data.get(campo)
        if not isinstance(valor, str) or not valor.strip():
            raise BadRequestError(
                description=f"El campo '{campo}' es obligatorio.",
                message="Faltan campos obligatorios."
            )

    for campo in ["nombre", "apellido", "email"]:
        if len(data[campo].strip()) > MAX_TEXTO_LENGTH:
            raise BadRequestError(
                description=f"El campo '{campo}' no puede superar los {MAX_TEXTO_LENGTH} caracteres."
            )

    if not re.fullmatch(REGEX_EMAIL, data["email"].strip()):
        raise BadRequestError(description="El formato del email no es válido.")

    if not MIN_PASSWORD_LENGTH <= len(data["password"]) <= MAX_PASSWORD_LENGTH:
        raise BadRequestError(
            description=(
                f"La contraseña debe tener entre "
                f"{MIN_PASSWORD_LENGTH} y {MAX_PASSWORD_LENGTH} caracteres."
            )
        )

    _validar_especialidad_id(data.get("especialidad_id"))


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