from flask import Flask
from config import Config
from src.routes import health_bp
from src.routes import auth_bp
from src.utils.error_handlers import register_error_handlers
from src.utils.jwt_config import configurar_jwt

app = Flask(__name__)
app.config.from_object(Config)

configurar_jwt(app)
register_error_handlers(app)

app.register_blueprint(health_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(app.config['PORT']), debug=True)