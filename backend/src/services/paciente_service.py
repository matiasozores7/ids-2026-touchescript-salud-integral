from src.repositories.usuario_repository import crear_usuario
from src.repositories.paciente_repository import insertar_paciente
from src.validators.paciente_validator import validar_datos_paciente

def crear_paciente_service(connection, data: dict) -> int:
    error_estructura = validar_datos_paciente(data)
    if error_estructura:
        raise ValueError(error_estructura)

    usuario_id = crear_usuario(connection, data)
    cobertura_id = data.get("cobertura_id")
    
    nuevo_id_paciente = insertar_paciente(connection, usuario_id, cobertura_id)

    return nuevo_id_paciente