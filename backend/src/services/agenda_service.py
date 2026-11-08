from src.database.connection import transaction
from src.errors.exceptions import BadRequestError, ConflictError, NotFoundError
from src.repositories import agendas_repository as agenda_repo
from datetime import timedelta


def _validar_referencias(connection, datos):
    if not agenda_repo.obtener_medico_activo(connection, datos["medico_id"]):
        raise NotFoundError(description="El médico no existe o está inactivo.")

    if not agenda_repo.obtener_consultorio_activo(connection, datos["consultorio_id"]):
        raise NotFoundError(description="El consultorio no existe o está inactivo.")


def crear_agenda(datos):
    with transaction() as connection:
        _validar_referencias(connection, datos)

        if agenda_repo.existe_conflicto(connection, datos):
            raise ConflictError(
                message="Existe un conflicto de horario.",
                description="El médico o consultorio ya tiene una agenda en ese horario."
            )

        agenda_id = agenda_repo.crear(connection, datos)
        return agenda_id


def _serializar_agenda(agenda):
    if not agenda:
        return agenda

    agenda = dict(agenda)

    for campo in ("hora_inicio", "hora_fin"):
        valor = agenda.get(campo)

        if isinstance(valor, timedelta):
            total_segundos = int(valor.total_seconds())
            horas, resto = divmod(total_segundos, 3600)
            minutos, segundos = divmod(resto, 60)
            agenda[campo] = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    return agenda


def listar_por_medico(medico_id):
    with transaction() as connection:
        if not agenda_repo.obtener_medico_activo(connection, medico_id):
            raise NotFoundError(
                description="El médico no existe o está inactivo."
            )

        agendas = agenda_repo.listar_por_medico(connection, medico_id)
        return [_serializar_agenda(agenda) for agenda in agendas]


def actualizar_agenda(agenda_id, datos):
    with transaction() as connection:
        if not agenda_repo.obtener(connection, agenda_id):
            raise NotFoundError(description="La agenda no existe.")

        _validar_referencias(connection, datos)

        if agenda_repo.existe_conflicto(connection, datos, agenda_id):
            raise ConflictError(
                message="Existe un conflicto de horario.",
                description="El médico o consultorio ya tiene una agenda en ese horario."
            )

        agenda_repo.actualizar(connection, agenda_id, datos)


def eliminar_agenda(agenda_id):
    with transaction() as connection:
        if not agenda_repo.obtener(connection, agenda_id):
            raise NotFoundError(description="La agenda no existe.")

        agenda_repo.eliminar(connection, agenda_id)


def listar_medicos_por_especialidad(especialidad_id):
    with transaction() as connection:
        if not agenda_repo.existe_especialidad(connection, especialidad_id):
            raise NotFoundError(description="La especialidad no existe.")

        return agenda_repo.listar_medicos_por_especialidad(
            connection, especialidad_id
        )