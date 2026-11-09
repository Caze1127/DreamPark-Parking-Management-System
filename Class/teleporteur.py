from .placement import Placement
from .place import Place

class Teleporteur:

    def teleporter_voiture_super_abonne(
            self, 
            voiture, 
            parking,
            service = "aucun",
            adresse_livraison = None, 
            heure_livraison = None
            ):

        placement = Placement(voiture, None, parking, service)
                
        placement.adresseLivraison = adresse_livraison
        placement.heureLivraison = heure_livraison 

        voiture.ajout_placement(placement)
        parking.ajouter_placement(placement)
        voiture.serviceGaranti = service
        voiture.priseEnChargeGarantie = True
        
        return "Véhicule du super-abonné pris en charge"

    def teleporter_voiture(
            self, 
            voiture, 
            place,
            parking,
            service = "aucun", 
            adresse_livraison = None, 
            heure_livraison = None
            ):
        
        placement = Placement(voiture, place, parking, service)
        
        placement.adresseLivraison = adresse_livraison
        placement.heureLivraison = heure_livraison

        if place.ajout_placement(placement):
            
            voiture.ajout_placement(placement)
            parking.ajouter_placement(placement)
            voiture.estDansParking = True
            voiture.place = place
            
            return placement
        
        return False

    def rapporter_voiture(self,voiture):
        
        if not voiture.estDansParking:
            return False

        resultat = voiture.sortir_du_parking()

        if resultat:
            return voiture

        return False 
            
    def rapporter_voiture_garantie(self, voiture):
        
        if not voiture.priseEnChargeGarantie :
            return False

        for placement in voiture.placements:
            
            if placement.estEnCours and placement.place is None:
                
                placement.partirPlace()
                voiture.priseEnChargeGarantie = False
                voiture.serviceGaranti = "aucun"    
                
                return voiture 
            
        return False

    def envoyer_en_service(self, voiture):
        placement = next((p for p in reversed(voiture.placements) if p.estEnCours), None)
        if placement is None or placement.service not in ("maintenance", "entretien"):
            return False

        parking = placement.parking
        responsable = parking.responsables_voitures.get(voiture.immatriculation)
        voiture.retourServiceGaranti = (
            voiture.priseEnChargeGarantie
            or (responsable is not None and responsable.estSuperAbonne)
        )

        if voiture.priseEnChargeGarantie:
            if placement.place is not None:
                return False
            if not parking.retirer_voiture_garantie(voiture):
                return False
            voiture.priseEnChargeGarantie = False
            voiture.serviceGaranti = "aucun"
        elif (not voiture.estDansParking or voiture.place is None
              or voiture.place.placement is not placement):
            return False

        voiture.serviceEnCours = placement.service
        placement.partirPlace()
        return True

    def retour_service(self, voiture):
        if voiture.serviceEnCours not in ("maintenance", "entretien"):
            return False
        if not voiture.placements:
            return False

        parking = voiture.placements[-1].parking
        place_libre = parking.rechercher_place(voiture)
        if place_libre is not None:
            resultat = self.teleporter_voiture(voiture, place_libre, parking)
            if resultat is False:
                return False
        elif voiture.retourServiceGaranti:
            self.teleporter_voiture_super_abonne(voiture, parking)
            parking.ajouter_voiture_garantie(voiture)
        else:
            return False

        voiture.serviceEnCours = "aucun"
        voiture.retourServiceGaranti = False
        return True

    def livrer_voiture(self, voiture):

        if not voiture.estDansParking or voiture.place is None:
            return False

        if voiture.place is None:
            return False

        placement = voiture.place.placement

        if placement is None:
            return False

        service = placement.service
        adresse = placement.adresseLivraison
        heure = placement.heureLivraison
        if (
            service == "livraison" 
            and adresse is not None 
            and heure is not None
            ):
         
            resultat = placement.partirPlace()
            if resultat :
                return True 
        return False

    def livrer_voiture_garantie(self, voiture):
        
        if not voiture.priseEnChargeGarantie:
            return False 
            
        for placement in voiture.placements:
                    
            if placement.estEnCours and placement.place is None:


                service = placement.service
                adresse = placement.adresseLivraison
                heure = placement.heureLivraison
                garantie = placement.parking.rechercher_voiture_garantie(voiture.immatriculation)

                if (
                    service == "livraison" 
                    and adresse is not None 
                    and heure is not None
                    and garantie is not None
                    ):

                    resultat = placement.partirPlace()

                    if resultat:

                        placement.parking.retirer_voiture_garantie(voiture)
                        voiture.priseEnChargeGarantie = False
                        voiture.serviceGaranti = "aucun"
                        
                        return True

        return False



                

