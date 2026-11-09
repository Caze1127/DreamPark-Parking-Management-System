import tkinter as tk
from .theme import appliquer_style

class VueEntree:

    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)

        self.fenetre.title("Entrée des véhicules")
        self.fenetre.geometry("600x700")

        self.numero_acces = tk.IntVar(value=1)
        self.label_acces = tk.Label(self.fenetre, text="Borne d’entrée utilisée :")
        self.label_acces.pack(pady=3)
        self.menu_acces = tk.OptionMenu(self.fenetre, self.numero_acces, 1, 2)
        self.menu_acces.pack(pady=3)

        self.mode_paiement = tk.StringVar(value = "Choisir un paiement")
        self.choix_abonnement = tk.StringVar(value = "Choisir un abonnement")
        
        self.label_titre = tk.Label(
            self.fenetre,
            text = "ENTRÉE VÉHICULE",
            font = ("Arial", 24, "bold")
        )

        self.label_titre.pack(pady = 2)

        self.label_nom = tk.Label(
            self.fenetre,
            text = "*Nom :",
            width = 25
        )

        self.label_nom.pack(pady = 2)

        self.champ_nom = tk.Entry(
            self.fenetre
            )
        
        self.champ_nom.pack()

        self.label_adresse = tk.Label(
            self.fenetre,
            text = "*Adresse :",
            width = 25
        )

        self.label_adresse.pack(pady = 2)

        self.champ_adresse = tk.Entry(
            self.fenetre
        )
        
        self.champ_adresse.pack(pady = 2)

        self.label_immatriculation = tk.Label(
            self.fenetre,
            text = "*Immatriculation :",
            width = 25
        )

        self.label_immatriculation.pack(pady = 2)

        self.champ_immatriculation = tk.Entry(
            self.fenetre
        )

        self.champ_immatriculation.pack()

        self.label_hauteur = tk.Label(
            self.fenetre,
            text = "*Hauteur :",
            width = 25
        )

        self.label_hauteur.pack(pady = 2)

        self.champ_hauteur = tk.Entry(
            self.fenetre
        )

        self.champ_hauteur.pack()

        self.label_longueur = tk.Label(
                    self.fenetre,
                    text = "*Longueur :",
                    width = 25
                )

        self.label_longueur.pack(pady = 2)

        self.champ_longueur = tk.Entry(
            self.fenetre
        )

        self.champ_longueur.pack()

        self.label_choix_abonnement = tk.Label(
            self.fenetre,
            text = "*Choix d'abonnement :",
            width = 25
        )
        self.label_choix_abonnement.pack(pady = 2)

        self.menu_abonnement = tk.OptionMenu(
            self.fenetre,
            self.choix_abonnement,
            "Aucun", "Abonné classique", "Super-abonné",
        )
        
        self.menu_abonnement.pack(pady = 4)

        self.label_mode_paiement = tk.Label(
            self.fenetre,
            text = "*Mode de paiement :",
            width = 25
        )
        
        self.label_mode_paiement.pack(pady = 2)

        self.menu_paiement = tk.OptionMenu(
            self.fenetre,
            self.mode_paiement,
            "CB", "Espece",
            
        )
        self.menu_paiement.pack(pady = 4)

        self.bouton_valider = tk.Button(
            self.fenetre,
            text = "Valider",
            width = 25
        )

        self.bouton_valider.pack(pady = 6)

        self.bouton_quitter = tk.Button(
            self.fenetre,
            text = "Quitter",
            width = 25,
            command = self.fenetre.destroy
        )
        
        self.bouton_quitter.pack(pady = 6) 

        appliquer_style(self.fenetre)

    def masquer_champs_identite(self):
        
        self.label_nom.pack_forget()
        self.champ_nom.pack_forget()
        self.label_adresse.pack_forget()
        self.champ_adresse.pack_forget()

    def masquer_champs_abonnement(self):
        
        self.label_mode_paiement.pack_forget()
        self.menu_paiement.pack_forget()
        self.label_choix_abonnement.pack_forget()
        self.menu_abonnement.pack_forget()

    def configurer_menu_abonne_classique(self):

        self.choix_abonnement.set("Aucun")
        menu = self.menu_abonnement["menu"]

        self.label_choix_abonnement.config(text = "Modifier mon offre")

        menu.delete(0, "end")
        
        menu.add_command(
            label = "Conserver mon abonnement",
            command = lambda: self.choix_abonnement.set("Aucun")
        )
        menu.add_command(
                label = "Passer au Super",
                command = lambda: self.choix_abonnement.set("Super-abonné")
            )
        



