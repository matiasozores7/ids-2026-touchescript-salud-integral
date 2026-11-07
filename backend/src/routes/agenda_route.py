from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services import agenda_service
from src.validators import agenda_validator
from src.utils.decorators import roles_requeridos
from src.utils.responses import success_response


agenda_bp = Blueprint("agendas", __name__)


@agenda_bp.route("/agendas", methods=["POST"])
@jwt_required()
@roles_requeridos("admin")
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
@jwt_required()
def listar_agendas_medico(medico_id):
    resultado = agenda_service.listar_por_medico(medico_id)

    return success_response(
        data=resultado,
        message="Agendas del médico"
    )



@agenda_bp.route("/agendas/<int:agenda_id>", methods=["PUT"])
@jwt_required()
@roles_requeridos("admin")
def actualizar_agenda(agenda_id):
    datos = request.get_json() or {}
    agenda_validator.validar(datos)

    resultado = agenda_service.actualizar_agenda(agenda_id, datos)

    return success_response(
        data=resultado,
        message="Agenda actualizada exitosamente"
    )


@agenda_bp.route("/agendas/<int:agenda_id>", methods=["DELETE"])
@jwt_required()
@roles_requeridos("admin")
def eliminar_agenda(agenda_id):
    agenda_service.eliminar_agenda(agenda_id)

    return success_response(message="Agenda eliminada exitosamente")







