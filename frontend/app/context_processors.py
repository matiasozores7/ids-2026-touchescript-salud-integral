from datetime import datetime


def inject_now():
    ahora = datetime.now()

    dias = [
        "lunes", "martes", "miércoles", "jueves",
        "viernes", "sábado", "domingo"
    ]

    meses = [
        "enero", "febrero", "marzo", "abril", "mayo",
        "junio", "julio", "agosto", "septiembre",
        "octubre", "noviembre", "diciembre"
    ]

    fecha_formateada = (
        f"{dias[ahora.weekday()]} {ahora.day} de "
        f"{meses[ahora.month - 1]} · {ahora:%H:%M}"
    )

    return {"fecha_actual": fecha_formateada}