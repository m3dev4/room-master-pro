from models.groupes.groupeModel import GroupeModel


class GroupeController:
    def __init__(self):
        self.model = GroupeModel()

    def lister(self):
        return self.model.get_all()

    def obtenir(self, groupe_id):
        return self.model.get_by_id(groupe_id)

    def creer(self, nom, email, telephone):
        if not nom or not nom.strip():
            return {"success": False, "message": "Le nom du groupe est obligatoire"}
        return self.model.create(nom.strip(), email.strip(), telephone.strip())

    def modifier(self, groupe_id, nom, email, telephone):
        if not self.model.get_by_id(groupe_id):
            return {"success": False, "message": f"Groupe ID {groupe_id} introuvable"}
        return self.model.update(groupe_id, nom.strip(), email.strip(), telephone.strip())

    def supprimer(self, groupe_id):
        if not self.model.get_by_id(groupe_id):
            return {"success": False, "message": f"Groupe ID {groupe_id} introuvable"}
        return self.model.delete(groupe_id)
