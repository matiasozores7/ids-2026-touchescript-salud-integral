from flask import Blueprint, jsonify, request
from src.database.connection import transaction
from src.repositories.paciente_repository import obtener_todos_los_pacientes
from src.services.paciente_service import crear_paciente_service

pacientes_bp = Blueprint('pacientes_bp', __name__)


@pacientes_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        with transaction() as connection:
            pacientes = obtener_todos_los_pacientes(connection)
           
        return jsonify(pacientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@pacientes_bp.route('/pacientes', methods=['POST'])
def post_paciente():
    respuesta_json = None
    codigo_estado = 200

    try:
        data = request.get_json()
        
        with transaction() as conexion:
            nuevo_id = crear_paciente_service(conexion, data)
        
        respuesta_json = jsonify({
            "mensaje": "Paciente creado con éxito",
            "id": nuevo_id
        })
        codigo_estado = 201

    except ValueError as ve:
        respuesta_json = jsonify({"error": str(ve)})
        codigo_estado = 400

    except Exception as e:
        print(f"¡ERROR INTERNO INESPERADO!: {str(e)}")
        respuesta_json = jsonify({"error": str(e)})
        codigo_estado = 500

    return respuesta_json, codigo_estado