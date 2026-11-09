class AppError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(AppError):
    def __init__(self, message):
        super().__init__(message, 400)


class AuthenticationError(AppError):
    def __init__(self, message="Debés iniciar sesión."):
        super().__init__(message, 401)


class ForbiddenError(AppError):
    def __init__(self, message="No tenés permisos para realizar esta operación."):
        super().__init__(message, 403)


class NotFoundError(AppError):
    def __init__(self, message="Recurso no encontrado."):
        super().__init__(message, 404)


class ConflictError(AppError):
    def __init__(self, message):
        super().__init__(message, 409)


class ExternalServiceError(AppError):
    def __init__(self, message="No se pudo completar la operación."):
        super().__init__(message, 502)


class ServiceUnavailableError(AppError):
    def __init__(self, message="El servicio no está disponible."):
        super().__init__(message, 503)


class ServiceTimeoutError(AppError):
    def __init__(self, message="El servicio tardó demasiado en responder."):
        super().__init__(message, 504)