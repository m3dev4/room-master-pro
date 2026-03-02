from database.connect import ConnectDB
from datetime import datetime


class UserModel:

    @staticmethod
    def register(nom, prenom, email, password):
        connection = ConnectDB()
        cursor = connection.get_cursor()
        sql = """INSERT INTO users (nom, prenom, email, password) VALUES (%s, %s, %s, %s)"""
        try:
            cursor.execute(sql, (nom, prenom, email, password))
            connection.commit()
            return {"success": True, "message": "Inscription reussie"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def getEmail(email):
        connection = ConnectDB()
        cursor = connection.get_cursor()

        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        return cursor.fetchone()

    @staticmethod
    def upsert_session(user_id, token, created_at, expires_at):
        conn = ConnectDB()
        cur = conn.get_cursor()

        cur.execute(
            """
            INSERT INTO sessions (user_id, token, created_at, expires_at)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                token=VALUES(token),
                created_at=VALUES(created_at),
                expires_at=VALUES(expires_at)
        """,
            (user_id, token, created_at, expires_at),
        )

        conn.commit()
        cur.close()
        conn.close()

    def get_session(self, token):
        conn = ConnectDB()
        cursor = conn.get_cursor()

        sql = """ SELECT * FROM sessions WHERE token = %s """
        cursor.execute(sql, (token,))
        return cursor.fetchone()

    def get_user_id_by_token(self, token):
        conn = ConnectDB()
        cursor = conn.get_cursor()

        sql = """ SELECT user_id, expires_at FROM sessions WHERE token = %s """
        try:
            cursor.execute(sql, (token,))
            row = cursor.fetchone()
            if not row:
                return None

            user_id, expires_at = row

            if expires_at is not None and expires_at < datetime.now():
                return None

            return user_id
        finally:
            cursor.close()
            conn.close()
