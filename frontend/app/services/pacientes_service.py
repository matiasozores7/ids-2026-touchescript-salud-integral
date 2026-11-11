
from app.clients.api_client import api_request


def listar_pacientes() -> list[dict]:
    resultado = api_request(
        method="GET",
        endpoint="/pacientes",
        params={"limit": 100, "offset": 0},
        authenticated=True,
    )

    data = resultado.get("data") or {}
    return data.get("items", [])


def crear_paciente(
    nombre: str,
    apellido: str,
    email: str,
    password: str,
    cobertura_id: int,
    telefono: str | None = None,
) -> None:
    api_request(
        method="POST",
        endpoint="/pacientes",
        json={
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "password": password,
            "cobertura_id": cobertura_id,
            "telefono": telefono,
        },
        authenticated=True,
    )


def actualizar_paciente(
    paciente_id: int,
    nombre: str,
    apellido: str,
    email: str,
    cobertura_id: int,
    telefono: str | None = None,
) -> None:
    api_request(
        method="PATCH",
        endpoint=f"/pacientes/{paciente_id}",
        json={
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "cobertura_id": cobertura_id,
            "telefono": telefono,
        },
        authenticated=True,
    )

def eliminar_paciente(paciente_id: int) -> None:
    api_request(
        method="DELETE",
        endpoint=f"/pacientes/{paciente_id}",
        authenticated=True,
    )
