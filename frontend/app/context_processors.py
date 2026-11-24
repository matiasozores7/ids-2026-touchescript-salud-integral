from datetime import datetime
from app.utils.date_format import fecha_larga


def inject_now():
    ahora = datetime.now()
    fecha_formateada = (
        f"{fecha_larga(ahora)} · {ahora:%H:%M}"
    )

    return {"fecha_actual": fecha_formateada}