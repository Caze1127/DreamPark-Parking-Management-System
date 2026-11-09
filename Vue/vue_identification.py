import tkinter as tk

from .theme import FOND, PANNEAU, TEXTE, SECONDAIRE, ACCENT, CARTE, BORDURE, appliquer_style


class VueIdentification:

    def __init__(self, fenetre_principale):
        self.fenetre = tk.Toplevel(fenetre_principale)
        self.fenetre.title('Dream Park | Identification')
        self.fenetre.geometry('550x590')
        self.fenetre.minsize(520, 560)
        self.fenetre.configure(bg=FOND)

        self.label_titre = tk.Label(self.fenetre, text='BIENVENUE CHEZ DREAM PARK',
                                    font=('Segoe UI', 20, 'bold'), fg=TEXTE, bg=FOND)
        self.label_titre.pack(pady=(34, 10))
        tk.Label(self.fenetre, text='Choisissez votre espace pour continuer',
                 font=('Segoe UI', 11), fg=SECONDAIRE, bg=FOND).pack(pady=(0, 28))

        self.cadre_client = tk.Frame(self.fenetre, bg=PANNEAU,
                                     highlightbackground=BORDURE, highlightthickness=1)
        self.cadre_client.pack(fill='x', padx=42, pady=(0, 18))
        self.label_identification = tk.Label(self.cadre_client,
                                            text="Possédez-vous une carte d'abonnement ?",
                                            font=('Segoe UI', 11, 'bold'), fg=TEXTE, bg=PANNEAU)
        self.label_identification.pack(pady=(18, 8))
        self.frame_boutons = tk.Frame(self.cadre_client, bg=PANNEAU)
        self.frame_boutons.pack(pady=(0, 18))
        self.bouton_oui = tk.Button(self.frame_boutons, text='Oui, j’ai une carte', width=17)
        self.bouton_oui.grid(row=0, column=0, padx=7)
        self.bouton_non = tk.Button(self.frame_boutons, text='Non, nouveau client', width=17)
        self.bouton_non.grid(row=0, column=1, padx=7)

        tk.Label(self.fenetre, text='ACCÈS PROFESSIONNELS', font=('Segoe UI', 10, 'bold'),
                 fg=SECONDAIRE, bg=FOND).pack(pady=(1, 10))
        self.bouton_voiturier = tk.Button(self.fenetre, text='↗  Espace voiturier', width=34)
        self.bouton_voiturier.pack(pady=6)
        self.bouton_administrateur = tk.Button(self.fenetre, text='▦  Espace administrateur', width=34)
        self.bouton_administrateur.pack(pady=6)

        self.zone_formulaire = tk.Frame(self.fenetre, bg=FOND)
        self.zone_formulaire.pack(fill='x', padx=75, pady=(12, 0))
        self.label_numero_carte = tk.Label(self.zone_formulaire, text='Numéro de carte :')
        self.champ_numero_carte = tk.Entry(self.zone_formulaire)
        self.label_nom = tk.Label(self.zone_formulaire, text='Nom :')
        self.champ_nom = tk.Entry(self.zone_formulaire)
        self.label_adresse = tk.Label(self.zone_formulaire, text='Adresse :')
        self.champ_adresse = tk.Entry(self.zone_formulaire)
        self.bouton_valider = tk.Button(self.zone_formulaire, text='Valider et continuer', width=34)
        self.bouton_retour = tk.Button(self.zone_formulaire, text='Retour', command=self.fenetre.destroy, width=34)

        appliquer_style(self.zone_formulaire)
        appliquer_style(self.frame_boutons)
        for bouton in (self.bouton_voiturier, self.bouton_administrateur):
            bouton.configure(bg=CARTE, fg=TEXTE, activebackground=BORDURE,
                             activeforeground=TEXTE, relief='flat', bd=0,
                             cursor='hand2', font=('Segoe UI', 11, 'bold'), pady=9)

    def afficher_champs_carte(self):
        for widget in (self.label_numero_carte, self.champ_numero_carte,
                       self.label_nom, self.champ_nom, self.label_adresse,
                       self.champ_adresse, self.bouton_valider):
            widget.pack_forget()
        self.label_numero_carte.pack(pady=4)
        self.champ_numero_carte.pack(fill='x', ipady=6, pady=(0, 12))
        self.bouton_valider.pack(pady=6)

    def afficher_champs_nouveau_client(self):
        for widget in (self.label_numero_carte, self.champ_numero_carte,
                       self.label_nom, self.champ_nom, self.label_adresse,
                       self.champ_adresse, self.bouton_valider):
            widget.pack_forget()
        self.label_nom.pack(pady=4)
        self.champ_nom.pack(fill='x', ipady=5)
        self.label_adresse.pack(pady=4)
        self.champ_adresse.pack(fill='x', ipady=5, pady=(0, 6))
        self.bouton_valider.pack(pady=5)
