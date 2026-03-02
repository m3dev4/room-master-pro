from controller.auth.authService_controller import AuthService
from controller.reservation.reservationController import ReservationController
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


console = Console()


class Reservations:
    def __init__(self, token=None):
        self.reservation = ReservationController()
        self.token = token

    def afficher_vue_globale(self, date, data):
        table = Table(
            title=f"Planning du {date}",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True,
        )
        table.add_column("ID", justify="center", style="bold yellow")
        table.add_column("Début", style="white")
        table.add_column("Fin", style="white")
        table.add_column("Groupe", style="white")

        if not data:
            console.print("\n[bold red]Aucune donnée disponible.[/bold red]")
            return

        for row in data:
            creneau_id = row[0]
            heure_debut = row[1]
            heure_fin = row[2]
            groupe = row[3] if row[3] else "[LIBRE]"
            table.add_row(
                str(creneau_id), str(heure_debut), str(heure_fin), str(groupe)
            )

        console.print(table)

    def afficher_disponibilites(self, date, data):
        table = Table(
            title=f"Disponibilités pour la date: {date}",
            box=box.ROUNDED,
            border_style="magenta",
            show_lines=True,
        )
        table.add_column("ID", justify="center", style="bold yellow")
        table.add_column("Début", style="white")
        table.add_column("Fin", style="white")

        if not data:
            console.print(
                "\n[bold red]Aucun créneau disponible pour cette date.[/bold red]"
            )
            return

        for row in data:
            creneau_id = row[0]
            heure_debut = row[1]
            heure_fin = row[2]
            table.add_row(str(creneau_id), str(heure_debut), str(heure_fin))

        console.print(table)

    def afficher_menu(self):
        table = Table(
            title="📅 CONSULTATION DU PLANNING",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True,
        )

        table.add_column("Option", justify="center", style="bold yellow")
        table.add_column("Description", style="white")

        table.add_row("1", "Vue Globale (Tous les créneaux de la journée)")
        table.add_row("2", "Vue Disponibilités (Créneaux libres uniquement)")
        table.add_row("3", "Affecter une reservation")
        table.add_row("4", "Quitter")

        console.print(
            Panel(table, title="🎯 Centre Culturel - Admin", border_style="green")
        )

    def menu(self):

        while True:
            console.clear()
            self.afficher_menu()

            choix = console.input("\n[bold cyan]➤ Choisissez une option : [/bold cyan]")

            match choix:
                case "1":
                    date = console.input(
                        "\n[bold cyan]➤ Entrez la date (YYYY-MM-DD) : [/bold cyan]"
                    )
                    data = self.reservation.vue_global(date)
                    self.afficher_vue_globale(date, data)

                case "2":
                    console.print(
                        "\n[bold magenta]🟢 Affichage des Disponibilités...[/bold magenta]"
                    )
                    date = console.input(
                        "\n[bold cyan]➤ Entrez la date (YYYY-MM-DD) : [/bold cyan]"
                    )
                    data = self.reservation.disponibilite(date)
                    self.afficher_disponibilites(date, data)

                case "3":
                    date = input("Date (YYYY-MM-DD) : ")
                    motif = input("Motif : ")

                    disponibles = self.reservation.disponibilite(date)
                    self.afficher_disponibilites(date, disponibles)

                    if not disponibles:
                        continue

                    crenaux_id = input("ID du créneau à réserver : ")
                    groupe_id = input("ID du groupe : ")

                    result = self.reservation.affecter_creneau(
                        date, motif, int(crenaux_id), int(groupe_id), self.token
                    )
                    if result and result.get("success"):
                        console.print(
                            "\n[bold green]✅ Réservation effectuée avec succès ![/bold green]"
                        )
                    else:
                        message = (
                            result.get("message")
                            if isinstance(result, dict)
                            else "Erreur lors de la réservation"
                        )
                        console.print(f"\n[bold red]❌ {message}[/bold red]")

                case "4":
                    console.print("\n[bold red]Au revoir 👋[/bold red]")
                    break

                case _:
                    console.print("\n[bold red]Option invalide ![/bold red]")
