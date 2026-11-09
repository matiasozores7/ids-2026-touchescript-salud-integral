from src.database.connection import transaction
from src.errors.exceptions import ConflictError, NotFoundError
from src.repositories import coberturas_repository as coberturas_repo


def listar_coberturas(limit: int, offset: int):
    with transaction() as connection:
        total = coberturas_repo.contar_coberturas(connection)

        items = coberturas_repo.listar_coberturas(
            connection,
            limit,
            offset
        )

    return items, total


def obtener_cobertura(cobertura_id: int):
    with transaction() as connection:
        cobertura = coberturas_repo.buscar_cobertura(
            connection,
            cobertura_id
        )

        if cobertura is None:
            raise NotFoundError(description="La cobertura no existe.")

    return cobertura


def crear_cobertura(nombre: str) -> int:
    with transaction() as connection:
        if coberturas_repo.existe_nombre(connection, nombre):
            raise ConflictError(
                description="Ya existe una cobertura con ese nombre."
            )

        cobertura_id = coberturas_repo.crear_cobertura(
            connection,
            nombre
        )

    return cobertura_id


def actualizar_cobertura(cobertura_id: int, nombre: str) -> None:
    with transaction() as connection:
        cobertura = coberturas_repo.buscar_cobertura(
            connection,
            cobertura_id
        )

        if cobertura is None:
            raise NotFoundError(description="La cobertura no existe.")

        if coberturas_repo.existe_nombre(
            connection,
            nombre,
            excluir_id=cobertura_id
        ):
            raise ConflictError(
                description="Ya existe otra cobertura con ese nombre."
            )

        coberturas_repo.actualizar_cobertura(
            connection,
            cobertura_id,
            nombre
        )


def eliminar_cobertura(cobertura_id: int) -> None:
    with transaction() as connection:
        cobertura = coberturas_repo.buscar_cobertura(
            connection,
            cobertura_id
        )

        if cobertura is None:
            raise NotFoundError(description="La cobertura no existe.")

        if coberturas_repo.contar_pacientes(
            connection,
            cobertura_id
        ) > 0:
            raise ConflictError(
                description=(
                    "No se puede eliminar la cobertura porque está "
                    "asignada a uno o más pacientes."
                )
            )

        coberturas_repo.eliminar_cobertura(
            connection,
            cobertura_id
        )