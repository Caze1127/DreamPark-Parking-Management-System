import tkinter as tk
from .theme import appliquer_style 

class VueDesabonnement:

    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)

        self.fenetre.title("Résiliation de mon abonnement")
        self.fenetre.geometry("500x450")

        self.choix_desabonnement = tk.StringVar(value="Choisir une option")

        self.label_confirmation = tk.Label(
            self.fenetre,
            text = "Que souhaitez-vous faire avec votre super-abonnement ?",
            wraplength=400,
            justify="center"
        )

        self.label_confirmation.pack()

        self.frame_boutons = tk.Frame(self.fenetre)
        self.frame_boutons.pack(pady=10)


        self.menu_desabonnement = tk.OptionMenu(
            self.fenetre,
            self.choix_desabonnement,
            "Devenir abonné classique",
            "Résilier complètement"
        )
        self.bouton_annuler = tk.Button(
            self.frame_boutons,
            text = "Annuler",
            width = 15
            )

        self.bouton_annuler.grid(row=0, column=0, padx=10)

        self.bouton_confirmer = tk.Button(
            self.frame_boutons,
            text = "Confirmer",
            width = 15,
            )

        self.bouton_confirmer.grid(row=0, column=1, padx=10)
        
        appliquer_style(self.fenetre)

    def afficher_choix_super_abonne(self):

        self.menu_desabonnement.pack(
            before = self.frame_boutons,
            pady = 10
        )
        