import tkinter as tk
from .theme import appliquer_style


class VueAdministrateur:
    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)
        self.fenetre.title("Espace administrateur - Dream Park")
        self.fenetre.geometry("450x300")
        self.fenetre.resizable(False, False)

        self.titre = tk.Label(
            self.fenetre,
            text="ESPACE ADMINISTRATEUR",
            font=("Arial", 19, "bold")
        )
        self.titre.pack(pady=25)

        self.description = tk.Label(
            self.fenetre,
            text="Consulter et exporter les statistiques du parking",
            wraplength=390
        )
        self.description.pack(pady=12)

        self.bouton_statistiques = tk.Button(
            self.fenetre,
            text="Consulter les statistiques",
            width=32
        )
        self.bouton_statistiques.pack(pady=12)

        self.bouton_retour = tk.Button(
            self.fenetre,
            text="Retour à l'identification",
            width=32
        )
        self.bouton_retour.pack(pady=12)

        appliquer_style(self.fenetre)
