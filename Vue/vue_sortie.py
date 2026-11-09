import tkinter as tk
from .theme import appliquer_style

class VueSortie:

    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)

        self.fenetre.title("Reprendre mon véhicule")
        self.fenetre.geometry("600x600")
        
        self.numero_acces = tk.IntVar(value=1)
        self.label_acces = tk.Label(self.fenetre, text="Borne de sortie utilisée :")
        self.label_acces.pack(pady=5)
        self.menu_acces = tk.OptionMenu(self.fenetre, self.numero_acces, 1, 2)
        self.menu_acces.pack(pady=5)

        self.label_ticket = tk.Label(
            self.fenetre,
            text = "Veuillez saisir les 6 caractères de votre référence"
        )

        self.label_ticket.pack(pady=10)

        self.champ_ticket = tk.Entry(self.fenetre)
        
        self.champ_ticket.pack(pady = 10)

        self.bouton_valider = tk.Button(
            self.fenetre,
            text = "Valider",
            width = 25
        )

        self.bouton_valider.pack(pady = 10)

        self.bouton_annuler = tk.Button(
            self.fenetre,
            text = "Annuler",
            width = 25
        )

        self.bouton_annuler.pack(pady = 10)

        appliquer_style(self.fenetre)
