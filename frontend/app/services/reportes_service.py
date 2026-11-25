import os

import requests
from flask import session

from app.errors.exceptions import AppError


def obtener_reportes(periodo: int) -> dict:
    token = (
        session.get("access_token")
        or session.get("token")
        or session.get("jwt")
    )

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        respuesta = requests.get(
            f"{os.getenv('API_BASE_URL')}/reportes",
            params={"period": periodo},
            headers=headers,
            timeout=10,
        )

        if respuesta.status_code >= 400:
            try:
                detalle = respuesta.json()
            except ValueError:
                detalle = respuesta.text

            raise AppError(
                f"Backend reportes: HTTP {respuesta.status_code} - {detalle}"
            )

        payload = respuesta.json()

        if "data" in payload:
            return payload["data"]

        return payload

    except requests.RequestException as error:
        raise AppError(
            f"El frontend no pudo conectar con el backend: {error}"
        )