import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# config
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")


class ConnectDB:
    def __init__(self):
        self._connection = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, database=NAME, autocommit=True
        )

    def get_cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()
