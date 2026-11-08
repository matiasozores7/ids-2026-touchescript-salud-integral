# Es un archivo que va a servir para ir migrando todo lo que se hizo del front
# a una estructura mas modularizada para implementar correctamente la integracion front/back
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(port=5001, debug=True)