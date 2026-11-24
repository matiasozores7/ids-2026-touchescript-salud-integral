class Roles:
    PACIENTE = "paciente"
    MEDICO = "medico"
    ADMIN = "admin"

    @classmethod
    def validos(cls) -> frozenset[str]:
        return frozenset((cls.PACIENTE, cls.MEDICO, cls.ADMIN))