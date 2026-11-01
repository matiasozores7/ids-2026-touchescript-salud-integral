from src.repositories.usuario_repository import (
    crear_usuario,
    actualizar_usuario_por_id,
    desactivar_usuario_por_id
)
from src.repositories.paciente_repository import (
    insertar_paciente,
    actualizar_paciente_por_id,
    obtener_usuario_id_por_paciente_id,
    buscar_paciente_por_id
)
from src.validators.paciente_validator import validar_datos_paciente, validar_datos_actualizacion_paciente

def crear_paciente_service(connection, data: dict) -> int:
    error_estructura = validar_datos_paciente(data)
    if error_estructura:
        raise ValueError(error_estructura)

    usuario_id = crear_usuario(connection, data)
    cobertura_id = data.get("cobertura_id")
    
    nuevo_id_paciente = insertar_paciente(connection, usuario_id, cobertura_id)

    return nuevo_id_paciente

def actualizar_paciente_service(connection, paciente_id: int, data: dict) -> None:
    error_estructura = validar_datos_actualizacion_paciente(data)
    if error_estructura:
        raise ValueError(error_estructura)

    usuario_id = obtener_usuario_id_por_paciente_id(connection, paciente_id)
    if not usuario_id:
        raise ValueError(f"El paciente con ID {paciente_id} no existe.")

    actualizar_usuario_por_id(connection, usuario_id, data)
    
    cobertura_id = data.get("cobertura_id")
    actualizar_paciente_por_id(connection, paciente_id, cobertura_id)

def eliminar_paciente_service(connection, paciente_id: int) -> None:
    paciente = buscar_paciente_por_id(connection, paciente_id)
    if not paciente:
        raise ValueError(f"El paciente con ID {paciente_id} no existe.")

    if not paciente.get("activo"):
        raise ValueError(f"El paciente con ID {paciente_id} ya se encuentra dado de baja.")

    desactivar_usuario_por_id(connection, paciente.get("usuario_id"))
