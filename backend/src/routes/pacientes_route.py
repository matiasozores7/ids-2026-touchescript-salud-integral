from flask import Blueprint, jsonify
from src.database.connection import transaction
from src.repositories.paciente_repository import obtener_todos_los_pacientes


pacientes_bp = Blueprint('pacientes_bp', __name__)


@pacientes_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        with transaction() as connection:
            pacientes = obtener_todos_los_pacientes(connection)
           
        return jsonify(pacientes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

