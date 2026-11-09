from .camera import Camera
from .borne_ticket import BorneTicket
from .teleporteur import Teleporteur
from .panneau_affichage import PanneauAffichage
from .voiture import Voiture


class Acces:
    def __init__(self, numero=1):
        if numero not in (1, 2):
            raise ValueError("Le numéro d’accès doit être 1 ou 2")
        self.numero = numero
        self.camera = Camera()
        self.borne = BorneTicket()
        self.teleporteur1 = Teleporteur()
        self.teleporteur2 = Teleporteur()
        self.panneau = PanneauAffichage()

    def memoriser_entree(self, voiture):
        placement = next((p for p in reversed(voiture.placements) if p.estEnCours), None)
        if placement is not None:
            placement.accesEntree = self.numero

    def actionner_camera(self, voiture):
        
        camera = self.camera
        hauteur = camera.capturer_hauteur(voiture)
        longueur = camera.capturer_longueur(voiture)
        immatriculation = camera.capturer_immatriculation(voiture)
        return hauteur,longueur,immatriculation

    def actionnerPanneau(self, parking):
        return self.panneau.afficherNbPlacesDisponibles(parking)
    
    def retrouver_voiture_ticket(self, ticket, parking):

        reference = ticket.strip().upper()

        if len(reference) != 6:
            return "Ticket invalide"

        if any(caractere not in "0123456789ABCDEF" for caractere in reference):
            return "Ticket invalide"

        for placement in parking.placements:

            if placement.estEnCours and placement.reference_courte == reference:

                voiture = placement.voiture

                if voiture.estDansParking or voiture.priseEnChargeGarantie:
                    return voiture

        return "Ticket invalide ou expiré"

    def gerer_abonnement(self, client, parking, mode_paiement, choix_abonnement):
        
        est_abonne, est_super_abonne = self.borne.recuperer_infos_carte(client)
        
        
        
        if not est_abonne:
            
            if choix_abonnement == "Aucun":
                
                paiement = self.borne.valider_mode_paiement(mode_paiement)
                                            
                if paiement is None:
                    return "Erreur veuillez choisir votre mode de paiement"
            
            else:
                abonnement = self.borne.valider_choix_abonnement(
                    choix_abonnement, parking
                    )
                
                if abonnement is None:
                    return "Erreur : abonnement invalide"
                
                if abonnement.estPackGar:
                    paiement = self.borne.valider_mode_paiement(mode_paiement)
                            
                    if paiement is None:
                        return "Erreur veuillez choisir votre mode de paiement"
    
                    else:      
                        client.superSAbonner()

                else:
                    
                    paiement = self.borne.valider_mode_paiement(mode_paiement)
                            
                    if paiement is None:
                        return "Erreur veuillez choisir votre mode de paiement"
    
                    else:      
                        client.sAbonner()
        
        elif not est_super_abonne and est_abonne:

            if choix_abonnement == "Super-abonné":
            
                abonnement = self.borne.valider_choix_abonnement(
                    choix_abonnement, parking
                    )
                
                if abonnement is None:
                    return "Erreur : abonnement invalide"
                
                if abonnement.estPackGar:
                    paiement = self.borne.valider_mode_paiement(mode_paiement)
                            
                    if paiement is None:
                        return "Erreur veuillez choisir votre mode de paiement"

                    else:      
                        client.superSAbonner()



    def gerer_service(self, client, choix_service):
        
        est_abonne = self.borne.recuperer_infos_carte(client)[0]                    
        
        service = "aucun"
        
        if est_abonne and choix_service is not None:
           choix = self.borne.valider_choix_service(choix_service)

           if choix is None:
               return None  
           
           service = choix     
        return service 
                
    def gerer_prise_en_charge_garantie(self, voiture, parking, service, adresse_livraison, heure_livraison):
        
        self.teleporteur1.teleporter_voiture_super_abonne(voiture , parking ,service, adresse_livraison, heure_livraison)
        
        parking.ajouter_voiture_garantie(voiture)
        
        ticket = self.borne.delivrer_ticket_garanti(voiture)
        
        return ticket

    def lancer_service(self, voiture):
        return self.teleporteur2.envoyer_en_service(voiture)

    def terminer_service(self, voiture):
        return self.teleporteur2.retour_service(voiture)

    def rechercher_placement_actif(self, voiture):

        for placement in voiture.placements:

            if placement.estEnCours:
                return placement 
        
        return None
        
    def modifier_service(
        self,
        client,
        voiture,
        nouveau_service,
        heure_livraison=None
        ):

        rech = self.rechercher_placement_actif(voiture)

        if rech is None:
            return False

        service = self.gerer_service(client, nouveau_service)

        if service is None:
            return False

        if service == "livraison":
            
            if heure_livraison is None:
                return False

            rech.adresseLivraison = client.adresse
            rech.heureLivraison = heure_livraison
        else:
            rech.adresseLivraison = None
            rech.heureLivraison = None 

        rech.service = service
        
        if voiture.priseEnChargeGarantie: 
            voiture.serviceGaranti = service

        return True  
    
    def lancer_livraison(self, voiture):
        
        if voiture.priseEnChargeGarantie:
            return self.teleporteur2.livrer_voiture_garantie(voiture)
        
        return self.teleporteur2.livrer_voiture(voiture)
        

    def lancer_procedure_entree(
                self,
                client,
                voiture,
                parking,
                choix_service = None,
                mode_paiement = None,
                choix_abonnement = None, 
                heure_livraison = None
                ):
    
            hauteur, longueur, immatriculation = self.actionner_camera(voiture)
    
            if hauteur <= 0 or longueur <= 0 or immatriculation == "":
                return "Informations du véhicule invalides"

            immatriculation = Voiture.normaliser_immatriculation(immatriculation)
            voiture.immatriculation = immatriculation
            if not immatriculation:
                return "Informations du véhicule invalides"

            ancienne_voiture = parking.rechercher_voiture(immatriculation)
            if ancienne_voiture is not None and ancienne_voiture is not voiture:
                return "Utilisez le véhicule déjà enregistré pour cette immatriculation"

            for ancien_placement in parking.placements:
                if ancien_placement.voiture.immatriculation == immatriculation:
                    if ancien_placement.estEnCours:
                        return "Ce véhicule possède déjà un stationnement actif"
                    if ancien_placement.voiture.serviceEnCours in ("maintenance", "entretien"):
                        return "Ce véhicule est actuellement en service"

            est_super_abonne = self.borne.recuperer_infos_carte(client)[1]

            if parking.nombre_places_libres() == 0 :
                            
                if est_super_abonne:
                    resultat_service = self.gerer_service(client, choix_service)

                    if resultat_service is None:
                        return "Erreur veuillez faire un choix de service"

                    service = resultat_service

                    adresse_livraison = None
                    
                    if service == "livraison": 
                                    
                        if heure_livraison is None:
                            return "Erreur: Heure de livraison non fournie"
                        
                        else:
                            adresse_livraison = client.adresse
                    
                    charge_garantie = self.gerer_prise_en_charge_garantie(voiture, parking, service, adresse_livraison, heure_livraison)
                    parking.enregistrer_voiture(client, voiture)
                    self.memoriser_entree(voiture)
                    return charge_garantie
                return "Le parking est plein"
                
            place = parking.rechercher_place(voiture)
                
            if place is None:
                            
                if est_super_abonne:
                    resultat_service = self.gerer_service(client, choix_service)
                                                
                    if resultat_service is None:
                        return "Erreur veuillez faire un choix de service"

                    service = resultat_service

                    adresse_livraison = None
                    
                    if service == "livraison": 
                                    
                        if heure_livraison is None:
                            return "Erreur: Heure de livraison non fournie"
                        
                        else:
                            adresse_livraison = client.adresse

                    charge_garantie = self.gerer_prise_en_charge_garantie(voiture, parking, service, adresse_livraison, heure_livraison)
                    parking.enregistrer_voiture(client, voiture)
                    self.memoriser_entree(voiture)
                    return charge_garantie
                
                return "Aucune place disponible adaptée à ce véhicule"

            resultat_abonnement = self.gerer_abonnement(client,parking,mode_paiement,choix_abonnement)
            
            if resultat_abonnement is not None:
                return resultat_abonnement

            resultat_service = self.gerer_service(client, choix_service)
            
            if resultat_service is None:
                return "Erreur veuillez faire un choix de service"

            service = resultat_service      

            adresse_livraison = None

            if service == "livraison": 
                
                if heure_livraison is None:
                    return "Erreur: Heure de livraison non fournie"
                
                else:
                    adresse_livraison = client.adresse
                                         
            resultat_stationnement = self.teleporteur1.teleporter_voiture(
                voiture, 
                place,
                parking, 
                service, 
                adresse_livraison,
                heure_livraison
                )

            if resultat_stationnement:
                parking.enregistrer_voiture(client, voiture)
                self.memoriser_entree(voiture)
                return self.borne.delivrer_ticket(voiture, place)
            
            return "Erreur lors du stationnement"
    
    def lancer_procedure_sortie(self, ticket, parking):

        
        resultat = self.retrouver_voiture_ticket(ticket, parking)
        placement_sortie = None
        if isinstance(resultat, Voiture):
            placement_sortie = next((p for p in reversed(resultat.placements) if p.estEnCours), None)

        if isinstance(resultat, Voiture) and resultat.priseEnChargeGarantie:
          
          recup = self.teleporteur2.rapporter_voiture_garantie(resultat)

          if not recup:
              return "Voiture impossible a rapporter"
           
          retire = parking.retirer_voiture_garantie(resultat)

          if not retire:
              return "Erreur"
          if placement_sortie is not None:
              placement_sortie.accesSortie = self.numero
          return resultat  
        
        if isinstance(resultat, str):
            return resultat
        
        recup = self.teleporteur2.rapporter_voiture(resultat)

        if not isinstance(recup, Voiture):
            return False

        if placement_sortie is not None:
            placement_sortie.accesSortie = self.numero
        return recup


       
