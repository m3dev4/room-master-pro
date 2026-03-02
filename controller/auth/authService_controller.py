import bcrypt
from models.user.auth_model import UserModel
from datetime import datetime, timedelta
import uuid


class AuthService:
    def __init__(self):
        self.user_repo = UserModel()

    # Method de creation d'un compte
    def register(self, nom, prenom, email, password):
        if len(password) < 8:
            return {
                "success": False,
                "message": "Le mot de passe doit contenir plus de 8 caracteres",
            }

        existing_user = self.user_repo.getEmail(email)
        if existing_user:
            return {"success": False, "message": "Cet email est deja utilise"}

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        result = self.user_repo.register(nom, prenom, email, hashed_password)
        if result:
            return {"success": True, "message": "Inscription reussie"}

        return {"success": False, "message": "Erreur lors de l'inscription"}

    def login(self, email, password):
        user = self.user_repo.getEmail(email)

        if not user:
            return {"success": False, "message": "Email introuvable"}

        user_id = user[0]
        stored_hash = user[4]
        role = user[5]

        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return {"success": False, "message": "Mot de passe incorrect"}

        token = uuid.uuid4().hex
        now = datetime.now()
        expire_at = now + timedelta(hours=8)

        self.user_repo.upsert_session(user_id, token, now, expire_at)

        return {
            "success": True,
            "message": "Connexion reussie",
            "token": token,
            "role": role,
        }

    def getSession(self, token):
        session = self.user_repo.get_session(token)

        if not session:
            return {
                "success": False,
                "message": "Session invalide ou expirée",
                "data": None,
            }

        return {"success": True, "message": "Session valide", "data": session}
