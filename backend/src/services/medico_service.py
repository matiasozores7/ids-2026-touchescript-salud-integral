from src.database.connection import transaction
from src.repositories import medico_repository as medico_repo


def listar_medicos(limit: int, offset: int):
    with transaction() as connection:
        total = medico_repo.contar_medicos(connection)
        items = medico_repo.listar_medicos(connection, limit, offset)

    return items, total