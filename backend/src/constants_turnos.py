# Constantes y reglas para el módulo de turnos

ESTADO_DISPONIBLE = "disponible"
ESTADO_RESERVADO = "reservado"
ESTADO_CONFIRMADO = "confirmado"
ESTADO_ATENDIDO = "atendido"
ESTADO_CANCELADO = "cancelado"
ESTADO_AUSENTE = "ausente"

ESTADOS_VALIDOS = (
    ESTADO_DISPONIBLE,
    ESTADO_RESERVADO,
    ESTADO_CONFIRMADO,
    ESTADO_ATENDIDO,
    ESTADO_CANCELADO,
    ESTADO_AUSENTE,
)

# Matriz de transiciones válidas según el ciclo de vida de un turno
TRANSICIONES_VALIDAS = {
    ESTADO_DISPONIBLE: {ESTADO_RESERVADO, ESTADO_CANCELADO},
    ESTADO_RESERVADO: {ESTADO_CONFIRMADO, ESTADO_CANCELADO, ESTADO_AUSENTE, ESTADO_DISPONIBLE},
    ESTADO_CONFIRMADO: {ESTADO_ATENDIDO, ESTADO_CANCELADO, ESTADO_AUSENTE},
    ESTADO_ATENDIDO: set(),  # Estado terminal
    ESTADO_CANCELADO: {ESTADO_DISPONIBLE},  # Permite reapertura manual por administración
    ESTADO_AUSENTE: {ESTADO_DISPONIBLE},   # Permite reapertura manual por administración
}
