from flask import Blueprint, request
from src.utils.responses import success_response
from src.utils.decorators import validar_rol
from src.services.dashboard_service import (
    obtener_sala_espera_service,
    obtener_turnos_por_medico_especialidad_service,
    obtener_ocupacion_consultorios_service,
    obtener_ausentismo_service,
    obtener_tiempo_espera_service,
    obtener_turnos_hoy_service
)

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/dashboard/sala-espera", methods=["GET"])
@validar_rol("admin")
def get_sala_espera():
    fecha = request.args.get("fecha")
    pacientes = obtener_sala_espera_service(fecha)
    return success_response(data=pacientes, message="Sala de espera obtenida correctamente.")


@dashboard_bp.route("/dashboard/turnos-por-medico-especialidad", methods=["GET"])
@validar_rol("admin")
def get_turnos_por_medico_especialidad():
    fecha = request.args.get("fecha")
    reporte = obtener_turnos_por_medico_especialidad_service(fecha)
    return success_response(data=reporte, message="Turnos por médico y especialidad obtenidos correctamente.")


@dashboard_bp.route("/dashboard/ocupacion-consultorios", methods=["GET"])
@validar_rol("admin")
def get_ocupacion_consultorios():
    fecha = request.args.get("fecha")
    reporte = obtener_ocupacion_consultorios_service(fecha)
    return success_response(data=reporte, message="Ocupación de consultorios obtenida correctamente.")


@dashboard_bp.route("/dashboard/ausentismo", methods=["GET"])
@validar_rol("admin")
def get_ausentismo():
    fecha = request.args.get("fecha")
    reporte = obtener_ausentismo_service(fecha)
    return success_response(data=reporte, message="Reporte de ausentismo obtenido correctamente.")


@dashboard_bp.route("/dashboard/tiempo-espera", methods=["GET"])
@validar_rol("admin")
def get_tiempo_espera():
    fecha = request.args.get("fecha")
    reporte = obtener_tiempo_espera_service(fecha)
    return success_response(data=reporte, message="Tiempo de espera obtenido correctamente.")

@dashboard_bp.route("/dashboard/turnos-hoy", methods=["GET"])
@validar_rol("admin")
def get_turnos_hoy():
    estadisticas = obtener_turnos_hoy_service()

    return success_response(
        data=estadisticas,
        message="Estadísticas de turnos de hoy obtenidas correctamente."
    )