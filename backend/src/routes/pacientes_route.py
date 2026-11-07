from flask import Blueprint, request
from src.utils.responses import success_response
from src.utils.decorators import validar_rol
from src.services.paciente_service import (
    crear_paciente_service,
    actualizar_paciente_service,
    eliminar_paciente_service,
    obtener_pacientes_service
)

pacientes_bp = Blueprint("pacientes_bp", __name__)


@pacientes_bp.route("/pacientes", methods=["GET"])
@validar_rol("admin")
def get_pacientes():
    pacientes = obtener_pacientes_service()
    return success_response(data=pacientes, message="Pacientes obtenidos correctamente.")


@pacientes_bp.route("/pacientes", methods=["POST"])
@validar_rol("admin")
def post_paciente():
    data = request.get_json() or {}
    nuevo_id = crear_paciente_service(data)
    return success_response(data={"id": nuevo_id}, message="Paciente creado con éxito.", status_code=201)


@pacientes_bp.route("/pacientes/<int:paciente_id>", methods=["PUT"])
@validar_rol("admin")
def put_paciente(paciente_id):
    data = request.get_json() or {}
    actualizar_paciente_service(paciente_id, data)
    return success_response(message=f"Paciente con ID {paciente_id} actualizado con éxito.")


@pacientes_bp.route("/pacientes/<int:paciente_id>", methods=["DELETE"])
@validar_rol("admin")
def delete_paciente(paciente_id):
    eliminar_paciente_service(paciente_id)
    return success_response(message=f"Paciente con ID {paciente_id} dado de baja con éxito.")
