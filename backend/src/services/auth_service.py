from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from src.database.connection import transaction

from src.repositories import usuario_repository as usuario_repo
from src.repositories import paciente_repository as paciente_repo
from src.repositories import medico_repository as medico_repo
from src.repositories import token_repository as token_repo
from src.errors.exceptions import (APIError, ConflictError, UnauthorizedError)
from datetime import datetime, timezone

def _normalizar_email(email: str) -> str:
    return email.strip().lower()

def _obtener_perfil(connection, usuario: dict) -> int | None:
    repositorios = {
        "paciente": paciente_repo.buscar_paciente_por_usuario_id,
        "medico": medico_repo.buscar_medico_por_usuario_id
    }

    rol = usuario["rol"]

    if rol == "admin":
        return None

    buscar_perfil = repositorios.get(rol)

    if buscar_perfil is None:
        raise APIError(
            code="INVALID_ROLE",
            message="El rol del usuario no es válido.",
            description="El usuario tiene un rol no reconocido.",
            status_code=500
        )

    perfil = buscar_perfil(connection, usuario["id"])

    if perfil is None:
        raise APIError(
            code="PROFILE_NOT_FOUND",
            message="No se encontró el perfil del usuario.",
            description="Existe una cuenta sin su perfil asociado.",
            status_code=500
        )

    return perfil["id"]

def _generar_access_token(usuario_id: int, rol: str, perfil_id: int | None) -> str:
    return create_access_token(
        identity=str(usuario_id),
        additional_claims={
            "rol": rol,
            "perfil_id": perfil_id
        }
    )

def registrar_paciente(nombre: str, apellido: str, email: str, password: str, cobertura_id: int | None = None) -> dict:
    email_clean = _normalizar_email(email)
    password_hash = generate_password_hash(password)

    with transaction() as connection:
        usuario_existente = usuario_repo.buscar_usuario_por_email(connection, email_clean)

        if usuario_existente:
            raise ConflictError(
                message="El correo electrónico ya se encuentra registrado.",
                description="Ya existe un usuario registrado con ese correo electrónico."
            )

        usuario_id = usuario_repo.crear_usuario(connection, nombre.strip(), apellido.strip(), email_clean, password_hash)
        paciente_id = paciente_repo.crear_paciente(connection, usuario_id, cobertura_id)

    access_token = _generar_access_token(usuario_id=usuario_id, rol="paciente", perfil_id=paciente_id)

    return {"access_token": access_token}

def login_usuario(email: str, password: str) -> dict:
    email_clean = _normalizar_email(email)

    with transaction() as connection:
        usuario = usuario_repo.buscar_usuario_por_email(connection, email_clean)

        if not usuario or not check_password_hash(usuario["password_hash"], password):
            raise UnauthorizedError(
                description="El correo electrónico o la contraseña son incorrectos.",
                message="Credenciales inválidas."
            )

        if not usuario["activo"]:
            raise UnauthorizedError(
                description="Tu cuenta se encuentra desactivada. Contactá con administración.",
                message="Cuenta desactivada."
            )

        perfil_id = _obtener_perfil(connection, usuario)

    access_token = _generar_access_token(usuario_id=usuario["id"], rol=usuario["rol"], perfil_id=perfil_id)

    return {"access_token": access_token}

def logout_usuario(jti: str, exp: int) -> None:
    fecha_expiracion = datetime.fromtimestamp(exp, tz=timezone.utc).replace(tzinfo=None)

    with transaction() as connection:
        token_repo.revocar_token(connection, jti, fecha_expiracion)