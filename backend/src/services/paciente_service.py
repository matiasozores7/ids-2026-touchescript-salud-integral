from werkzeug.security import generate_password_hash
from src.database.connection import transaction
from src.repositories.usuario_repository import (
    buscar_usuario_por_email,
    crear_usuario,
    actualizar_usuario_por_id,
    desactivar_usuario_por_id
)
from src.repositories.paciente_repository import (
    obtener_todos_los_pacientes,
    insertar_paciente,
    actualizar_paciente_por_id,
    obtener_usuario_id_por_paciente_id,
    buscar_paciente_por_id
)
from src.validators.paciente_validator import validar_datos_paciente, validar_datos_actualizacion_paciente
from src.errors.exceptions import NotFoundError, ConflictError


def obtener_pacientes_service() -> list:
    with transaction() as connection:
        return obtener_todos_los_pacientes(connection)


def crear_paciente_service(data: dict) -> int:
    validar_datos_paciente(data)

    email_clean = data.get("email").strip().lower()

    with transaction() as connection:
        usuario_existente = buscar_usuario_por_email(connection, email_clean)
        if usuario_existente:
            raise ConflictError(
                message="El correo electrónico ya se encuentra registrado.",
                description="Ya existe un usuario registrado con ese correo electrónico."
            )

        password_hash = generate_password_hash(data.get("password"))
        usuario_id = crear_usuario(
            connection,
            data.get("nombre").strip(),
            data.get("apellido").strip(),
            email_clean,
            password_hash
        )
        cobertura_id = data.get("cobertura_id")
        nuevo_id_paciente = insertar_paciente(connection, usuario_id, cobertura_id)

    return nuevo_id_paciente


def actualizar_paciente_service(paciente_id: int, data: dict) -> None:
    validar_datos_actualizacion_paciente(data)

    with transaction() as connection:
        usuario_id = obtener_usuario_id_por_paciente_id(connection, paciente_id)

        if not usuario_id:
            raise NotFoundError(description=f"El paciente con ID {paciente_id} no existe.")

        actualizar_usuario_por_id(connection, usuario_id, data)
        actualizar_paciente_por_id(connection, paciente_id, data.get("cobertura_id"))


def eliminar_paciente_service(paciente_id: int) -> None:
    with transaction() as connection:
        paciente = buscar_paciente_por_id(connection, paciente_id)

        if not paciente:
            raise NotFoundError(description=f"El paciente con ID {paciente_id} no existe.")

        if not paciente.get("activo"):
            raise NotFoundError(description=f"El paciente con ID {paciente_id} ya se encuentra dado de baja.")

        desactivar_usuario_por_id(connection, paciente.get("usuario_id"))
