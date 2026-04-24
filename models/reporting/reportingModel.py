from database.connect import ConnectDB


class ReportingModel:

    @staticmethod
    def get_all_reservations():
        """Retourne toutes les réservations avec détails complets pour export."""
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = """
            SELECT
                r.id,
                r.date_reservation,
                r.motif,
                r.created_at,
                c.date_heure AS creneau_debut,
                c.date_fin   AS creneau_fin,
                g.nom        AS groupe,
                g.email      AS groupe_email,
                g.telephone  AS groupe_telephone,
                u.nom        AS admin_nom,
                u.prenom     AS admin_prenom,
                u.email      AS admin_email
            FROM reservations r
            JOIN creneaux  c ON c.id = r.creneaux_id
            JOIN groupes   g ON g.id = r.groupes_id
            JOIN users     u ON u.id = r.user_id
            ORDER BY r.date_reservation, c.date_heure
        """
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
    def get_reservations_by_date(date_debut, date_fin):
        """Réservations filtrées par période."""
        conn = ConnectDB()
        cursor = conn.get_cursor()
        sql = """
            SELECT
                r.id,
                r.date_reservation,
                r.motif,
                r.created_at,
                c.date_heure,
                c.date_fin,
                g.nom,
                g.email,
                g.telephone,
                u.nom,
                u.prenom,
                u.email
            FROM reservations r
            JOIN creneaux  c ON c.id = r.creneaux_id
            JOIN groupes   g ON g.id = r.groupes_id
            JOIN users     u ON u.id = r.user_id
            WHERE r.date_reservation BETWEEN %s AND %s
            ORDER BY r.date_reservation, c.date_heure
        """
        try:
            cursor.execute(sql, (date_debut, date_fin))
            return cursor.fetchall()
        except Exception as e:
            print(f"Erreur: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_stats():
        """Statistiques globales pour le rapport."""
        conn = ConnectDB()
        cursor = conn.get_cursor()
        stats = {}
        try:
            cursor.execute("SELECT COUNT(*) FROM reservations")
            stats["total_reservations"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM groupes")
            stats["total_groupes"] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM creneaux")
            stats["total_creneaux"] = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM reservations WHERE date_reservation = CURDATE()"
            )
            stats["reservations_aujourd_hui"] = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT g.nom, COUNT(r.id) AS nb
                FROM reservations r
                JOIN groupes g ON g.id = r.groupes_id
                GROUP BY g.nom
                ORDER BY nb DESC
                LIMIT 1
            """
            )
            row = cursor.fetchone()
            stats["groupe_plus_actif"] = row[0] if row else "N/A"

            return stats
        except Exception as e:
            print(f"Erreur stats: {e}")
            return stats
        finally:
            cursor.close()
            conn.close()
