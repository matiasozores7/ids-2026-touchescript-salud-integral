from flask import Flask

from config import Config
from app.routes.auth_route import auth_bp
from app.routes.patient import patient_bp
from app.routes.backoffice import backoffice_bp
from app.routes.cancelacion_route import cancelacion_bp
from app.context_processors import inject_now
from app.utils.error_handlers import register_error_handlers

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    app.context_processor(inject_now)
    register_error_handlers(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(backoffice_bp)
    app.register_blueprint(cancelacion_bp)

    return app