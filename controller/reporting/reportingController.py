import csv
import os
from datetime import datetime
from models.reporting.reportingModel import ReportingModel


CSV_HEADERS = [
    "ID Réservation",
    "Date Réservation",
    "Motif",
    "Créé le",
    "Créneau Début",
    "Créneau Fin",
    "Groupe",
    "Email Groupe",
    "Téléphone Groupe",
    "Admin Nom",
    "Admin Prénom",
    "Admin Email",
]


class ReportingController:
    def __init__(self):
        self.model = ReportingModel()

    def get_stats(self):
        return self.model.get_stats()

    def exporter_csv_global(self, chemin_sortie=None):
   
        data = self.model.get_all_reservations()
        return self._ecrire_csv(data, chemin_sortie, suffixe="global")

    def exporter_csv_periode(self, date_debut, date_fin, chemin_sortie=None):

        data = self.model.get_reservations_by_date(date_debut, date_fin)
        return self._ecrire_csv(
            data, chemin_sortie, suffixe=f"{date_debut}_au_{date_fin}"
        )

    def _ecrire_csv(self, data, chemin_sortie, suffixe="export"):
      
        if not data:
            return {"success": False, "message": "Aucune donnée à exporter"}

        if not chemin_sortie:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"reservations_{suffixe}_{timestamp}.csv"
            chemin_sortie = os.path.join(os.getcwd(), nom_fichier)

        try:
            with open(chemin_sortie, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(CSV_HEADERS)
                for row in data:
                    writer.writerow([str(v) if v is not None else "" for v in row])
            return {
                "success": True,
                "message": f"Export réussi : {len(data)} réservation(s)",
                "chemin": chemin_sortie,
                "nb_lignes": len(data),
            }
        except Exception as e:
            return {"success": False, "message": f"Erreur d'écriture CSV : {e}"}
