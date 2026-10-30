import re 
from src.errors.exceptions import BadRequestError

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
REGEX_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def validar_registro(data: dict):
    _validar_tipo_data(data)
    campos_requeridos = ["email", "password", "nombre", "apellido"]
    _validar_campos_requeridos(data, campos_requeridos)
    _validar_email(data["email"])
    _validar_password(data["password"])
    _validar_cobertura(data.get("cobertura_id")) # Si no se utiliza get y no existe ese campo lanza excepción, por eso lo hago mediante la función get

def validar_login(data: dict):
    _validar_tipo_data(data)
    campos_requeridos = ["email", "password"]
    _validar_campos_requeridos(data, campos_requeridos)
    _validar_email(data["email"])

def _validar_tipo_data(data: dict):
    if not isinstance(data, dict):
        raise BadRequestError(
            description="El cuerpo de la solicitud debe ser un objeto JSON."
        )

def _validar_campos_requeridos(data: dict, campos: list):
    for campo in campos:
        valor = data.get(campo)

        if not isinstance(valor, str) or not valor.strip():
            raise BadRequestError(
                description=f"El campo '{campo}' es obligatorio.",
                message="Faltan campos obligatorios."
            )

def _validar_email(email: str):
    if not re.fullmatch(REGEX_EMAIL, email.strip()):
        raise BadRequestError(
            description="El formato del email no es válido."
        )

def _validar_password(password: str):
    if not MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH:
        raise BadRequestError(
            description=(
                f"La contraseña debe tener entre "
                f"{MIN_PASSWORD_LENGTH} y {MAX_PASSWORD_LENGTH} caracteres."
            )
        )

def _validar_cobertura(cobertura_id : int | None):
    if cobertura_id is None:
        return

    if ( 
         # bool es una subclase de int en Python
         # Sin esta comprobación True y False pasarían como enteros
        isinstance(cobertura_id, bool)
        or not isinstance(cobertura_id, int)
        or cobertura_id <= 0
    ):
        raise BadRequestError(
            description="El identificador de cobertura no es válido."
        )