from src.database.connection import transaction
from src.repositories.reportes_repository import (
    contar_turnos,
    obtener_ausentismo_general,
    obtener_espera_promedio,
    obtener_ausentismo_por_especialidad,
    obtener_resultados_turnos,
    obtener_ocupacion_consultorios,
    obtener_espera_diaria,
    obtener_espera_por_profesional
)


PERIODOS_VALIDOS = (7, 14, 28)


def validar_periodo(periodo) -> int:
    try:
        periodo = int(periodo)
    except (TypeError, ValueError):
        raise ValueError("El período debe ser 7, 14 o 28 días")

    if periodo not in PERIODOS_VALIDOS:
        raise ValueError("El período debe ser 7, 14 o 28 días")

    return periodo


def obtener_reportes(periodo) -> dict:
    periodo = validar_periodo(periodo)

    with transaction() as connection:
        total_turnos = contar_turnos(connection, periodo)
        ausentismo_general = obtener_ausentismo_general(connection, periodo)
        espera_promedio = obtener_espera_promedio(connection, periodo)

        especialidades = obtener_ausentismo_por_especialidad(
            connection,
            periodo
        )
        resultados = obtener_resultados_turnos(connection, periodo)
        ocupacion = obtener_ocupacion_consultorios(connection, periodo)
        esperas = obtener_espera_diaria(connection, periodo)
        profesionales = obtener_espera_por_profesional(
            connection,
            periodo
        )

    return {
        "report_data": {
            "specialties": {
                "labels": [
                    fila["label"] for fila in especialidades
                ],
                "values": [
                    float(fila["value"] or 0)
                    for fila in especialidades
                ]
            },
            "appointmentResults": resultados,
            "occupancy": {
                "labels": [
                    fila["label"] for fila in ocupacion
                ],
                "values": [
                    float(fila["value"] or 0)
                    for fila in ocupacion
                ]
            },
            "waiting": {
                "labels": [
                    fila["label"] for fila in esperas
                ],
                "values": [
                    float(fila["value"] or 0)
                    for fila in esperas
                ]
            },
            "professionals": {
                "labels": [
                    fila["label"] for fila in profesionales
                ],
                "values": [
                    float(fila["value"] or 0)
                    for fila in profesionales
                ]
            }
        },
        "total_turnos": total_turnos,
        "ausentismo_general": ausentismo_general,
        "espera_promedio": espera_promedio
    }