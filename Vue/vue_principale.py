import tkinter as tk

from .theme import FOND, PANNEAU, CARTE, ACCENT, TEXTE, SECONDAIRE, BORDURE, appliquer_style


class VuePrincipale:

    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title('Dream Park | Parking intelligent')
        self.fenetre.geometry('780x690')
        self.fenetre.minsize(720, 650)
        self.fenetre.configure(bg=FOND)

        self.entete = tk.Frame(self.fenetre, bg=FOND)
        self.entete.pack(fill='x', padx=42, pady=(35, 14))

        self.titre = tk.Label(self.entete, text='DREAM PARK',
                              font=('Segoe UI', 28, 'bold'), fg=TEXTE, bg=FOND)
        self.titre.pack(anchor='w')
        tk.Label(self.entete, text='GESTION DE PARKING  /  TABLEAU DE BORD',
                 font=('Segoe UI', 10, 'bold'), fg=ACCENT, bg=FOND).pack(anchor='w', pady=(1, 0))

        self.panneau_places = tk.Frame(self.fenetre, bg=PANNEAU,
                                      highlightbackground=BORDURE, highlightthickness=1)
        self.panneau_places.pack(fill='x', padx=42, pady=(10, 18))
        tk.Label(self.panneau_places, text='DISPONIBILITÉ EN TEMPS RÉEL',
                 font=('Segoe UI', 10, 'bold'), fg=SECONDAIRE, bg=PANNEAU).pack(anchor='w', padx=23, pady=(17, 4))
        self.label_places = tk.Label(self.panneau_places, text='Places disponibles : 0',
                                     font=('Segoe UI', 22, 'bold'), fg=TEXTE, bg=PANNEAU)
        self.label_places.pack(anchor='w', padx=23)
        ligne = tk.Frame(self.panneau_places, bg=PANNEAU)
        ligne.pack(fill='x', padx=23, pady=(10, 19))
        self.label_acces_1 = tk.Label(ligne, text='Accès 1 — Places disponibles : 0',
                                     font=('Segoe UI', 10), fg=ACCENT, bg=PANNEAU)
        self.label_acces_1.pack(side='left')
        self.label_acces_2 = tk.Label(ligne, text='Accès 2 — Places disponibles : 0',
                                     font=('Segoe UI', 10), fg=ACCENT, bg=PANNEAU)
        self.label_acces_2.pack(side='right')

        tk.Label(self.fenetre, text='OPÉRATIONS', font=('Segoe UI', 11, 'bold'),
                 fg=SECONDAIRE, bg=FOND).pack(anchor='w', padx=42, pady=(0, 10))

        self.zone_actions = tk.Frame(self.fenetre, bg=FOND)
        self.zone_actions.pack(fill='x', padx=42)
        self.bouton_entree = tk.Button(self.zone_actions, text='➕  Entrer un véhicule', width=25)
        self.bouton_entree.grid(row=0, column=0, sticky='ew', padx=(0, 7), pady=6)
        self.bouton_sortie = tk.Button(self.zone_actions, text='↗  Récupérer un véhicule', width=25)
        self.bouton_sortie.grid(row=0, column=1, sticky='ew', padx=(7, 0), pady=6)
        self.bouton_service = tk.Button(self.zone_actions, text='⚙  Gérer un service', width=25)
        self.bouton_service.grid(row=1, column=0, sticky='ew', padx=(0, 7), pady=6)
        self.bouton_abonnement = tk.Button(self.zone_actions, text='◈  Mon abonnement', width=25)
        self.bouton_abonnement.grid(row=1, column=1, sticky='ew', padx=(7, 0), pady=6)
        self.zone_actions.grid_columnconfigure(0, weight=1)
        self.zone_actions.grid_columnconfigure(1, weight=1)

        self.bouton_statistiques = tk.Button(self.fenetre, text='Statistiques', width=25)
        self.bouton_statistiques.pack(pady=(6, 0))
        self.bouton_statistiques.configure(bg=CARTE, fg=TEXTE, relief='flat', bd=0, font=('Segoe UI', 10, 'bold'), pady=7)
        self.bouton_quitter = tk.Button(self.fenetre, text='Quitter Dream Park', width=25,
                                        command=self.fenetre.destroy)
        self.bouton_quitter.pack(side='bottom', pady=(5, 24))
        tk.Label(self.fenetre, text='DEUX BORNES CONNECTÉES  •  20 PLACES  •  3 NIVEAUX',
                 font=('Segoe UI', 9), fg=SECONDAIRE, bg=FOND).pack(side='bottom', pady=(10, 5))

        appliquer_style(self.zone_actions)
        self.bouton_quitter.configure(bg=CARTE, fg=TEXTE, activebackground=BORDURE, activeforeground=TEXTE)

    def afficher_nombre_places(self, nombre):
        self.label_places.config(text=f'{nombre} places disponibles')
        self.label_acces_1.config(text=f'●  Accès 1 : {nombre} places')
        self.label_acces_2.config(text=f'●  Accès 2 : {nombre} places')
