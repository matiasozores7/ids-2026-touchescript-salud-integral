from flask import Blueprint
from src.constants import HEALTH_OK_MESSAGE

health_bp = Blueprint('health', __name__)


@health_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {
        'status': 'ok',
        'message': HEALTH_OK_MESSAGE
    }, 200
