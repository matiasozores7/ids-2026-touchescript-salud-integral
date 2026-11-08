import requests

from flask import current_app


def login_usuario(email: str, password: str) -> dict:
    url = f"{current_app.config['API_BASE_URL']}/auth/login"

    try:
        response = requests.post(
            url,
            json={
                "email": email,
                "password": password
            },
            timeout=10
        )

        resultado = response.json()

    except requests.Timeout:
        raise RuntimeError("El servidor de autenticación no respondió.")

    except requests.RequestException:
        raise RuntimeError("No se pudo conectar con el servidor.")

    except ValueError:
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    if not response.ok:
        raise RuntimeError(
            resultado.get("message", "No se pudo iniciar sesión.")
        )

    return resultado["data"]

def registrar_paciente(
    nombre: str,
    apellido: str,
    email: str,
    password: str,
    cobertura_id: int | None = None
) -> dict:
    url = f"{current_app.config['API_BASE_URL']}/auth/registro"

    try:
        response = requests.post(
            url,
            json={
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "password": password,
                "cobertura_id": cobertura_id
            },
            timeout=10
        )
        resultado = response.json()

    except requests.Timeout:
        raise RuntimeError("El servidor de registro no respondió.")
    except requests.RequestException:
        raise RuntimeError("No se pudo conectar con el servidor.")
    except ValueError:
        raise RuntimeError("El servidor devolvió una respuesta inválida.")

    if not response.ok:
        raise RuntimeError(
            resultado.get("message", "No se pudo registrar el paciente.")
        )

    data = resultado.get("data")

    if not isinstance(data, dict) or not data.get("access_token"):
        raise RuntimeError("La respuesta no contiene el token de acceso.")

    return data