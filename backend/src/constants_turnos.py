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

    @classmethod
    def transiciones_validas(cls) -> dict:
        return {
            cls.ESTADO_DISPONIBLE: (
                cls.ESTADO_RESERVADO,
                cls.ESTADO_CANCELADO,
            ),
            cls.ESTADO_RESERVADO: (
                cls.ESTADO_CONFIRMADO,
                cls.ESTADO_CANCELADO,
                cls.ESTADO_AUSENTE,
                cls.ESTADO_DISPONIBLE,
            ),
            cls.ESTADO_CONFIRMADO: (
                cls.ESTADO_EN_CONSULTA,
                cls.ESTADO_ATENDIDO,
                cls.ESTADO_CANCELADO,
                cls.ESTADO_AUSENTE,
            ),
            cls.ESTADO_EN_CONSULTA: (cls.ESTADO_ATENDIDO,),
            cls.ESTADO_ATENDIDO: (),
            cls.ESTADO_CANCELADO: (cls.ESTADO_DISPONIBLE,),
            cls.ESTADO_AUSENTE: (cls.ESTADO_DISPONIBLE,),
        }

    @classmethod
    def dias_semana(cls) -> dict:
        return {
            0: "Lunes",
            1: "Martes",
            2: "Miercoles",
            3: "Jueves",
            4: "Viernes",
            5: "Sabado",
            6: "Domingo",
        }

    VENTANA_CHECKIN_MINUTOS = 15
