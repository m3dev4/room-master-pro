from database.connect import ConnectDB


class ReservatonModel:

    @staticmethod
    def get_vue_global(date):
        conn = ConnectDB()
        cursor = conn.get_cursor()

        sql = """
         SELECT c.id, c.date_heure, c.date_fin, 
         g.nom AS groupe
         FROM creneaux c
         LEFT JOIN reservations r ON c.id = r.creneaux_id 
         AND r.date_reservation = %s
         LEFT JOIN groupes g ON r.groupes_id = g.id
         ORDER BY c.date_heure
        """
        try:
            cursor.execute(sql, (date,))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Erreur; {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_disponible(date):
        conn = ConnectDB()
        cursor = conn.get_cursor()

        sql = """
        SELECT c.id, c.date_heure, c.date_fin
        FROM creneaux c
        WHERE c.id NOT IN (
            SELECT r.creneaux_id
            FROM reservations r
            WHERE r.date_reservation = %s
        )
        ORDER BY c.date_heure
        """
        try:
            cursor.execute(sql, (date,))
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Erreur; {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def creneau_reserve(date, crenau_id):
        conn = ConnectDB()
        cursor = conn.get_cursor()

        sql = """
        SELECT id FROM reservations
        WHERE date_reservation = %s AND creneaux_id = %s
        """

        try:
            cursor.execute(
                sql,
                (
                    date,
                    crenau_id,
                ),
            )
            result = cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"Erreur: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def reserver(date, motif, creneau_id, groupe_id, user_id):
        conn = ConnectDB()
        cursor = conn.get_cursor()

        sql = """INSERT INTO reservations (date_reservation, motif, creneaux_id, groupes_id, user_id) VALUES (%s, %s, %s, %s, %s)"""
        try:
            cursor.execute(sql, (date, motif, creneau_id, groupe_id, user_id))
            conn.commit()
        except Exception as e:
            print(f"Erreur: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
