from src.database.connection import get_db_connection
from src.repositories import usuario_repository as usuario_repo
from src.repositories import paciente_repository as paciente_repo
from src.repositories import medico_repository as medico_repo

def crear_usuario_y_paciente(
    nombre: str,
    apellido: str,
    email: str,
    password_hash: str,
    cobertura_id: int = None
):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            usuario_id = usuario_repo.crear_usuario(
                cursor, nombre, apellido, email, password_hash, rol="paciente"
            )

            paciente_id = paciente_repo.crear_paciente(
                cursor, usuario_id, cobertura_id
            )

        connection.commit()

        return {
            "usuario_id": usuario_id,
            "paciente_id": paciente_id,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "rol": "paciente"
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def crear_usuario_y_medico(
    nombre: str,
    apellido: str,
    email: str,
    password_hash: str,
    especialidad_id: int
) -> dict:

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:

            usuario_id = usuario_repo.crear_usuario(
                cursor,
                nombre,
                apellido,
                email,
                password_hash,
                rol="medico"
            )

            medico_id = medico_repo.crear_medico(
                cursor,
                usuario_id,
                especialidad_id
            )

        connection.commit()

        return {
            "usuario_id": usuario_id,
            "medico_id": medico_id,
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "rol": "medico"
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()