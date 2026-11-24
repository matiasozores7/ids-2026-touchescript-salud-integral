from types import MappingProxyType


class ReglasTurno:
    ESTADO_DISPONIBLE = "disponible"
    ESTADO_RESERVADO = "reservado"
    ESTADO_CONFIRMADO = "confirmado"
    ESTADO_EN_CONSULTA = "en_consulta"
    ESTADO_ATENDIDO = "atendido"
    ESTADO_CANCELADO = "cancelado"
    ESTADO_AUSENTE = "ausente"

    ESTADOS_VALIDOS = (
        ESTADO_DISPONIBLE,
        ESTADO_RESERVADO,
        ESTADO_CONFIRMADO,
        ESTADO_EN_CONSULTA,
        ESTADO_ATENDIDO,
        ESTADO_CANCELADO,
        ESTADO_AUSENTE,
    )

    TRANSICIONES_VALIDAS = MappingProxyType({
        ESTADO_DISPONIBLE: frozenset((ESTADO_RESERVADO, ESTADO_CANCELADO)),
        ESTADO_RESERVADO: frozenset((
            ESTADO_CONFIRMADO, ESTADO_CANCELADO, ESTADO_AUSENTE, ESTADO_DISPONIBLE,
        )),
        ESTADO_CONFIRMADO: frozenset((
            ESTADO_EN_CONSULTA, ESTADO_ATENDIDO, ESTADO_CANCELADO, ESTADO_AUSENTE,
        )),
        ESTADO_EN_CONSULTA: frozenset((ESTADO_ATENDIDO,)),
        ESTADO_ATENDIDO: frozenset(),
        ESTADO_CANCELADO: frozenset((ESTADO_DISPONIBLE,)),
        ESTADO_AUSENTE: frozenset((ESTADO_DISPONIBLE,)),
    })

    DIAS_SEMANA_MAPA = MappingProxyType({
        0: "Lunes",
        1: "Martes",
        2: "Miercoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sabado",
        6: "Domingo",
    })

    VENTANA_CHECKIN_MINUTOS = 15
