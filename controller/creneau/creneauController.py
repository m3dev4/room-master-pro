from models.creneaux.creneauModel import CreneauModel


class CreneauController:
    def __init__(self):
        self.model = CreneauModel()

    def lister(self):
        return self.model.get_all()

    def obtenir(self, creneau_id):
        return self.model.get_by_id(creneau_id)

    def creer(self, date_heure, date_fin):
        if not date_heure or not date_fin:
            return {"success": False, "message": "Les dates de début et fin sont obligatoires"}
        if date_heure >= date_fin:
            return {"success": False, "message": "La date de début doit être antérieure à la date de fin"}
        return self.model.create(date_heure, date_fin)

    def modifier(self, creneau_id, date_heure, date_fin):
        if not self.model.get_by_id(creneau_id):
            return {"success": False, "message": f"Créneau ID {creneau_id} introuvable"}
        if date_heure >= date_fin:
            return {"success": False, "message": "La date de début doit être antérieure à la date de fin"}
        return self.model.update(creneau_id, date_heure, date_fin)

    def supprimer(self, creneau_id):
        if not self.model.get_by_id(creneau_id):
            return {"success": False, "message": f"Créneau ID {creneau_id} introuvable"}
        return self.model.delete(creneau_id)
