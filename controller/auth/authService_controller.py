import bcrypt
from models.user.auth_model import UserModel


class AuthService:
    def __init__(self):
        self.user_repo = UserModel()

    def register(self, nom, prenom, email, password):
        if password < 8:
            return {
                "success": False,
                "message": "Le mot de passe doit contenir plus de 8 caracteres",
            }

        existing_user = self.user_repo.getEmail(email)
        if existing_user:
            return {"success": False, "message": "Cet email est deja utilise"}

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.user_repo.register(nom, prenom, email, hashed_password)

    def login(self, email, password):
        user = self.user_repo.getEmail(email)

        if not user:
            return {"success": False, "message": "Email introuvable"}

        stored_password = user[4]

        if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
            return {"success": True, "role": user[4]}

    