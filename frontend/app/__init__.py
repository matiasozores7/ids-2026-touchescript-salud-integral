from flask import Flask

from config import Config
from app.routes.auth_route import auth_bp
from app.routes.patient_route import patient_bp
from app.routes.backoffice import backoffice_bp

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(backoffice_bp)

    return app