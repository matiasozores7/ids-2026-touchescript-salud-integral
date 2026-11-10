from src.database.connection import transaction
from src.errors.exceptions import ConflictError, NotFoundError
from src.repositories import especialidades_repository as especialidades_repo


def listar_especialidades(limit: int, offset: int):
    with transaction() as connection:
        total = especialidades_repo.contar_especialidades(connection)
        items = especialidades_repo.listar_especialidades(
            connection,
            limit,
            offset
        )

    return items, total


def crear_especialidad(nombre: str, descripcion: str | None) -> int:
    with transaction() as connection:
        if especialidades_repo.existe_nombre(connection, nombre):
            raise ConflictError(
                description="Ya existe una especialidad con ese nombre."
            )

        especialidad_id = especialidades_repo.crear_especialidad(
            connection,
            nombre=nombre,
            descripcion=descripcion
        )

    return especialidad_id


def actualizar_especialidad(
    especialidad_id: int,
    nombre: str,
    descripcion: str | None
) -> None:
    with transaction() as connection:
        especialidad = especialidades_repo.buscar_especialidad(
            connection,
            especialidad_id
        )

        if especialidad is None:
            raise NotFoundError(description="La especialidad no existe.")

        especialidades_repo.actualizar_especialidad(
            connection,
            especialidad_id=especialidad_id,
            nombre=nombre,
            descripcion=descripcion
        )


def eliminar_especialidad(especialidad_id: int) -> None:
    with transaction() as connection:
        especialidad = especialidades_repo.buscar_especialidad(
            connection,
            especialidad_id
        )

        if especialidad is None:
            raise NotFoundError(description="La especialidad no existe.")

        if especialidades_repo.contar_medicos(connection, especialidad_id) > 0:
            raise ConflictError(
                description=(
                    "No se puede eliminar la especialidad porque está "
                    "asignada a uno o más médicos."
                )
            )

        especialidades_repo.eliminar_especialidad(connection, especialidad_id)
