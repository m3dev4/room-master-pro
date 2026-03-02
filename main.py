from rich import print
from rich.panel import Panel
from rich.console import Console
import re
import traceback
from controller.auth.authService_controller import AuthService
from interface.reservation import Reservations

pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
regex_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

console = Console()


class Main:
    def __init__(self):
        self.auth_service = AuthService()
        self.reserve = Reservations()

    def menu(self):
        while True:
            console.print(
                Panel("Bienvenue dans le systeme de gestion de salle", expand=False)
            )
            console.print("1. S'inscrire")
            console.print("2. Se connecter")
            console.print("3. Quitter")

            choice = input("Choisissez une option: ")

            match choice:
                case "1":
                    while True:
                        nom = input("Entrez votre nom: ")
                        if not nom.isalpha() or nom == "":
                            print("Veuillez entrer un nom valide.")
                            continue
                        else:
                            nom = nom.capitalize().strip()
                            break

                    while True:
                        prenom = input("Entrez votre prenom: ")
                        if not prenom.isalpha() or prenom == "":
                            print("Veuillez entrer un prenom valide.")
                            continue
                        else:
                            prenom = prenom.capitalize().replace(" ", " ")
                            break

                    while True:
                        email = input("Veuillez saisir l'email: ").strip()
                        if re.match(pattern, email):
                            break
                        else:
                            print("Email invalide.")

                    while True:
                        password = input("Veuillez saisir le mot de passe: ")
                        if re.fullmatch(regex_pattern, password):
                            break
                        else:
                            print(
                                "Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial."
                            )
                            continue
                    try:
                        result = self.auth_service.register(
                            nom, prenom, email, password
                        )
                        if result and not result["success"]:
                            print(result["message"])
                    except Exception as e:
                        print(f"Erreur lors de la connexion : {e}")
                        traceback.print_exc()

                case "2":
                    while True:
                        email = input("Veuillez saisir l'email: ").strip()
                        if re.match(pattern, email):
                            break
                        else:
                            print("Email invalide.")

                    password = input("Entrer votr mot de passe: ")
                    try:
                        result = self.auth_service.login(email, password)
                        if result["success"] and result["role"] == "admin":
                            self.reserve = Reservations(token=result.get("token"))
                            self.reserve.menu()
                        elif result["success"] and result["role"] != "admin":
                            print("Bienvenue ! menu disponible uniquement pour l'admin")
                        else:
                            print(result["message"])
                    except Exception as e:
                        print(f"Erreur: {e}")
                        traceback.print_exc()
                case "3":
                    print("Au revoir!")
                    exit()
                case _:
                    print("Option invalide")


if __name__ == "__main__":
    mainMenu = Main()
    mainMenu.menu()
