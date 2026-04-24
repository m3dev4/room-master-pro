from controller.creneau.creneauController import CreneauController
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from datetime import datetime

console = Console()

DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


def _parse_dt(valeur):
    """Parse une chaîne en datetime, retourne None si invalide."""
    try:
        return datetime.strptime(valeur.strip(), DATETIME_FMT)
    except ValueError:
        return None


class CreneauInterface:
    def __init__(self):
        self.ctrl = CreneauController()

    # ------------------------------------------------------------------ #
    #  Affichage                                                           #
    # ------------------------------------------------------------------ #
    def _afficher_liste(self, creneaux):
        if not creneaux:
            console.print("\n[bold red]Aucun créneau trouvé.[/bold red]")
            return

        table = Table(
            title="🕐 Liste des Créneaux",
            box=box.ROUNDED,
            border_style="magenta",
            show_lines=True,
        )
        table.add_column("ID",     justify="center", style="bold yellow")
        table.add_column("Début",  style="white")
        table.add_column("Fin",    style="white")

        for c in creneaux:
            table.add_row(str(c[0]), str(c[1]), str(c[2]))

        console.print(table)

    def _afficher_menu(self):
        table = Table(
            title="🕐 GESTION DES CRÉNEAUX",
            box=box.ROUNDED,
            border_style="magenta",
            show_lines=True,
        )
        table.add_column("Option", justify="center", style="bold yellow")
        table.add_column("Action",  style="white")

        table.add_row("1", "Lister tous les créneaux")
        table.add_row("2", "Ajouter un créneau")
        table.add_row("3", "Modifier un créneau")
        table.add_row("4", "Supprimer un créneau")
        table.add_row("5", "Retour au menu principal")

        console.print(Panel(table, title="🎯 Centre Culturel – Admin", border_style="green"))

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #
    def _lister(self):
        creneaux = self.ctrl.lister()
        self._afficher_liste(creneaux)

    def _ajouter(self):
        console.print("\n[bold magenta]── Nouveau créneau ──[/bold magenta]")
        console.print("[dim]Format attendu : YYYY-MM-DD HH:MM:SS (ex: 2026-05-10 09:00:00)[/dim]\n")

        while True:
            debut_str = console.input("[bold cyan]Début : [/bold cyan]")
            debut = _parse_dt(debut_str)
            if debut:
                break
            console.print("[bold red]Format invalide. Utilisez : YYYY-MM-DD HH:MM:SS[/bold red]")

        while True:
            fin_str = console.input("[bold cyan]Fin   : [/bold cyan]")
            fin = _parse_dt(fin_str)
            if fin:
                break
            console.print("[bold red]Format invalide. Utilisez : YYYY-MM-DD HH:MM:SS[/bold red]")

        result = self.ctrl.creer(debut, fin)
        if result["success"]:
            console.print(f"\n[bold green]✅ {result['message']}[/bold green]")
        else:
            console.print(f"\n[bold red]❌ {result['message']}[/bold red]")

    def _modifier(self):
        self._lister()
        try:
            cid = int(console.input("\n[bold cyan]ID du créneau à modifier : [/bold cyan]"))
        except ValueError:
            console.print("[bold red]ID invalide.[/bold red]")
            return

        creneau = self.ctrl.obtenir(cid)
        if not creneau:
            console.print(f"[bold red]❌ Créneau ID {cid} introuvable.[/bold red]")
            return

        console.print(f"\n[dim]Valeurs actuelles → Début: {creneau[1]} | Fin: {creneau[2]}[/dim]")
        console.print("[dim](Laisser vide = conserver la valeur actuelle)[/dim]\n")

        debut_str = console.input("[bold cyan]Nouveau début (YYYY-MM-DD HH:MM:SS) : [/bold cyan]").strip()
        fin_str   = console.input("[bold cyan]Nouvelle fin  (YYYY-MM-DD HH:MM:SS) : [/bold cyan]").strip()

        debut = _parse_dt(debut_str) if debut_str else creneau[1]
        fin   = _parse_dt(fin_str)   if fin_str   else creneau[2]

        if debut_str and not _parse_dt(debut_str):
            console.print("[bold red]Format de début invalide.[/bold red]")
            return
        if fin_str and not _parse_dt(fin_str):
            console.print("[bold red]Format de fin invalide.[/bold red]")
            return

        result = self.ctrl.modifier(cid, debut, fin)
        if result["success"]:
            console.print(f"\n[bold green]✅ {result['message']}[/bold green]")
        else:
            console.print(f"\n[bold red]❌ {result['message']}[/bold red]")

    def _supprimer(self):
        self._lister()
        try:
            cid = int(console.input("\n[bold cyan]ID du créneau à supprimer : [/bold cyan]"))
        except ValueError:
            console.print("[bold red]ID invalide.[/bold red]")
            return

        confirm = console.input(
            f"[bold red]⚠️  Confirmer la suppression du créneau {cid} ? (oui/non) : [/bold red]"
        ).strip().lower()

        if confirm not in ("oui", "o"):
            console.print("[yellow]Suppression annulée.[/yellow]")
            return

        result = self.ctrl.supprimer(cid)
        if result["success"]:
            console.print(f"\n[bold green]✅ {result['message']}[/bold green]")
        else:
            console.print(f"\n[bold red]❌ {result['message']}[/bold red]")

    # ------------------------------------------------------------------ #
    #  Boucle principale                                                   #
    # ------------------------------------------------------------------ #
    def menu(self):
        while True:
            console.clear()
            self._afficher_menu()
            choix = console.input("\n[bold magenta]➤ Choisissez une option : [/bold magenta]")

            match choix:
                case "1":
                    self._lister()
                case "2":
                    self._ajouter()
                case "3":
                    self._modifier()
                case "4":
                    self._supprimer()
                case "5":
                    break
                case _:
                    console.print("\n[bold red]Option invalide ![/bold red]")

            console.input("\n[dim]Appuyez sur Entrée pour continuer...[/dim]")
