from flask import Blueprint, request

from src.services import agenda_service
from src.validators import agenda_validator
from src.utils.decorators import validar_token, validar_rol
from src.utils.responses import success_response


agenda_bp = Blueprint("agendas", __name__)


@agenda_bp.route("/agendas", methods=["POST"])
@validar_rol("admin")
def crear_agenda():
    datos = request.get_json() or {}
    agenda_validator.validar(datos)

    resultado = agenda_service.crear_agenda(datos)

    return success_response(
        data=resultado,
        message="Agenda creada exitosamente",
        status_code=201
    )


@agenda_bp.route("/medicos/<int:medico_id>/agendas", methods=["GET"])
@validar_token
def listar_agendas_medico(medico_id):
    resultado = agenda_service.listar_por_medico(medico_id)

    return success_response(
        data=resultado,
        message="Agendas del médico"
    )



@agenda_bp.route("/agendas/<int:agenda_id>", methods=["PUT"])
@validar_rol("admin")
def actualizar_agenda(agenda_id):
    datos = request.get_json() or {}
    agenda_validator.validar(datos)

    resultado = agenda_service.actualizar_agenda(agenda_id, datos)

    return success_response(
        data=resultado,
        message="Agenda actualizada exitosamente"
    )


@agenda_bp.route("/agendas/<int:agenda_id>", methods=["DELETE"])
@validar_rol("admin")
def eliminar_agenda(agenda_id):
    agenda_service.eliminar_agenda(agenda_id)

    return success_response(message="Agenda eliminada exitosamente")







