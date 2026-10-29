from flask import Flask
from config import Config
from src.routes import health_bp
from src.utils.error_handlers import register_error_handlers

app = Flask(__name__)
app.config.from_object(Config)

register_error_handlers(app)
app.register_blueprint(health_bp)
# Cuando agreguen blueprints agreguen el url_prefix="/api" 
# para cumplir con la convención del listado

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(app.config['PORT']), debug=True)