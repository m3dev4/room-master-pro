import os
from controller.reporting.reportingController import ReportingController
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


class ReportingInterface:
    def __init__(self):
        self.ctrl = ReportingController()

    # ------------------------------------------------------------------ #
    #  Affichage menu                                                      #
    # ------------------------------------------------------------------ #
    def _afficher_menu(self):
        table = Table(
            title="📊 REPORTING & EXPORT CSV",
            box=box.ROUNDED,
            border_style="yellow",
            show_lines=True,
        )
        table.add_column("Option", justify="center", style="bold yellow")
        table.add_column("Action",  style="white")

        table.add_row("1", "Afficher les statistiques globales")
        table.add_row("2", "Exporter toutes les réservations (CSV)")
        table.add_row("3", "Exporter par période (CSV)")
        table.add_row("4", "Retour au menu principal")

        console.print(Panel(table, title="🎯 Centre Culturel – Admin", border_style="green"))

    # ------------------------------------------------------------------ #
    #  Statistiques                                                        #
    # ------------------------------------------------------------------ #
    def _afficher_stats(self):
        stats = self.ctrl.get_stats()
        if not stats:
            console.print("[bold red]Impossible de récupérer les statistiques.[/bold red]")
            return

        table = Table(
            title="📈 Statistiques Générales",
            box=box.ROUNDED,
            border_style="yellow",
            show_lines=True,
        )
        table.add_column("Indicateur",  style="bold cyan")
        table.add_column("Valeur",      style="bold white", justify="right")

        table.add_row("Total réservations",       str(stats.get("total_reservations", 0)))
        table.add_row("Total groupes",             str(stats.get("total_groupes", 0)))
        table.add_row("Total créneaux",            str(stats.get("total_creneaux", 0)))
        table.add_row("Réservations aujourd'hui", str(stats.get("reservations_aujourd_hui", 0)))
        table.add_row("Groupe le plus actif",      str(stats.get("groupe_plus_actif", "N/A")))

        console.print(table)

    # ------------------------------------------------------------------ #
    #  Export CSV global                                                   #
    # ------------------------------------------------------------------ #
    def _export_global(self):
        chemin = console.input(
            "\n[bold cyan]Dossier de destination (Entrée = répertoire courant) : [/bold cyan]"
        ).strip()

        chemin_complet = None
        if chemin:
            if not os.path.isdir(chemin):
                console.print(f"[bold red]❌ Dossier introuvable : {chemin}[/bold red]")
                return
            from datetime import datetime
            nom = f"reservations_global_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            chemin_complet = os.path.join(chemin, nom)

        result = self.ctrl.exporter_csv_global(chemin_complet)
        self._afficher_resultat_export(result)

    # ------------------------------------------------------------------ #
    #  Export CSV par période                                              #
    # ------------------------------------------------------------------ #
    def _export_periode(self):
        console.print("\n[dim]Format date : YYYY-MM-DD[/dim]")
        date_debut = console.input("[bold cyan]Date début : [/bold cyan]").strip()
        date_fin   = console.input("[bold cyan]Date fin   : [/bold cyan]").strip()

        if not date_debut or not date_fin:
            console.print("[bold red]❌ Les deux dates sont obligatoires.[/bold red]")
            return

        if date_debut > date_fin:
            console.print("[bold red]❌ La date de début doit être ≤ à la date de fin.[/bold red]")
            return

        chemin = console.input(
            "[bold cyan]Dossier de destination (Entrée = répertoire courant) : [/bold cyan]"
        ).strip()

        chemin_complet = None
        if chemin:
            if not os.path.isdir(chemin):
                console.print(f"[bold red]❌ Dossier introuvable : {chemin}[/bold red]")
                return
            from datetime import datetime
            nom = f"reservations_{date_debut}_au_{date_fin}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            chemin_complet = os.path.join(chemin, nom)

        result = self.ctrl.exporter_csv_periode(date_debut, date_fin, chemin_complet)
        self._afficher_resultat_export(result)

    # ------------------------------------------------------------------ #
    #  Résultat export                                                     #
    # ------------------------------------------------------------------ #
    def _afficher_resultat_export(self, result):
        if result["success"]:
            console.print(f"\n[bold green]✅ {result['message']}[/bold green]")
            console.print(f"[bold white]📁 Fichier : [underline]{result['chemin']}[/underline][/bold white]")
            console.print(f"[dim]Lignes exportées : {result['nb_lignes']}[/dim]")
        else:
            console.print(f"\n[bold red]❌ {result['message']}[/bold red]")

    # ------------------------------------------------------------------ #
    #  Boucle principale                                                   #
    # ------------------------------------------------------------------ #
    def menu(self):
        while True:
            console.clear()
            self._afficher_menu()
            choix = console.input("\n[bold yellow]➤ Choisissez une option : [/bold yellow]")

            match choix:
                case "1":
                    self._afficher_stats()
                case "2":
                    self._export_global()
                case "3":
                    self._export_periode()
                case "4":
                    break
                case _:
                    console.print("\n[bold red]Option invalide ![/bold red]")

            console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")
