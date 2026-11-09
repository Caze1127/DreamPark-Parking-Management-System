import tkinter as tk
from .theme import appliquer_style


class VueVoiturier:
    def __init__(self, fenetre_principale):
        self.fenetre = tk.Toplevel(fenetre_principale)
        self.fenetre.title("Espace voiturier - Dream Park")
        self.fenetre.geometry("690x480")

        self.titre = tk.Label(
            self.fenetre,
            text="LIVRAISONS À EFFECTUER",
            font=("Arial", 18, "bold")
        )
        self.titre.pack(pady=18)

        self.description = tk.Label(
            self.fenetre,
            text="Sélectionnez une livraison, puis confirmez son exécution."
        )
        self.description.pack(pady=5)

        self.cadre_liste = tk.Frame(self.fenetre)
        self.cadre_liste.pack(fill="both", expand=True, padx=20, pady=10)

        self.barre_defilement = tk.Scrollbar(self.cadre_liste)
        self.barre_defilement.pack(side="right", fill="y")

        self.liste_livraisons = tk.Listbox(
            self.cadre_liste,
            font=("Arial", 11),
            yscrollcommand=self.barre_defilement.set,
            exportselection=False
        )
        self.liste_livraisons.pack(side="left", fill="both", expand=True)
        self.barre_defilement.config(command=self.liste_livraisons.yview)

        self.bouton_actualiser = tk.Button(
            self.fenetre,
            text="Actualiser les livraisons",
            width=30
        )
        self.bouton_actualiser.pack(pady=5)

        self.bouton_livrer = tk.Button(
            self.fenetre,
            text="Confirmer la livraison sélectionnée",
            width=30
        )
        self.bouton_livrer.pack(pady=5)

        self.bouton_retour = tk.Button(
            self.fenetre,
            text="Retour à l'identification",
            width=30
        )
        self.bouton_retour.pack(pady=12)

        self.immatriculations = []

        appliquer_style(self.fenetre)

    def afficher_livraisons(self, livraisons):
        self.liste_livraisons.delete(0, tk.END)
        self.immatriculations = []

        for immatriculation, adresse, heure in livraisons:
            self.immatriculations.append(immatriculation)
            self.liste_livraisons.insert(
                tk.END,
                f"{immatriculation}  |  {adresse}  |  {heure}"
            )

    def immatriculation_selectionnee(self):
        selection = self.liste_livraisons.curselection()

        if not selection:
            return None

        return self.immatriculations[selection[0]]
