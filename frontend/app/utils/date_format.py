from datetime import datetime


def nombre_dia(fecha: datetime, *, capitalizado: bool = True) -> str:
    dias = (
        "lunes", "martes", "miércoles", "jueves",
        "viernes", "sábado", "domingo",
    )
    nombre = dias[fecha.weekday()]
    return nombre.capitalize() if capitalizado else nombre


def nombre_mes(fecha: datetime) -> str:
    meses = (
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre",
        "diciembre",
    )
    return meses[fecha.month]


def nombre_dia_corto(fecha: datetime) -> str:
    return nombre_dia(fecha)[:3]


def fecha_larga(fecha: datetime) -> str:
    return f"{nombre_dia(fecha)} {fecha.day} de {nombre_mes(fecha)}"
