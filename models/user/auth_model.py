from database.connect import ConnectDB


class UserModel:

    @staticmethod
    def register(nom, prenom, email, password):
        conenction = ConnectDB()
        cursor = conenction.get_cursor()

        sql = """INSERT INTO users (nom, prenom, email, password) VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (nom, prenom, email, password))
        conenction.commit()

        cursor.close()
        conenction.close()

    @staticmethod
    def getEmail(self, email):
        conenction = ConnectDB()
        cursor = conenction.get_cursor()

        sql = "SELECT * FROM user WHERE email = %s"
        cursor.execute(sql, (email,))
        return self.cursor.fetchone()

    @staticmethod
    def createSession(self, token, created_at, expire_at):
        connection = ConnectDB()
        cursor = connection.get_cursor()
        
        sql = """INSERT INTO sessions (token, created_at, expire_at) VALUES (%s, %s, %s)"""
        cursor.execute(sql, (token, created_at, expire_at))
        connection.commit()
        
        cursor.close()
        connection.close()
        