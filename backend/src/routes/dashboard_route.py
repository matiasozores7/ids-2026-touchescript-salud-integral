from flask import Blueprint, jsonify, request
from src.database.connection import transaction
from src.services.dashboard_service import (
    obtener_sala_espera_service,
    obtener_turnos_por_medico_especialidad_service,
    obtener_ocupacion_consultorios_service,
    obtener_ausentismo_service,
    obtener_tiempo_espera_service
)

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard/sala-espera', methods=['GET'])
def get_sala_espera():
    try:
        fecha = request.args.get('fecha')

        with transaction() as connection:
            pacientes = obtener_sala_espera_service(connection, fecha)

        return jsonify(pacientes), 200

    except Exception as e:
        print(f"¡ERROR INTERNO INESPERADO EN SALA DE ESPERA!: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/dashboard/turnos-por-medico-especialidad', methods=['GET'])
def get_turnos_por_medico_especialidad():
    try:
        fecha = request.args.get('fecha')

        with transaction() as connection:
            reporte = obtener_turnos_por_medico_especialidad_service(connection, fecha)

        return jsonify(reporte), 200

    except Exception as e:
        print(f"¡ERROR INTERNO INESPERADO EN TURNOS POR MEDICO Y ESPECIALIDAD!: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/dashboard/ocupacion-consultorios', methods=['GET'])
def get_ocupacion_consultorios():
    try:
        fecha = request.args.get('fecha')

        with transaction() as connection:
            reporte = obtener_ocupacion_consultorios_service(connection, fecha)

        return jsonify(reporte), 200

    except Exception as e:
        print(f"¡ERROR INTERNO INESPERADO EN OCUPACION DE CONSULTORIOS!: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/dashboard/ausentismo', methods=['GET'])
def get_ausentismo():
    try:
        fecha = request.args.get('fecha')

        with transaction() as connection:
            reporte = obtener_ausentismo_service(connection, fecha)

        return jsonify(reporte), 200

    except Exception as e:
        print(f"¡ERROR INTERNO INESPERADO EN AUSENTISMO!: {str(e)}")
        return jsonify({"error": str(e)}), 500


@dashboard_bp.route('/dashboard/tiempo-espera', methods=['GET'])
def get_tiempo_espera():
    try:
        fecha = request.args.get('fecha')

        with transaction() as connection:
            reporte = obtener_tiempo_espera_service(connection, fecha)

        return jsonify(reporte), 200

    except Exception as e:
        print(f"¡ERROR INTERNO INESPERADO EN TIEMPO DE ESPERA!: {str(e)}")
        return jsonify({"error": str(e)}), 500
