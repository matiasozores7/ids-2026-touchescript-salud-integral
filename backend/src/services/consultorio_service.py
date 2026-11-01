from src.database.connection import get_db_connection
from src.errors.exceptions import NotFoundError
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


def actualizar_consultorio(
    consultorio_id: int,
    numero_sala: str,
    piso: str | None
) -> None:
    connection = get_db_connection()

    try:
        consultorio = consultorio_repo.buscar_consultorio_activo(
            connection,
            consultorio_id
        )

        if consultorio is None:
            raise NotFoundError(
                description="El consultorio no existe o se encuentra inactivo."
            )

        consultorio_repo.actualizar_consultorio(
            connection,
            consultorio_id=consultorio_id,
            numero_sala=numero_sala,
            piso=piso
        )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
