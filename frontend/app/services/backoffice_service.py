import requests

from flask import current_app


def _headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


def _obtener_error(response) -> str:
    try:
        resultado = response.json()
    except ValueError:
        return "El servidor devolvió una respuesta inválida."

    if not isinstance(resultado, dict):
        return "No se pudo completar la operación."

    errores = resultado.get("errors", [])
    if errores and isinstance(errores[0], dict):
        return errores[0].get(
            "description",
            errores[0].get("message", "No se pudo completar la operación.")
        )

    return resultado.get("message", "No se pudo completar la operación.")


def _solicitar(metodo: str, ruta: str, access_token: str, **kwargs) -> dict:
    if not access_token:
        raise RuntimeError("La sesión de administración no está autenticada.")

    url = f"{current_app.config['API_BASE_URL']}{ruta}"

    try:
        response = requests.request(
            metodo,
            url,
            headers=_headers(access_token),
            timeout=10,
            **kwargs
        )
    except requests.Timeout:
        raise RuntimeError("El servidor de especialidades no respondió.")
    except requests.RequestException:
        raise RuntimeError("No se pudo conectar con el servidor.")

    if not response.ok:
        raise RuntimeError(_obtener_error(response))

    try:
        resultado = response.json()
    except ValueError:
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    if not isinstance(resultado, dict):
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    return resultado


def listar_especialidades(access_token: str) -> dict:
    resultado = _solicitar(
        "GET",
        "/especialidades?_limit=100&_offset=0",
        access_token
    )
    data = resultado.get("data")

    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise RuntimeError("El servidor devolvió una lista de especialidades inválida.")

    return data


def crear_especialidad(
    access_token: str,
    nombre: str,
    descripcion: str | None
) -> None:
    _solicitar(
        "POST",
        "/especialidades",
        access_token,
        json={"nombre": nombre, "descripcion": descripcion}
    )


def actualizar_especialidad(
    access_token: str,
    especialidad_id: int,
    nombre: str,
    descripcion: str | None
) -> None:
    _solicitar(
        "PUT",
        f"/especialidades/{especialidad_id}",
        access_token,
        json={"nombre": nombre, "descripcion": descripcion}
    )


def eliminar_especialidad(access_token: str, especialidad_id: int) -> None:
    _solicitar(
        "DELETE",
        f"/especialidades/{especialidad_id}",
        access_token
    )