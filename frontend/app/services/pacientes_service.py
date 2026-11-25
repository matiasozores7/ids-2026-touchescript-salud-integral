
from app.clients.api_client import api_request
from app.errors.exceptions import ExternalServiceError


def listar_pacientes(limit: int = 10, offset: int = 0) -> dict:
    resultado = api_request(
        method="GET",
        endpoint="/pacientes",
        params={
            "_limit": limit,
            "_offset": offset,
        },
        authenticated=True,
    )

    data = resultado.get("data")
    if (
        not isinstance(data, dict)
        or not isinstance(data.get("items"), list)
    ):
        raise ExternalServiceError(
            "La respuesta del servicio de pacientes tiene un formato inválido."
        )

    return data


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
