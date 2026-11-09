import tkinter as tk
from .theme import appliquer_style 

class VueGestionAbonnement():
    def __init__(self, fenetre_principale):

        self.fenetre = tk.Toplevel(fenetre_principale)

        self.fenetre.title("Gestion de mon abonnement")
        self.fenetre.geometry("500x450")

        self.statut = tk.StringVar()
        self.mode_paiement = tk.StringVar(value = "Choisir un paiement")
        self.choix_abonnement = tk.StringVar(value = "Choisir un abonnement")

        self.label_titre = tk.Label(
            self.fenetre,
            text="GESTION DE MON ABONNEMENT",
            font=("Arial", 20, "bold"),
            width = 30
        )

        self.label_titre.pack(pady= 5 )

        self.label_statut = tk.Label(
            self.fenetre,
            textvariable = self.statut,
            font=("Arial", 20, "bold"),
            width = 30
        )

        self.label_statut.pack(pady = 30)

        self.label_abonnement = tk.Label(
            self.fenetre,
            text = "Choix de l'abonnement"
        )

        self.menu_abonnement = tk.OptionMenu(
            self.fenetre,
            self.choix_abonnement,
            "Abonné classique","Super-abonné"
        )

        self.label_mode_paiement = tk.Label(
            self.fenetre,
            text = "*Mode de paiement :",
            width = 25
        )

        self.menu_paiement = tk.OptionMenu(
            self.fenetre,
            self.mode_paiement,
            "CB", "Espece",
            
        )

        self.bouton_modifier = tk.Button(
            self.fenetre,
            text = "Modifier mon abonnement",
            width = 25
        )
            
        self.bouton_valider = tk.Button(
            self.fenetre,
            text = "Valider",
            width = 25
            )

        self.bouton_desabonner = tk.Button(
            self.fenetre,
            text = "Se Desabonner",
            width = 25
        )
        
        self.bouton_quitter = tk.Button(
            self.fenetre,
            text = "Quitter",
            width = 25
        )

        self.bouton_quitter.pack()

        appliquer_style(self.fenetre)

    def afficher_formulaire_abonnement(self):

        self.bouton_desabonner.pack_forget()
        self.bouton_modifier.pack_forget()
        self.bouton_valider.pack_forget()
        self.label_abonnement.pack_forget()
        self.menu_abonnement.pack_forget()
        self.label_mode_paiement.pack_forget()
        self.menu_paiement.pack_forget()

        self.bouton_valider.pack(
            before = self.bouton_quitter,
            pady = 5
        )

        self.menu_paiement.pack(
            before = self.bouton_valider,
            pady = 5
        )

        self.label_mode_paiement.pack(
            before = self.menu_paiement,
            pady = 5
        )

        self.menu_abonnement.pack(
            before = self.label_mode_paiement,
            pady = 5
        )

        self.label_abonnement.pack(
            before = self.menu_abonnement,
            pady = 5
        )

    def afficher_options_abonne(self, peut_modifier):

        self.bouton_valider.pack_forget()
        self.label_abonnement.pack_forget()
        self.menu_abonnement.pack_forget()
        self.label_mode_paiement.pack_forget()
        self.menu_paiement.pack_forget()

        self.bouton_desabonner.pack(
                before = self.bouton_quitter,
                pady = 5 
            )
        
        if peut_modifier:

            menu = self.menu_abonnement["menu"]
    
            menu.delete(0, "end")
            
            menu.add_command(
                label = "Passer au Super",
                command=lambda: self.choix_abonnement.set("Super-abonné")
            )
            
            self.bouton_modifier.pack(
                before = self.bouton_desabonner,
                pady = 5
            )

    

            

    