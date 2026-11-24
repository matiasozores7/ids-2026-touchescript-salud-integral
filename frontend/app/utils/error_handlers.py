import logging

from flask import render_template
from werkzeug.exceptions import HTTPException

from app.errors.exceptions import (
    AppError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
)

logger = logging.getLogger(__name__)


def register_error_handlers(app):

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        return render_template(
            "errors/401.html",
            message=error.message,
        ), 401

    @app.errorhandler(ForbiddenError)
    def handle_forbidden_error(error):
        return render_template(
            "errors/403.html",
            message=error.message,
        ), 403

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(error):
        return render_template(
            "errors/404.html",
            message=error.message,
        ), 404

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return render_template(
            "errors/error.html",
            message=error.message,
            status_code=error.status_code
        ), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        if error.code == 403:
            return render_template(
                "errors/403.html",
                message="No tenés permisos para acceder a esta sección.",
            ), 403

        if error.code == 404:
            return render_template(
                "errors/404.html",
                message="La página que buscás no existe.",
            ), 404

        if error.code == 401:
            return render_template(
                "errors/401.html",
                message="Debés iniciar sesión para acceder.",
            ), 401

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