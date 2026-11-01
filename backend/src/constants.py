API_VERSION = "v1"
STATUS_ACTIVE = "active"
STATUS_INACTIVE = "inactive"

HEALTH_OK_MESSAGE = "API Backend activa"

# Validaciones de usuarios (nombre, apellido y email son VARCHAR(100) en la tabla usuarios)
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
MAX_TEXTO_LENGTH = 100
REGEX_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"