from Vue.vue_administrateur import VueAdministrateur
from Class.administrateur import Administrateur
from Vue.vue_voiturier import VueVoiturier
from Class.voiturier import Voiturier
from tkinter import messagebox
from Vue.vue_entree import VueEntree
from Vue.vue_message import VueMessage
from Vue.vue_identification import VueIdentification
from Vue.vue_gestion_abonnement import VueGestionAbonnement
from Vue.vue_desabonnement import VueDesabonnement
from Vue.vue_sortie import VueSortie
from Vue.vue_service import VueService
from Class.voiture import Voiture
from Class.client import Client 
from Class.acces import Acces
from Class.statistique import Statistique
from Class.vue_statistiques_texte import VueStatistiquesTexte
from Class.vue_statistiques_html import VueStatistiquesHTML
from Vue.vue_statistiques import VueStatistiques
from tkinter import filedialog
from secrets import randbelow

class ControleurPrincipal:
    def __init__(self, vue, parking):
        
        self.vue = vue
        self.parking = parking
        self.acces_physiques = {1: Acces(1), 2: Acces(2)}
        
        self.vue.bouton_entree.config(
            command = self.ouvrir_entree
        )

        self.vue.bouton_abonnement.config(
            command = self.ouvrir_gestion_abonnement
        )     

        self.vue.bouton_sortie.config(
            command = self.ouvrir_sortie
        )

        self.vue.bouton_service.config(
            command = self.ouvrir_gestion_service
        )

        self.vue.bouton_statistiques.pack_forget()

        self.vue.fenetre.after(0, self.ouvrir_identification)
        
        self.vue_message = VueMessage(self.vue.fenetre)
        self.clients = []
        self.client_identifie = None
        self.mode_identification = None

    def ouvrir_identification(self):

        self.client_identifie = None
        self.mode_identification = None
        
        self.vue_identification = VueIdentification(self.vue.fenetre)
        
        self.vue_identification.fenetre.transient(self.vue.fenetre)
        self.vue_identification.fenetre.grab_set()

        self.vue_identification.fenetre.protocol(
            "WM_DELETE_WINDOW",
            self.blocage_fenetre
        )
        
        self.vue_identification.bouton_oui.config(
            command = self.selectionner_carte
        )

        self.vue_identification.bouton_valider.config(
            command = self.valider_identification
        )

        self.vue_identification.bouton_non.config(
            command = self.selectionner_nouveau_client
        )

        self.vue_identification.bouton_administrateur.config(
            command=self.ouvrir_espace_administrateur
        )

        self.vue_identification.bouton_voiturier.config(
            command=self.ouvrir_espace_voiturier
        )
        
    def ouvrir_entree(self):

        if self.client_identifie is None:
            return self.vue_message.afficher_erreur("Veuillez vous identifiez")
        
        self.vue_entree = VueEntree(self.vue.fenetre)

        self.vue_entree.fenetre.transient(self.vue.fenetre)
        self.vue_entree.fenetre.grab_set()

        self.vue_entree.bouton_valider.config(
            command = self.valider_entree
        )

        self.vue_entree.bouton_quitter.config(
            command = self.annuler_entree
        )

        self.vue_entree.fenetre.protocol(
            "WM_DELETE_WINDOW",
            self.annuler_entree
        )
        
        if self.client_identifie is not None:

            self.vue_entree.masquer_champs_identite()

            if self.client_identifie.estAbonne : 

                self.vue_entree.masquer_champs_abonnement()

    def ouvrir_sortie(self):
        
        self.vue_sortie = VueSortie(self.vue.fenetre)

        self.vue_sortie.fenetre.transient(self.vue.fenetre)
        self.vue_sortie.fenetre.grab_set()

        self.vue_sortie.bouton_valider.config(
            command = self.valider_sortie
        )

        self.vue_sortie.bouton_annuler.config(
            command = self.annuler_sortie
        )

        self.vue_sortie.fenetre.protocol(
            "WM_DELETE_WINDOW",
            self.annuler_sortie
        )

    def ouvrir_gestion_abonnement(self):
    
            if self.client_identifie is not None:
                
                self.vue_gestion_abonnement = VueGestionAbonnement(self.vue.fenetre)

                self.vue_gestion_abonnement.fenetre.transient(self.vue.fenetre)
                self.vue_gestion_abonnement.fenetre.grab_set()

                self.vue_gestion_abonnement.bouton_quitter.config(
                    command = self.quitter_gestion_abonnement
                )

                self.vue_gestion_abonnement.bouton_valider.config(
                    command = self.valider_souscription
                )

                self.vue_gestion_abonnement.bouton_modifier.config(
                    command = self.ouvrir_formulaire_modification
                )

                self.vue_gestion_abonnement.bouton_desabonner.config(
                    command = self.ouvrir_formulaire_desabonnement
                )
                
                self.vue_gestion_abonnement.fenetre.protocol(
                    "WM_DELETE_WINDOW",
                    self.quitter_gestion_abonnement
                )
                
                if self.client_identifie.estSuperAbonne:
                
                    self.vue_gestion_abonnement.statut.set("Super-abonnement")
                    self.vue_gestion_abonnement.afficher_options_abonne(False)

                elif self.client_identifie.estAbonne:

                    self.vue_gestion_abonnement.statut.set("Abonnement classique")
                    self.vue_gestion_abonnement.afficher_options_abonne(True)

                else:

                    self.vue_gestion_abonnement.statut.set("Aucun abonnement")
                    self.vue_gestion_abonnement.afficher_formulaire_abonnement()

    def ouvrir_formulaire_modification(self):

        self.vue_gestion_abonnement.afficher_formulaire_abonnement()

        self.vue_gestion_abonnement.bouton_valider.config(
            command = self.valider_modification_abonnement
        )

    def ouvrir_formulaire_desabonnement(self):
        
        if self.client_identifie is not None:
                    
            self.vue_desabonnement = VueDesabonnement(self.vue_gestion_abonnement.fenetre)


            if self.client_identifie.estSuperAbonne:
                self.vue_desabonnement.afficher_choix_super_abonne()

            self.vue_desabonnement.fenetre.transient(self.vue_gestion_abonnement.fenetre)
            self.vue_desabonnement.fenetre.grab_set()

            self.vue_desabonnement.bouton_annuler.config(
                command = self.annuler_desabonnement
            )

            self.vue_desabonnement.bouton_confirmer.config(
                command = self.valider_desabonnement
            )
            self.vue_desabonnement.fenetre.protocol(
                "WM_DELETE_WINDOW",
                self.annuler_desabonnement
            )

    def ouvrir_gestion_service(self):
       
        if self.client_identifie == None:
            return self.vue_message.afficher_erreur("Veuillez vous identifié")

        if not self.client_identifie.estAbonne:
            return self.vue_message.afficher_erreur("Vous n'etes pas abonné pour accéder a ce service ")

        self.vue_service = VueService(self.vue.fenetre)
        self.vue_service.fenetre.transient(self.vue.fenetre)
        self.vue_service.fenetre.grab_set()

        self.vue_service.bouton_valider.config(
            command = self.valider_service
        )

        self.vue_service.bouton_lancer_service.config(
            command=self.lancer_service_interface
        )

        self.vue_service.bouton_terminer_service.config(
            command=self.terminer_service_interface
        )

        self.vue_service.bouton_annuler.config(
            command = self.annuler_service
        )

        self.vue_service.fenetre.protocol(
            "WM_DELETE_WINDOW",
            self.annuler_service
        )

        self.vue_service.choix_service.trace_add(
            "write", self.actualiser_heure_service
        )

    def actualiser_heure_service(self, *args):

        if self.vue_service.choix_service.get() == "livraison":
            self.vue_service.afficher_heure()
        else:
            self.vue_service.masquer_heure()

    def valider_identification(self):
        
        if self.mode_identification == "carte":

            numeroCarte = self.vue_identification.champ_numero_carte.get().strip().replace(" ", "") 
            
            if numeroCarte == "":
                return self.vue_message.afficher_erreur("Ce champ est obligatoire")
            
            else:
                
                try :
                
                    numeroDeCarte = int(numeroCarte)

                except ValueError : 
                    
                    return self.vue_message.afficher_erreur("Ce champ doit etre numérique")

                client = self.rechercher_client(numeroDeCarte)
                        
                if client is None:
                    return self.vue_message.afficher_erreur("Numéro de carte inconnu")

                self.vue_message.afficher_information("Vous etes bien identifié")
                self.client_identifie = client 
                self.vue_identification.fenetre.destroy()

        elif self.mode_identification == "nouveau":

            nom = self.vue_identification.champ_nom.get()
            adresse = self.vue_identification.champ_adresse.get()

            if nom.strip() == "" or adresse.strip() == "" :
                return self.vue_message.afficher_erreur("Ce champ est obligatoire")

            client = Client(nom, adresse)
            self.client_identifie = client
            self.clients.append(client)

            if not self.sauvegarder_donnees():
                return

            self.vue_identification.fenetre.destroy()
    
    def valider_entree(self):
        
        immatriculation = Voiture.normaliser_immatriculation(
            self.vue_entree.champ_immatriculation.get()
        )
        strhauteur = self.vue_entree.champ_hauteur.get()
        strlongueur = self.vue_entree.champ_longueur.get ()
        modePaiement =  self.vue_entree.mode_paiement.get()
        choixAbonnement = self.vue_entree.choix_abonnement.get()

        if self.client_identifie is None :

            self.vue_message.afficher_erreur("Client non identifier")
            return 

        client = self.client_identifie

        if not client.estAbonne :

            if modePaiement == "Choisir un paiement":
                return self.vue_message.afficher_erreur(
                    "Veuillez choisir un abonnement avant de valider un choix de paiement"
                )  

            if choixAbonnement == "Choisir un abonnement" : 
                return self.vue_message.afficher_erreur(
                    "Veuillez choisir un abonnement avant de valider un choix de paiement"
                )
                    
        if  immatriculation.strip() == "" :
                    
                return self.vue_message.afficher_erreur("Ce champ est obligatoire")

        try :
                    
            hauteur = float(strhauteur)
            longueur = float(strlongueur)

        except ValueError :
            
            return self.vue_message.afficher_erreur("Ce champ doit etre un nombre") 

        if hauteur <= 0 or longueur <= 0 :
            
            return self.vue_message.afficher_erreur("La hauteur et la longueur doivent être strictement positives.") 
        
        numero_acces = self.vue_entree.numero_acces.get()
        if numero_acces not in (1, 2):
            numero_acces = 1
        acces = getattr(self, "acces_physiques", {}).get(numero_acces) or Acces(numero_acces)

        for placement in self.parking.placements:

            if (
                placement.estEnCours
                and placement.voiture.immatriculation == immatriculation
            ):
                return self.vue_message.afficher_erreur(
                    "Ce véhicule possède déjà un stationnement actif"
                )

        voiture = self.parking.rechercher_voiture(immatriculation)

        if voiture is None:
            voiture = Voiture(hauteur, longueur, immatriculation)
        else:
            if voiture.serviceEnCours in ["maintenance", "entretien"]:
                return self.vue_message.afficher_erreur(
                    "Ce véhicule est actuellement en service"
                )

            voiture.hauteur = hauteur
            voiture.longueur = longueur
        
        resultatEntree = acces.lancer_procedure_entree(
                                client, 
                                voiture, 
                                self.parking, 
                                None, 
                                modePaiement,
                                choixAbonnement
                            )

        if  isinstance(resultatEntree, str):
            
            if resultatEntree.startswith("Ticket -"):
                
                self.actualiser_places()
                resultat = resultatEntree

                if voiture not in client.voitures:
                    client.voitures.append(voiture)
                
                if client.estAbonne:
                    if client.numeroCarte is None:
                        self.attribuer_carte(client)
                    resultat = (f"Votre numéro de carte : {self.formater_numero_carte(client.numeroCarte)}" ) + "\n\n" + resultatEntree

                if client not in self.clients:
                    self.clients.append(client)

                if not self.sauvegarder_donnees():
                    return

                self.vue_message.afficher_information(resultat)      
                self.vue_entree.fenetre.destroy()
                self.terminer_session()    
                
            
            else:
                return self.vue_message.afficher_erreur(resultatEntree)

    def valider_souscription(self):
        client = self.client_identifie
        choixAbonnement = self.vue_gestion_abonnement.choix_abonnement.get()
        modePaiement = self.vue_gestion_abonnement.mode_paiement.get()

        if client is None:
            return self.vue_message.afficher_erreur("Veuillez vous identifier")

        elif client.estAbonne :
            return self.vue_message.afficher_erreur("Vous etes déja abonné")
        
        if choixAbonnement == "Choisir un abonnement":
            return self.vue_message.afficher_erreur("Veuillez choisir un abonnement")

        if modePaiement == "Choisir un paiement":
            return self.vue_message.afficher_erreur("Veuillez choisir un mode de paiement")

        acces = Acces()
        resultat = acces.gerer_abonnement(client ,self.parking, modePaiement, choixAbonnement)

        if resultat is None :

            if not client.estAbonne:
                return self.vue_message.afficher_erreur("La souscription n'a pas été effectuée")

            if client.numeroCarte is None:

                self.attribuer_carte(client)

            if client not in self.clients : 
                
                self.clients.append(client)

            if not self.sauvegarder_donnees():
                return

            self.vue_message.afficher_information(f"Abonnement : {choixAbonnement} - Numéro de carte : {self.formater_numero_carte(client.numeroCarte)}")
            self.vue_gestion_abonnement.fenetre.destroy()
            self.terminer_session()
            

        else :
            return self.vue_message.afficher_erreur(resultat)

    def valider_modification_abonnement(self):
        client = self.client_identifie
        choixAbonnement = self.vue_gestion_abonnement.choix_abonnement.get()
        modePaiement = self.vue_gestion_abonnement.mode_paiement.get()

        if client is None:
            return self.vue_message.afficher_erreur("Veuillez vous identifié")

        if not client.estAbonne:
            return self.vue_message.afficher_erreur("Vous n'avais pas d'abonnement")

        if client.estSuperAbonne:
            return self.vue_message.afficher_erreur("Vous possédez déjà l'abonnement maximal")

        if choixAbonnement =="Choisir un abonnement":
            return self.vue_message.afficher_erreur("Veuillez choisir un abonnement")
         
        if modePaiement == "Choisir un paiement":
            return self.vue_message.afficher_erreur("Veuillez choisir un mode de paiement")

        if choixAbonnement != "Super-abonné":
            return self.vue_message.afficher_erreur("Veuillez choisir un abonnement supérieurs au votre")

        if choixAbonnement == "Super-abonné":
            client.superSAbonner()

        if not self.sauvegarder_donnees():
            return

        self.vue_message.afficher_information(f"Abonnement : {choixAbonnement} - Numéro de carte : {self.formater_numero_carte(client.numeroCarte)}")
        self.vue_gestion_abonnement.fenetre.destroy()
        self.terminer_session()

    def valider_desabonnement(self):

        client = self.client_identifie
        choix_desabonnement = self.vue_desabonnement.choix_desabonnement.get()
        message_confirmation = ""
        
        if client is None :
            return self.vue_message.afficher_erreur("Veuillez vous identifier")

        if not client.estAbonne:
            return self.vue_message.afficher_erreur("Vous n'avez pas d'abonnement")
        
        if client.estSuperAbonne :

            if choix_desabonnement == "Choisir une option":
                return self.vue_message.afficher_erreur("Veuillez faire un choix")
            
            elif choix_desabonnement == "Devenir abonné classique" :
                
                client.SuperSeDesabonner()
                message_confirmation = (
                    "Votre super-abonnement a été remplacé par un abonnement classique.\n\n"
                    + "Votre numéro de carte reste inchangé."
                )
            
            elif choix_desabonnement == "Résilier complètement" :
                
                client.seDesabonner()
                message_confirmation = "Votre abonnement a été résilié. Vous n'êtes désormais plus abonné à DreamPark."

            else:
                return self.vue_message.afficher_information("Choix de désabonnement invalide")
        elif client.estAbonne:
            
            client.seDesabonner()
            message_confirmation = "Votre abonnement a été résilié. Vous n'êtes désormais plus abonné à DreamPark."

         
        if not self.sauvegarder_donnees():
            return

        self.vue_message.afficher_information(message_confirmation)
        self.vue_desabonnement.fenetre.destroy()
        self.vue_gestion_abonnement.fenetre.destroy()
        self.terminer_session()

    def valider_sortie(self):
        
        ticket = self.vue_sortie.champ_ticket.get()
        
        if ticket.strip() == "":
            return self.vue_message.afficher_erreur(
                "Veuillez saisir votre ticket"
            )

        numero_acces = self.vue_sortie.numero_acces.get()
        if numero_acces not in (1, 2):
            numero_acces = 1
        acces = getattr(self, "acces_physiques", {}).get(numero_acces) or Acces(numero_acces)
        resultat = acces.lancer_procedure_sortie(ticket, self.parking)

        if isinstance(resultat, str):
            return self.vue_message.afficher_erreur(resultat)

        elif not resultat:
            return self.vue_message.afficher_erreur("Récupération impossible")

        if isinstance(resultat, Voiture):
            if not self.sauvegarder_donnees():
                return
            self.vue_message.afficher_information(f"Votre véhicule {resultat.immatriculation} a été récupéré avec succès.")            
            self.actualiser_places()
            self.vue_sortie.fenetre.destroy()
            self.terminer_session()

    def valider_service(self):

        immatriculation = Voiture.normaliser_immatriculation(self.vue_service.champ_immatriculation.get())
        choixService = self.vue_service.choix_service.get()
        client = self.client_identifie
        
        if immatriculation == "":
            return self.vue_message.afficher_erreur(
                "Veuillez renseigner votre immatriculation"
            )

        if choixService == "Choisir un service":
            return self.vue_message.afficher_erreur(
                "Veuillez choisir un service"
            )
    
        voiture = client.rechercherVoiture(immatriculation)

        if voiture is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture n'appartient pas au client identifié"
            )

        acces = Acces()
        placement = acces.rechercher_placement_actif(voiture)

        if placement is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture ne possède aucun stationnement actif"
            )

        if choixService == "livraison":

            self.vue_service.afficher_heure()

            heureLivraison = self.vue_service.champ_heure.get().strip()

            if heureLivraison == "":
                return

            try:
                from datetime import datetime
                datetime.strptime(heureLivraison, "%H:%M")

            except ValueError:
                return self.vue_message.afficher_erreur(
                    "Veuillez saisir une heure valide au format HH:MM"
                )

            resultatModification = acces.modifier_service(
                client,
                voiture,
                choixService,
                heure_livraison=heureLivraison
            )
            
        else:

            self.vue_service.masquer_heure()

            resultatModification = acces.modifier_service(
                client,
                voiture,
                choixService
            )

        if not resultatModification:
            return self.vue_message.afficher_erreur(
                "Impossible d'enregistrer le service demandé"
            )

        if not self.sauvegarder_donnees():
            return

        self.vue_message.afficher_information(
            f"Le service '{choixService}' a été enregistré "
            f"pour le véhicule {immatriculation}."
        )

        self.vue_service.fenetre.destroy()
        self.terminer_session()

    def lancer_service_interface(self):

        immatriculation = Voiture.normaliser_immatriculation(self.vue_service.champ_immatriculation.get())
        client = self.client_identifie

        if client is None:
            return self.vue_message.afficher_erreur(
                "Veuillez vous identifier"
            )

        if immatriculation == "":
            return self.vue_message.afficher_erreur(
                "Veuillez renseigner votre immatriculation"
            )

        voiture = client.rechercherVoiture(immatriculation)

        if voiture is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture n'appartient pas au client identifié"
            )

        acces = Acces()

        placement = acces.rechercher_placement_actif(voiture)

        if placement is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture ne possède aucun stationnement actif"
            )

        if placement.service not in ["maintenance", "entretien"]:
            return self.vue_message.afficher_erreur(
                "Aucun entretien ou maintenance n'est enregistré pour ce véhicule"
            )

        resultat = acces.lancer_service(voiture)

        if not resultat:
            return self.vue_message.afficher_erreur(
                "Impossible de lancer le service"
            )

        self.actualiser_places()

        if not self.sauvegarder_donnees():
            return

        self.vue_message.afficher_information(
            f"Le service '{placement.service}' a été lancé "
            f"pour le véhicule {immatriculation}."
        )

        self.vue_service.fenetre.destroy()
        self.terminer_session()
    
    def lancer_livraison_interface(self):

        immatriculation = Voiture.normaliser_immatriculation(self.vue_service.champ_immatriculation.get())
        client = self.client_identifie

        if client is None:
            return self.vue_message.afficher_erreur(
                "Veuillez vous identifier"
            )

        if immatriculation == "":
            return self.vue_message.afficher_erreur(
                "Veuillez renseigner votre immatriculation"
            )

        voiture = client.rechercherVoiture(immatriculation)

        if voiture is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture n'appartient pas au client identifié"
            )

        acces = Acces()

        placement = acces.rechercher_placement_actif(voiture)

        if placement is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture ne possède aucun stationnement actif"
            )

        if placement.service != "livraison":
            return self.vue_message.afficher_erreur(
                "Aucune livraison n'est enregistrée pour ce véhicule"
            )

        if not placement.adresseLivraison or not placement.heureLivraison:
            return self.vue_message.afficher_erreur(
                "L'adresse ou l'heure de livraison est manquante"
            )

        resultat = acces.lancer_livraison(voiture)

        if not resultat:
            return self.vue_message.afficher_erreur(
                "Impossible de lancer la livraison"
            )

        self.actualiser_places()

        if not self.sauvegarder_donnees():
            return

        self.vue_message.afficher_information(
            f"La livraison du véhicule {immatriculation} a été effectuée.\n"
            f"Adresse : {placement.adresseLivraison}\n"
            f"Heure demandée : {placement.heureLivraison}"
        )

        self.vue_service.fenetre.destroy()
        self.terminer_session()

    def ouvrir_espace_administrateur(self):
        self.vue_identification.fenetre.destroy()
        self.client_identifie = None
        self.vue_administrateur = VueAdministrateur(self.vue.fenetre)
        self.vue_administrateur.fenetre.transient(self.vue.fenetre)
        self.vue_administrateur.fenetre.grab_set()

        self.vue_administrateur.bouton_statistiques.config(
            command=self.ouvrir_statistiques
        )
        self.vue_administrateur.bouton_retour.config(
            command=self.fermer_espace_administrateur
        )
        self.vue_administrateur.fenetre.protocol(
            "WM_DELETE_WINDOW", self.fermer_espace_administrateur
        )

    def fermer_espace_administrateur(self):
        self.vue_administrateur.fenetre.destroy()
        self.ouvrir_identification()

    def ouvrir_statistiques(self):

        self.vue_statistiques = VueStatistiques(self.vue.fenetre)

        self.vue_statistiques.fenetre.transient(self.vue.fenetre)
        self.vue_statistiques.fenetre.grab_set()

        self.vue_statistiques.bouton_actualiser.config(
            command = self.actualiser_statistiques
        )

        self.vue_statistiques.bouton_exporter_texte.config(
            command = self.exporter_statistiques_texte
        )

        self.vue_statistiques.bouton_exporter_html.config(
            command = self.exporter_statistiques_html
        )

        self.vue_statistiques.bouton_fermer.config(
            command = self.fermer_statistiques
        )

        self.vue_statistiques.fenetre.protocol(
            "WM_DELETE_WINDOW",
            self.fermer_statistiques
        )

        self.actualiser_statistiques()

    def actualiser_statistiques(self):

        administrateur = Administrateur("Administrateur Dream Park")
        resume = administrateur.consulter_statistiques(self.parking)

        self.vue_statistiques.afficher_statistiques(resume)

        return resume

    def exporter_statistiques_texte(self):

        chemin = filedialog.asksaveasfilename(
            parent=self.vue_statistiques.fenetre,
            title="Enregistrer les statistiques en TXT",
            defaultextension=".txt",
            initialfile="statistiques_dreampark.txt",
            filetypes=[("Fichiers texte", "*.txt")]
        )

        if not chemin:
            return

        resume = self.actualiser_statistiques()

        try:
            VueStatistiquesTexte().enregistrer(resume, chemin)

        except OSError as erreur:
            return self.vue_message.afficher_erreur(f"Enregistrement impossible : {erreur}")

        self.vue_message.afficher_information("Les statistiques ont été enregistrées en TXT")

    def exporter_statistiques_html(self):

        chemin = filedialog.asksaveasfilename(
            parent=self.vue_statistiques.fenetre,
            title="Enregistrer les statistiques en HTML",
            defaultextension=".html",
            initialfile="statistiques_dreampark.html",
            filetypes=[("Fichiers HTML", "*.html")]
        )

        if not chemin:
            return

        resume = self.actualiser_statistiques()

        try:
            VueStatistiquesHTML().enregistrer(resume, chemin)

        except OSError as erreur:
            return self.vue_message.afficher_erreur(f"Enregistrement impossible : {erreur}")

        self.vue_message.afficher_information("Les statistiques ont été enregistrées en HTML")

    def fermer_statistiques(self):

        self.vue_statistiques.fenetre.destroy()
        vue_administrateur = getattr(self, "vue_administrateur", None)
        if vue_administrateur is not None and vue_administrateur.fenetre.winfo_exists():
            vue_administrateur.fenetre.grab_set()

    def actualiser_places(self):
            
        nombre = self.parking.nombre_places_libres()
        self.vue.afficher_nombre_places(nombre)

    def rechercher_client(self, numeroCarte):

        if numeroCarte is None :
            return None 
        
        for client in self.clients:
            
            if client.numeroCarte == numeroCarte:
                return client
        
        return None  

    @staticmethod
    def formater_numero_carte(numero):
        texte = str(numero)
        if len(texte) == 8 and texte.isdigit():
            return f"{texte[:4]} {texte[4:]}"
        return texte

    def attribuer_carte(self, client):
        if client.estAbonne and client.numeroCarte is None:
            numeros_existants = {
                c.numeroCarte for c in self.clients if c.numeroCarte is not None
            }
            numero = 10_000_000 + randbelow(90_000_000)
            while numero in numeros_existants:
                numero = 10_000_000 + randbelow(90_000_000)
            client.numeroCarte = numero
            return client

    def selectionner_carte(self,):
        
        self.mode_identification = "carte" 
        self.vue_identification.afficher_champs_carte()

    def selectionner_nouveau_client(self):
        
        self.mode_identification = "nouveau"
        self.vue_identification.afficher_champs_nouveau_client()

    def terminer_session(self):
        
       self.client_identifie = None
       self.ouvrir_identification()

    def blocage_fenetre(self):
        
        self.vue_message.afficher_erreur("L'identification est obligatoire")

    def annuler_entree(self):
        
        self.vue_entree.fenetre.destroy()
        self.terminer_session()

    def annuler_sortie(self):
            
        self.vue_sortie.fenetre.destroy()
        self.terminer_session()
    
    def annuler_desabonnement(self):

        self.vue_desabonnement.fenetre.destroy()
        self.vue_gestion_abonnement.fenetre.grab_set()

    def annuler_service(self):

        self.vue_service.fenetre.destroy()
        self.terminer_session()
        
    def quitter_gestion_abonnement(self):
    
        self.vue_gestion_abonnement.fenetre.destroy()
        self.terminer_session()

    def quitter_sans_identification(self):
        
        self.vue_identification.fenetre.destroy()
        self.ouvrir_sortie()

    def terminer_service_interface(self):

        immatriculation = Voiture.normaliser_immatriculation(self.vue_service.champ_immatriculation.get())
        client = self.client_identifie

        if client is None:
            return self.vue_message.afficher_erreur(
                "Veuillez vous identifier"
            )

        if immatriculation == "":
            return self.vue_message.afficher_erreur(
                "Veuillez renseigner votre immatriculation"
            )

        voiture = client.rechercherVoiture(immatriculation)

        if voiture is None:
            return self.vue_message.afficher_erreur(
                "Cette voiture n'appartient pas au client identifié"
            )

        if voiture.serviceEnCours not in ["maintenance", "entretien"]:
            return self.vue_message.afficher_erreur(
                "Cette voiture n'a aucun service en cours"
            )

        acces = Acces()

        resultat = acces.terminer_service(voiture)

        if not resultat:
            return self.vue_message.afficher_erreur(
                "Impossible de terminer le service. "
                "Vérifiez qu'une place adaptée est disponible."
            )

        self.actualiser_places()

        placement = voiture.placements[-1]
        if voiture.priseEnChargeGarantie:
            emplacement = "Prise en charge garantie (sans place physique)"
            nouveau_ticket = acces.borne.delivrer_ticket_garanti(voiture)
        else:
            emplacement = f"Nouvelle place attribuée : {voiture.place.numero}"
            nouveau_ticket = acces.borne.delivrer_ticket(voiture, voiture.place)

        if not self.sauvegarder_donnees():
            return

        self.vue_message.afficher_information(
            f"Le service du véhicule {immatriculation} est terminé.\n"
            f"{emplacement}\n\nNouveau ticket : {nouveau_ticket}"
        )

        self.vue_service.fenetre.destroy()
        self.terminer_session()
    def ouvrir_espace_voiturier(self):
        self.vue_identification.fenetre.destroy()
        self.client_identifie = None
        self.vue_voiturier = VueVoiturier(self.vue.fenetre)
        self.vue_voiturier.fenetre.transient(self.vue.fenetre)
        self.vue_voiturier.fenetre.grab_set()

        self.vue_voiturier.bouton_actualiser.config(
            command=self.actualiser_livraisons_voiturier
        )
        self.vue_voiturier.bouton_livrer.config(
            command=self.effectuer_livraison_voiturier
        )
        self.vue_voiturier.bouton_retour.config(
            command=self.fermer_espace_voiturier
        )
        self.vue_voiturier.fenetre.protocol(
            "WM_DELETE_WINDOW", self.fermer_espace_voiturier
        )
        self.actualiser_livraisons_voiturier()

    def actualiser_livraisons_voiturier(self):
        livraisons = []

        for placement in self.parking.placements:
            if placement.estEnCours and placement.service == "livraison":
                if placement.adresseLivraison and placement.heureLivraison:
                    livraisons.append((
                        placement.voiture.immatriculation,
                        placement.adresseLivraison,
                        placement.heureLivraison
                    ))

        self.vue_voiturier.afficher_livraisons(livraisons)

    def effectuer_livraison_voiturier(self):
        immatriculation = self.vue_voiturier.immatriculation_selectionnee()

        if immatriculation is None:
            return self.vue_message.afficher_erreur(
                "Veuillez sélectionner une livraison"
            )

        if not messagebox.askyesno(
            "Confirmer la livraison",
            f"Confirmer la livraison du véhicule {immatriculation} ?",
            parent=self.vue_voiturier.fenetre
        ):
            return

        voiturier = Voiturier("Voiturier Dream Park")
        resultat = voiturier.effectuer_livraison(
            immatriculation, self.parking
        )

        if not resultat:
            return self.vue_message.afficher_erreur(
                "Impossible d'effectuer cette livraison"
            )

        self.actualiser_places()

        if not self.sauvegarder_donnees():
            return

        self.actualiser_livraisons_voiturier()
        self.vue_message.afficher_information(
            f"La livraison du véhicule {immatriculation} est terminée"
        )

    def fermer_espace_voiturier(self):
        self.vue_voiturier.fenetre.destroy()
        self.ouvrir_identification()

    
    def fermer_application(self):

        if not self.sauvegarder_donnees():
            return

        self.vue.fenetre.destroy()

    def sauvegarder_donnees(self):
        try:
            self.sauvegarde.enregistrer(self.parking, self.clients)
            return True
        except (OSError, TypeError, ValueError, AttributeError) as erreur:
            self.vue_message.afficher_erreur(
                f"Impossible de sauvegarder les données : {erreur}"
            )
            return False
