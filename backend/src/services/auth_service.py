from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from src.repositories import usuario_repository as usuario_repo
from src.repositories import paciente_repository as paciente_repo
from src.repositories import medico_repository as medico_repo
from src.repositories import registro_repository as registro_repo
from src.repositories import token_repository as token_repo
from src.errors.exceptions import APIError, ConflictError, UnauthorizedError
from datetime import datetime, timezone

def registrar_paciente(
    nombre: str,
    apellido: str,
    email: str,
    password: str,
    cobertura_id: int = None
) -> dict:
    email_clean = email.strip().lower()

    usuario_existente = usuario_repo.buscar_usuario_por_email(email_clean)

    if usuario_existente:
        raise ConflictError(
            message="El correo electrónico ya se encuentra registrado.",
            description="Ya existe un usuario registrado con ese correo electrónico."
        )

    password_hash = generate_password_hash(password)

    nuevo_usuario = registro_repo.crear_usuario_y_paciente(
        nombre=nombre.strip(),
        apellido=apellido.strip(),
        email=email_clean,
        password_hash=password_hash,
        cobertura_id=cobertura_id
    )

    return nuevo_usuario


def login_usuario(email: str, password: str) -> dict:
    email_clean = email.strip().lower()

    usuario = usuario_repo.buscar_usuario_por_email(email_clean)

    if not usuario or not check_password_hash(
        usuario["password_hash"], password
    ):
        raise UnauthorizedError(
            description="El correo electrónico o la contraseña son incorrectos.",
            message="Credenciales inválidas."
        )

    perfil_id = None

    if usuario["rol"] == "paciente":
        perfil = paciente_repo.buscar_paciente_por_usuario_id(
            usuario["id"]
        )

    elif usuario["rol"] == "medico":
        perfil = medico_repo.buscar_medico_por_usuario_id(
            usuario["id"]
        )

    elif usuario["rol"] == "admin":
        perfil = None

    else:
        raise APIError(
            code="INVALID_ROLE",
            message="El rol del usuario no es válido.",
            description="El usuario tiene un rol no reconocido.",
            status_code=500
        )

    if usuario["rol"] in ("paciente", "medico"):
        if perfil is None:
            raise APIError(
                code="PROFILE_NOT_FOUND",
                message="No se encontró el perfil del usuario.",
                description="Existe una cuenta sin su perfil asociado.",
                status_code=500
            )

        perfil_id = perfil["id"]

    access_token = create_access_token(
        identity=str(usuario["id"]),
        additional_claims={
            "rol": usuario["rol"],
            "perfil_id": perfil_id
        }
    )

    return {
        "access_token": access_token,
        "usuario_id": usuario["id"],
        "nombre": usuario["nombre"],
        "apellido": usuario["apellido"],
        "email": usuario["email"],
        "rol": usuario["rol"],
        "perfil_id": perfil_id
    }

def logout_usuario(jti: str, exp: int) -> None:
    fecha_expiracion = datetime.fromtimestamp(
        exp,
        tz=timezone.utc
    ).replace(tzinfo=None)

    token_repo.revocar_token(
        jti=jti,
        fecha_expiracion=fecha_expiracion
    )