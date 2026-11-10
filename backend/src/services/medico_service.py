from werkzeug.security import generate_password_hash

from src.database.connection import transaction
from src.errors.exceptions import BadRequestError, ConflictError, NotFoundError
from src.repositories import medico_repository as medico_repo
from src.repositories import usuario_repository as usuario_repo


def _a_respuesta(medico: dict) -> dict:
    # Campos internos que no se exponen al cliente
    medico.pop("activo", None)
    medico.pop("usuario_id", None)
    return medico


def _obtener_medico_activo(connection, medico_id: int) -> dict:
    medico = medico_repo.obtener_medico_por_id(connection, medico_id)

    if medico is None or not medico["activo"]:
        raise NotFoundError(
            description="No existe un médico activo con ese identificador."
        )

    return medico


def listar_medicos(limit: int, offset: int):
    with transaction() as connection:
        total = medico_repo.contar_medicos(connection)
        items = medico_repo.listar_medicos(connection, limit, offset)

    return items, total


def obtener_medico(medico_id: int) -> dict:
    with transaction() as connection:
        medico = _obtener_medico_activo(connection, medico_id)

    return _a_respuesta(medico)


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

    return medico_id


def modificar_medico(medico_id: int, datos: dict) -> None:
    with transaction() as connection:
        medico = _obtener_medico_activo(connection, medico_id)

        nombre = datos["nombre"].strip() if "nombre" in datos else medico["nombre"]
        apellido = datos["apellido"].strip() if "apellido" in datos else medico["apellido"]
        email = medico["email"]
        especialidad_id = datos.get("especialidad_id", medico["especialidad_id"])

        if "email" in datos:
            email = datos["email"].strip().lower()
            usuario_con_email = usuario_repo.buscar_usuario_por_email(connection, email)

            # Si el email ya existe pero es de otro usuario, hay conflicto
            if usuario_con_email and usuario_con_email["id"] != medico["usuario_id"]:
                raise ConflictError(
                    message="El correo electrónico ya se encuentra registrado.",
                    description="Ya existe un usuario registrado con ese correo electrónico."
                )

        if "especialidad_id" in datos and not medico_repo.existe_especialidad(connection, especialidad_id):
            raise BadRequestError(
                description="La especialidad indicada no existe."
            )

        medico_repo.actualizar_medico(
            connection, medico_id, medico["usuario_id"],
            nombre, apellido, email, especialidad_id
        )


def eliminar_medico(medico_id: int) -> None:
    with transaction() as connection:
        medico = _obtener_medico_activo(connection, medico_id)

        if medico_repo.contar_turnos_pendientes(connection, medico_id) > 0:
            raise ConflictError(
                message="No se puede dar de baja al médico.",
                description="El médico tiene turnos reservados o confirmados pendientes."
            )

        medico_repo.desactivar_usuario(connection, medico["usuario_id"])


def listar_por_especialidad(especialidad_id: int):
    with transaction() as connection:
        return medico_repo.listar_por_especialidad(
            connection,
            especialidad_id
        )