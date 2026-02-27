import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

#config
HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
NAME = os.getenv("DB_NAME")


class ConnectDB:
    _instance = None

    def __new__(cls):
        try:
            if cls._instance is None:
                print("Creation du nouveau isntance...")
                cls._instance = super().__new__(cls)
                cls._instance.connection = mysql.connector.connect(
                    host=HOST, user=USER, password=PASSWORD, database=NAME
                )
                print("Database connected successfully")
            return cls._instance
        except Exception as e:
            print(e)

    def get_cursor(self):
        return self.connection.cursor()

