import re
from src.constants import (
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_TEXTO_LENGTH,
    REGEX_EMAIL,
)
from src.errors.exceptions import BadRequestError

CAMPOS_MODIFICABLES = [
    "nombre", "apellido", "email", "telefono", "especialidad_id",
    "matricula", "cobertura_ids"
]


def validar_creacion(data):
    _validar_tipo_data(data)
    _validar_campos_obligatorios(
        data,
        ["nombre", "apellido", "email", "password", "matricula"]
    )
    _validar_telefono(data)
    _validar_datos_personales(data)
    _validar_matricula(data["matricula"])
    _validar_password(data["password"])
    _validar_especialidad_id(data.get("especialidad_id"))
    _validar_cobertura_ids(data.get("cobertura_ids", []))


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
    _validar_telefono(data)
    _validar_datos_personales(data)

    if "matricula" in data:
        _validar_matricula(data["matricula"])

    if "especialidad_id" in data:
        _validar_especialidad_id(data["especialidad_id"])

    if "cobertura_ids" in data:
        _validar_cobertura_ids(data["cobertura_ids"])


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
    for campo in ["nombre", "apellido", "email", "telefono"]:
        if campo == "telefono" and data.get(campo) is None:
            continue
        if campo in data and len(data[campo].strip()) > MAX_TEXTO_LENGTH:
            raise BadRequestError(
                description=f"El campo '{campo}' no puede superar los {MAX_TEXTO_LENGTH} caracteres."
            )

    if "email" in data and not re.fullmatch(REGEX_EMAIL, data["email"].strip()):
        raise BadRequestError(description="El formato del email no es válido.")


def _validar_telefono(data):
    telefono = data.get("telefono")
    if telefono is not None and (
        not isinstance(telefono, str) or not telefono.strip()
    ):
        raise BadRequestError(
            description="El campo 'telefono' debe ser texto no vacío."
        )


def _validar_matricula(matricula):
    if not isinstance(matricula, str) or not matricula.strip():
        raise BadRequestError(
            description="El campo 'matricula' es obligatorio."
        )
    if len(matricula.strip()) > 50:
        raise BadRequestError(
            description="La matrícula no puede superar los 50 caracteres."
        )


def _validar_cobertura_ids(cobertura_ids):
    if not isinstance(cobertura_ids, list):
        raise BadRequestError(
            description="El campo 'cobertura_ids' debe ser una lista."
        )

    ids_vistos = set()
    for cobertura_id in cobertura_ids:
        if (
            isinstance(cobertura_id, bool)
            or not isinstance(cobertura_id, int)
            or cobertura_id <= 0
        ):
            raise BadRequestError(
                description=(
                    "Cada elemento de 'cobertura_ids' debe ser un "
                    "identificador entero positivo."
                )
            )
        if cobertura_id in ids_vistos:
            raise BadRequestError(
                description="La lista de coberturas no debe contener duplicados."
            )
        ids_vistos.add(cobertura_id)


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