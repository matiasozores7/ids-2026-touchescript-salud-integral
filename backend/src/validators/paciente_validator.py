def validar_datos_usuario(data) -> str | None:
    mensaje_error = None

    if not data:
        mensaje_error = "El cuerpo de la petición (JSON) está vacío."
    elif not data.get("nombre") or not data.get("nombre").strip():
        mensaje_error = "El campo 'nombre' es obligatorio."
    elif not data.get("apellido") or not data.get("apellido").strip():
        mensaje_error = "El campo 'apellido' es obligatorio."
    elif not data.get("email") or not data.get("email").strip():
        mensaje_error = "El campo 'email' es obligatorio."
    elif not data.get("password") or not data.get("password").strip():
        mensaje_error = "El campo 'password' es obligatorio."

    return mensaje_error

def validar_datos_paciente(data) -> str | None:
    mensaje_error = validar_datos_usuario(data)

    if not mensaje_error and not data.get("cobertura_id"):
        mensaje_error = "El campo 'cobertura_id' es obligatorio."

    return mensaje_error