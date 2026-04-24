from database.connect import ConnectDB


class CreneauModel:

    @staticmethod
    def get_all():
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "SELECT id, date_heure, date_fin FROM creneaux ORDER BY date_heure"
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
    def get_by_id(creneau_id):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "SELECT id, date_heure, date_fin FROM creneaux WHERE id = %s"
        try:
            cursor.execute(sql, (creneau_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erreur: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create(date_heure, date_fin):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "INSERT INTO creneaux (date_heure, date_fin) VALUES (%s, %s)"
        try:
            cursor.execute(sql, (date_heure, date_fin))
            conn.commit()
            return {"success": True, "message": "Créneau créé avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def update(creneau_id, date_heure, date_fin):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "UPDATE creneaux SET date_heure=%s, date_fin=%s WHERE id=%s"
        try:
            cursor.execute(sql, (date_heure, date_fin, creneau_id))
            conn.commit()
            return {"success": True, "message": "Créneau mis à jour avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def delete(creneau_id):
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = "DELETE FROM creneaux WHERE id = %s"
        try:
            cursor.execute(sql, (creneau_id,))
            conn.commit()
            return {"success": True, "message": "Créneau supprimé avec succès"}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()
