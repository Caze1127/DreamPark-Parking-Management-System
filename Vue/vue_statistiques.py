import tkinter as tk
from .theme import appliquer_style


class VueStatistiques:

    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)

        self.fenetre.title("Statistiques DreamPark")
        self.fenetre.geometry("720x620")
        self.fenetre.minsize(600, 480)

        self.titre = tk.Label(
            self.fenetre,
            text="STATISTIQUES DREAM PARK",
            font=("Arial", 20, "bold")
        )

        self.titre.pack(pady=15)

        self.frame_contenu = tk.Frame(self.fenetre)
        self.frame_contenu.pack(fill="both", expand=True, padx=20, pady=10)

        self.barre_defilement = tk.Scrollbar(self.frame_contenu)
        self.barre_defilement.pack(side="right", fill="y")

        self.zone_statistiques = tk.Text(
            self.frame_contenu,
            font=("Arial", 11),
            wrap="word",
            yscrollcommand=self.barre_defilement.set,
            state="disabled"
        )

        self.zone_statistiques.pack(side="left", fill="both", expand=True)
        self.barre_defilement.config(command=self.zone_statistiques.yview)

        self.frame_boutons = tk.Frame(self.fenetre)
        self.frame_boutons.pack(pady=15)

        self.bouton_actualiser = tk.Button(
            self.frame_boutons,
            text="Actualiser",
            width=17
        )

        self.bouton_actualiser.grid(row=0, column=0, padx=5, pady=5)

        self.bouton_exporter_texte = tk.Button(
            self.frame_boutons,
            text="Exporter TXT",
            width=17
        )

        self.bouton_exporter_texte.grid(row=0, column=1, padx=5, pady=5)

        self.bouton_exporter_html = tk.Button(
            self.frame_boutons,
            text="Exporter HTML",
            width=17
        )

        self.bouton_exporter_html.grid(row=0, column=2, padx=5, pady=5)

        self.bouton_fermer = tk.Button(
            self.fenetre,
            text="Fermer",
            width=25
        )

        self.bouton_fermer.pack(pady=10)

        appliquer_style(self.fenetre)

    def afficher_statistiques(self, resume):

        self.zone_statistiques.config(state="normal")
        self.zone_statistiques.delete("1.0", "end")

        for cle, valeur in resume.items():

            self.zone_statistiques.insert("end", f"{cle} : {valeur}\n\n")

        self.zone_statistiques.config(state="disabled")
