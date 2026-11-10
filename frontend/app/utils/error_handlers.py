import logging

from flask import render_template
from werkzeug.exceptions import HTTPException

from app.errors.exceptions import AppError

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return render_template(
            "errors/error.html",
            message=error.message,
            status_code=error.status_code
        ), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return render_template(
            "errors/error.html",
            message=error.description,
            status_code=error.code
        ), error.code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        logger.exception("Error inesperado en el frontend")

        return render_template(
            "errors/error.html",
            message="Ocurrió un error interno. Intentá nuevamente.",
            status_code=500
        ), 500