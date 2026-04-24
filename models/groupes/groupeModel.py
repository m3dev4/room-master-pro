from database.connect import ConnectDB


class GroupeModel:

    @staticmethod
    def get_all():
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "SELECT id, nom, email, telephone FROM groupes ORDER BY nom"
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_by_id(groupe_id):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "SELECT id, nom, email, telephone FROM groupes WHERE id = %s"
        try:
            cursor.execute(sql, (groupe_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erreur: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(nom, email, telephone):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "INSERT INTO groupes (nom, email, telephone) VALUES (%s, %s, %s)"
        try:
            cursor.execute(sql, (nom, email, telephone))
            conn.commit()
            return {"success": True, "message": "Groupe créé avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(groupe_id, nom, email, telephone):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "UPDATE groupes SET nom=%s, email=%s, telephone=%s WHERE id=%s"
        try:
            cursor.execute(sql, (nom, email, telephone, groupe_id))
            conn.commit()
            return {"success": True, "message": "Groupe mis à jour avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(groupe_id):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "DELETE FROM groupes WHERE id = %s"
        try:
            cursor.execute(sql, (groupe_id,))
            conn.commit()
            return {"success": True, "message": "Groupe supprimé avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()
