import requests

from flask import current_app, session


def _headers() -> dict[str, str]:
    token = session.get("access_token")
    if not token:
        raise RuntimeError("La sesión expiró. Iniciá sesión nuevamente.")
    return {"Authorization": f"Bearer {token}"}


def _request(method: str, path: str, **kwargs) -> dict:
    url = f"{current_app.config['API_BASE_URL']}{path}"
    kwargs.setdefault("headers", _headers())
    kwargs.setdefault("timeout", 10)

    try:
        response = requests.request(method, url, **kwargs)
        resultado = response.json()
    except requests.Timeout:
        raise RuntimeError("El servidor de consultorios no respondió.")
    except requests.RequestException:
        raise RuntimeError("No se pudo conectar con el servidor.")
    except ValueError:
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    if response.status_code in (401, 403):
        raise RuntimeError("No tenés permisos para administrar consultorios.")
    if not response.ok:
        raise RuntimeError(
            resultado.get("message", "No se pudo completar la operación.")
        )

    return resultado


def listar_consultorios() -> list[dict]:
    resultado = _request("GET", "/consultorios", params={"limit": 100, "offset": 0})
    data = resultado.get("data") or {}
    return data.get("items", [])


def crear_consultorio(numero_sala: str, piso: str | None) -> None:
    _request(
        "POST",
        "/consultorios",
        json={"numero_sala": numero_sala, "piso": piso or None},
    )


def actualizar_consultorio(
    consultorio_id: int,
    numero_sala: str,
    piso: str | None,
) -> None:
    _request(
        "PUT",
        f"/consultorios/{consultorio_id}",
        json={"numero_sala": numero_sala, "piso": piso or None},
    )


def eliminar_consultorio(consultorio_id: int) -> None:
    _request("DELETE", f"/consultorios/{consultorio_id}")
