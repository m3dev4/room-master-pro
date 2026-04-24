from controller.auth.authService_controller import AuthService
from controller.reservation.reservationController import ReservationController
from interface.groupe import GroupeInterface
from interface.creneau import CreneauInterface
from interface.reporting import ReportingInterface
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box


console = Console()


class Reservations:
    def __init__(self, token=None):
        self.reservation  = ReservationController()
        self.token        = token
        self.grp_ui       = GroupeInterface()
        self.creneau_ui   = CreneauInterface()
        self.reporting_ui = ReportingInterface()

    # ------------------------------------------------------------------ #
    #  Affichages planning                                                 #
    # ------------------------------------------------------------------ #
    def afficher_vue_globale(self, date, data):
        table = Table(
            title=f"Planning du {date}",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True,
        )
        table.add_column("ID",    justify="center", style="bold yellow")
        table.add_column("Début", style="white")
        table.add_column("Fin",   style="white")
        table.add_column("Groupe",style="white")

        if not data:
            console.print("\n[bold red]Aucune donnée disponible.[/bold red]")
            return

        for row in data:
            creneau_id  = row[0]
            heure_debut = row[1]
            heure_fin   = row[2]
            groupe      = row[3] if row[3] else "[LIBRE]"
            table.add_row(str(creneau_id), str(heure_debut), str(heure_fin), str(groupe))

        console.print(table)

    def afficher_disponibilites(self, date, data):
        table = Table(
            title=f"Disponibilités pour la date : {date}",
            box=box.ROUNDED,
            border_style="magenta",
            show_lines=True,
        )
        table.add_column("ID",    justify="center", style="bold yellow")
        table.add_column("Début", style="white")
        table.add_column("Fin",   style="white")

        if not data:
            console.print("\n[bold red]Aucun créneau disponible pour cette date.[/bold red]")
            return

        for row in data:
            table.add_row(str(row[0]), str(row[1]), str(row[2]))

        console.print(table)

    # ------------------------------------------------------------------ #
    #  Menu principal admin                                                #
    # ------------------------------------------------------------------ #
    def afficher_menu(self):
        table = Table(
            title="🏛️  PANNEAU D'ADMINISTRATION",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True,
        )
        table.add_column("Option", justify="center", style="bold yellow")
        table.add_column("Description", style="white")

        table.add_row("1", "📅  Vue globale du planning (tous les créneaux)")
        table.add_row("2", "🟢  Vue disponibilités (créneaux libres uniquement)")
        table.add_row("3", "📌  Affecter une réservation")
        table.add_row("4", "👥  Gestion des groupes  (CRUD)")
        table.add_row("5", "🕐  Gestion des créneaux (CRUD)")
        table.add_row("6", "📊  Reporting & Export CSV")
        table.add_row("7", "🚪  Déconnexion")

        console.print(
            Panel(table, title="🎯 Centre Culturel – Admin", border_style="green")
        )

    def menu(self):
        while True:
            console.clear()
            self.afficher_menu()

            choix = console.input("\n[bold cyan]➤ Choisissez une option : [/bold cyan]")

            match choix:
                # ── Planning global ──────────────────────────────────────
                case "1":
                    date = console.input(
                        "\n[bold cyan]➤ Entrez la date (YYYY-MM-DD) : [/bold cyan]"
                    )
                    data = self.reservation.vue_global(date)
                    self.afficher_vue_globale(date, data)
                    console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")

                # ── Disponibilités ───────────────────────────────────────
                case "2":
                    console.print(
                        "\n[bold magenta]🟢 Affichage des Disponibilités...[/bold magenta]"
                    )
                    date = console.input(
                        "\n[bold cyan]➤ Entrez la date (YYYY-MM-DD) : [/bold cyan]"
                    )
                    data = self.reservation.disponibilite(date)
                    self.afficher_disponibilites(date, data)
                    console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")

                # ── Affecter réservation ─────────────────────────────────
                case "3":
                    date  = console.input("[bold cyan]Date (YYYY-MM-DD) : [/bold cyan]")
                    motif = console.input("[bold cyan]Motif             : [/bold cyan]")

                    disponibles = self.reservation.disponibilite(date)
                    self.afficher_disponibilites(date, disponibles)

                    if not disponibles:
                        console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")
                        continue

                    try:
                        crenaux_id = int(
                            console.input("[bold cyan]ID du créneau à réserver : [/bold cyan]")
                        )
                        groupe_id  = int(
                            console.input("[bold cyan]ID du groupe              : [/bold cyan]")
                        )
                    except ValueError:
                        console.print("[bold red]❌ ID invalide.[/bold red]")
                        console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")
                        continue

                    result = self.reservation.affecter_creneau(
                        date, motif, crenaux_id, groupe_id, self.token
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
                    console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")

                # ── CRUD Groupes ─────────────────────────────────────────
                case "4":
                    self.grp_ui.menu()

                # ── CRUD Créneaux ────────────────────────────────────────
                case "5":
                    self.creneau_ui.menu()

                # ── Reporting / CSV ──────────────────────────────────────
                case "6":
                    self.reporting_ui.menu()

                # ── Déconnexion ──────────────────────────────────────────
                case "7":
                    console.print("\n[bold red]Déconnexion... Au revoir 👋[/bold red]")
                    break

                case _:
                    console.print("\n[bold red]Option invalide ![/bold red]")
                    console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")
