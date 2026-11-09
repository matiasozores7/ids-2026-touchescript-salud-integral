from getpass import getpass

from werkzeug.security import generate_password_hash

from src.database.connection import transaction
from src.repositories import usuario_repository as usuario_repo


def crear_admin():
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    email = input("Email: ").strip().lower()
    password = getpass("Contraseña: ")

    if not all([nombre, apellido, email, password]):
        raise ValueError("Todos los campos son obligatorios.")

    if len(password) < 8 or len(password) > 128:
        raise ValueError("La contraseña debe tener entre 8 y 128 caracteres.")

    password_hash = generate_password_hash(password)

    with transaction() as connection:
        usuario_existente = usuario_repo.buscar_usuario_por_email(
            connection,
            email
        )

        if usuario_existente:
            raise ValueError("Ya existe un usuario con ese email.")

        admin_id = usuario_repo.crear_usuario(
            connection=connection,
            nombre=nombre,
            apellido=apellido,
            email=email,
            password_hash=password_hash,
            rol="admin"
        )

    print(f"Administrador creado correctamente. ID: {admin_id}")


if __name__ == "__main__":
    crear_admin()