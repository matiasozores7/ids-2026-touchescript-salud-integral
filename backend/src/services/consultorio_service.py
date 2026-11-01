from src.database.connection import get_db_connection
from src.repositories import consultorio_repository as consultorio_repo


def listar_consultorios():
    connection = get_db_connection()

    try:
        return consultorio_repo.listar_consultorios_activos(connection)
    finally:
        connection.close()


def crear_consultorio(numero_sala: str, piso: str | None) -> int:
    connection = get_db_connection()

    try:
        consultorio_id = consultorio_repo.crear_consultorio(
            connection,
            numero_sala=numero_sala,
            piso=piso
        )
        connection.commit()
        return consultorio_id
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
