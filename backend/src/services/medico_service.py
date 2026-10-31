from werkzeug.security import generate_password_hash

from src.database.connection import transaction
from src.errors.exceptions import BadRequestError, ConflictError
from src.repositories import medico_repository as medico_repo
from src.repositories import usuario_repository as usuario_repo


def listar_medicos(limit: int, offset: int):
    with transaction() as connection:
        total = medico_repo.contar_medicos(connection)
        items = medico_repo.listar_medicos(connection, limit, offset)

    return items, total


def crear_medico(nombre, apellido, email, password, especialidad_id) -> dict:
    email_clean = email.strip().lower()
    password_hash = generate_password_hash(password)

    with transaction() as connection:
        if usuario_repo.buscar_usuario_por_email(connection, email_clean):
            raise ConflictError(
                message="El correo electrónico ya se encuentra registrado.",
                description="Ya existe un usuario registrado con ese correo electrónico."
            )

        if not medico_repo.existe_especialidad(connection, especialidad_id):
            raise BadRequestError(
                description="La especialidad indicada no existe."
            )

        usuario_id = usuario_repo.crear_usuario(
            connection, nombre.strip(), apellido.strip(),
            email_clean, password_hash, rol="medico"
        )
        medico_id = medico_repo.crear_medico(connection, usuario_id, especialidad_id)
        medico = medico_repo.obtener_medico_por_id(connection, medico_id)

    medico.pop("activo", None)
    return medico