import pymysql
from config import Config

def get_db_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        port=int(Config.DB_PORT),
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True # Analizar la implementación de esta linea para este TP. Podriamos tener que sacarla.
    )

def execute_query(
    query: str,
    params: tuple | dict = None,
    fetch_one: bool = False,
    fetch_all: bool = False
):
    """
    Ejecuta una consulta SQL parametrizada garantizando la seguridad
    (evita SQL Injection) y gestiona la apertura y cierre automático
    de conexiones y cursores.
    """
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())

            if fetch_one:
                return cursor.fetchone()

            if fetch_all:
                return cursor.fetchall()

            # Para INSERT devuelve el ID generado;
            # para UPDATE/DELETE, las filas afectadas.
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount

    finally:
        connection.close()