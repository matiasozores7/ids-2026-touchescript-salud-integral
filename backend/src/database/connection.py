import os
import pymysql
from contextlib import contextmanager
from config import Config

def get_db_connection():
    parametros = {
        "user": Config.DB_USER,
        "password": Config.DB_PASSWORD,
        "database": Config.DB_NAME,
        "cursorclass": pymysql.cursors.DictCursor
    }

    if Config.DB_HOST.startswith("/"):
        parametros["unix_socket"] = Config.DB_HOST
    elif Config.DB_HOST in ("localhost", "127.0.0.1") and os.path.exists("/var/run/mysqld/mysqld.sock"):
        parametros["unix_socket"] = "/var/run/mysqld/mysqld.sock"
    else:
        parametros["host"] = Config.DB_HOST
        parametros["port"] = int(Config.DB_PORT)

    return pymysql.connect(**parametros)


@contextmanager
def transaction():
    connection = get_db_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()