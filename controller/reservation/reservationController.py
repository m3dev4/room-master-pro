from models.reservations.reseservationModel import ReservatonModel
from models.user.auth_model import UserModel


class ReservationController:
    def __init__(self):
        self.reservation = ReservatonModel()
        self.user_repo = UserModel()

    def vue_global(self, date):
        return self.reservation.get_vue_global(date)

    def disponibilite(self, date):
        return self.reservation.get_disponible(date)

    def affecter_creneau(self, date, motif, creneau_id, groupe_id, token):
        user_id = self.user_repo.get_user_id_by_token(token)
        if not user_id:
            return {"success": False, "message": "Session invalide ou expirée"}

        if self.reservation.creneau_reserve(date, creneau_id):
            return {"success": False, "message": "Ce créneau est déjà réservé."}

        ok = self.reservation.reserver(date, motif, creneau_id, groupe_id, user_id)
        if ok is False:
            return {"success": False, "message": "Erreur lors de la réservation"}
        return {
            "success": True,
            "message": "Réservation effectuée avec succès",
            "date": date,
            "motif": motif,
            "creneau_id": creneau_id,
            "groupe_id": groupe_id,
        }
