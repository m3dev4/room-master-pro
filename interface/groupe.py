from controller.groupe.groupeController import GroupeController
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


class GroupeInterface:
    def __init__(self):
        self.ctrl = GroupeController()

    # ------------------------------------------------------------------ #
    #  Affichage                                                           #
    # ------------------------------------------------------------------ #
    def _afficher_liste(self, groupes):
        if not groupes:
            console.print("\n[bold red]Aucun groupe trouvé.[/bold red]")
            return

        table = Table(
            title="📋 Liste des Groupes",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True,
        )
        table.add_column("ID",        justify="center", style="bold yellow")
        table.add_column("Nom",       style="white")
        table.add_column("Email",     style="white")
        table.add_column("Téléphone", style="white")

        for g in groupes:
            table.add_row(str(g[0]), g[1] or "", g[2] or "", g[3] or "")

        console.print(table)

    def _afficher_menu(self):
        table = Table(
            title="👥 GESTION DES GROUPES",
            box=box.ROUNDED,
            border_style="cyan",
            show_lines=True,
        )
        table.add_column("Option", justify="center", style="bold yellow")
        table.add_column("Action",  style="white")

        table.add_row("1", "Lister tous les groupes")
        table.add_row("2", "Ajouter un groupe")
        table.add_row("3", "Modifier un groupe")
        table.add_row("4", "Supprimer un groupe")
        table.add_row("5", "Retour au menu principal")

        console.print(Panel(table, title="🎯 Centre Culturel – Admin", border_style="green"))

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #
    def _lister(self):
        groupes = self.ctrl.lister()
        self._afficher_liste(groupes)

    def _ajouter(self):
        console.print("\n[bold cyan]── Nouveau groupe ──[/bold cyan]")
        nom       = console.input("[bold cyan]Nom       : [/bold cyan]").strip()
        email     = console.input("[bold cyan]Email     : [/bold cyan]").strip()
        telephone = console.input("[bold cyan]Téléphone : [/bold cyan]").strip()

        result = self.ctrl.creer(nom, email, telephone)
        if result["success"]:
            console.print(f"\n[bold green]✅ {result['message']}[/bold green]")
        else:
            console.print(f"\n[bold red]❌ {result['message']}[/bold red]")

    def _modifier(self):
        self._lister()
        try:
            gid = int(console.input("\n[bold cyan]ID du groupe à modifier : [/bold cyan]"))
        except ValueError:
            console.print("[bold red]ID invalide.[/bold red]")
            return

        groupe = self.ctrl.obtenir(gid)
        if not groupe:
            console.print(f"[bold red]❌ Groupe ID {gid} introuvable.[/bold red]")
            return

        console.print(f"\n[dim]Valeurs actuelles → Nom: {groupe[1]} | Email: {groupe[2]} | Tél: {groupe[3]}[/dim]")
        console.print("[dim](Laisser vide = conserver la valeur actuelle)[/dim]\n")

        nom       = console.input("[bold cyan]Nouveau nom       : [/bold cyan]").strip() or groupe[1]
        email     = console.input("[bold cyan]Nouvel email      : [/bold cyan]").strip() or groupe[2]
        telephone = console.input("[bold cyan]Nouveau téléphone : [/bold cyan]").strip() or groupe[3]

        result = self.ctrl.modifier(gid, nom, email, telephone)
        if result["success"]:
            console.print(f"\n[bold green]✅ {result['message']}[/bold green]")
        else:
            console.print(f"\n[bold red]❌ {result['message']}[/bold red]")

    def _supprimer(self):
        self._lister()
        try:
            gid = int(console.input("\n[bold cyan]ID du groupe à supprimer : [/bold cyan]"))
        except ValueError:
            console.print("[bold red]ID invalide.[/bold red]")
            return

        confirm = console.input(
            f"[bold red]⚠️  Confirmer la suppression du groupe {gid} ? (oui/non) : [/bold red]"
        ).strip().lower()

        if confirm not in ("oui", "o"):
            console.print("[yellow]Suppression annulée.[/yellow]")
            return

        result = self.ctrl.supprimer(gid)
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
            choix = console.input("\n[bold cyan]➤ Choisissez une option : [/bold cyan]")

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
