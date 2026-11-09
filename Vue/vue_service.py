import tkinter as tk
from .theme import appliquer_style

class VueService:

    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)

        self.fenetre.title("Gestion des services")
        self.fenetre.geometry("500x450")

        self.choix_service = tk.StringVar(
            value = "Choisir un service"
        )

        self.label_immatriculation = tk.Label(
            self.fenetre,
            text = "Immatriculation",
            width = 25
        )

        self.label_immatriculation.pack(pady = 5)

        self.champ_immatriculation = tk.Entry(
            self.fenetre
        )

        self.champ_immatriculation.pack(pady = 5)

        self.menu_service = tk.OptionMenu(
            self.fenetre,
            self.choix_service,
            "entretien", "maintenance", "livraison", "aucun"
        )

        self.menu_service.pack(pady = 5)

        self.label_heure = tk.Label(
            self.fenetre,
            text = "Heure de livraison souhaité",
            width = 25 
        )

        self.champ_heure = tk.Entry(
            self.fenetre
        )

        self.bouton_valider = tk.Button(
            self.fenetre,
            text = "Valider",
            width = 25
        )

        self.bouton_valider.pack(pady = 5)

        self.bouton_lancer_service = tk.Button(
            self.fenetre,
            text="Lancer le service",
            width=25
        )

        self.bouton_lancer_service.pack(pady = 5)


        self.bouton_terminer_service = tk.Button(
            self.fenetre,
            text = "Terminer le service",
            width = 25
        )

        self.bouton_terminer_service.pack(pady = 5)

        self.bouton_annuler = tk.Button(
            self.fenetre,
            text = "Annuler",
            width = 25
        )

        self.bouton_annuler.pack(pady = 5)

        appliquer_style(self.fenetre)

    def afficher_heure(self):
        
        self.label_heure.pack(
            before = self.bouton_valider, 
            pady = 5
        )
        self.champ_heure.pack(
            before = self.bouton_valider, 
            pady = 5
        )

    def masquer_heure(self):
        
        self.label_heure.pack_forget()
        self.champ_heure.pack_forget()