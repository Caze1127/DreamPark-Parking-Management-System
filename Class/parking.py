from .voiture import Voiture

class Parking:
    def __init__(self,places):
        self.places = places
        self.abonnements = []
        self.voituresGaranties = []
        self.placements = []
        self.registre_voitures = {}
        self.responsables_voitures = {}

    def rechercher_voiture(self, immatriculation):
        identifiant = Voiture.normaliser_immatriculation(immatriculation)
        return self.registre_voitures.get(identifiant)

    def enregistrer_voiture(self, client, voiture):
        identifiant = Voiture.normaliser_immatriculation(voiture.immatriculation)
        precedente = self.registre_voitures.get(identifiant)
        if precedente is not None and precedente is not voiture:
            return False

        ancien_client = self.responsables_voitures.get(identifiant)
        if ancien_client is not None and ancien_client is not client:
            if voiture in ancien_client.voitures:
                ancien_client.voitures.remove(voiture)

        self.registre_voitures[identifiant] = voiture
        self.responsables_voitures[identifiant] = client
        if voiture not in client.voitures:
            client.voitures.append(voiture)
        return True


    def ajouter_placement(self, placement):
        self.placements.append(placement)
        
    
    def rechercher_place(self, voiture):
        
        for place in self.places:
            
            if place.estLibre and place.longueur >= voiture.longueur and place.hauteur >= voiture.hauteur:
                return place
        
        return None

    def nombre_places_libres(self):
        
        compteur = 0

        for place in self.places:
            
            if place.estLibre:
                compteur += 1
        
        return compteur

    def nombre_places_libres_par_niveau(self, niveau):
        
        compteur = 0

        for place in self.places:
            
            if place.estLibre and place.niveau == niveau :
                compteur += 1
        
        return compteur

    def ajouter_abonnement(self, abonnement):
        
        self.abonnements.append(abonnement)

    def rechercher_place_numero(self, numero):
        
        for place in self.places:
            
            if place.numero == numero:
                return place
        
        return None

    def ajouter_voiture_garantie(self, voiture):
        self.voituresGaranties.append(voiture)

    def rechercher_voiture_garantie(self, immatriculation):
        
        immatriculation = Voiture.normaliser_immatriculation(immatriculation)
        for voiture in self.voituresGaranties:
            
            if immatriculation == voiture.immatriculation: 
                return voiture
            
        return None

    def retirer_voiture_garantie(self, voiture):
        
        if voiture in self.voituresGaranties:
            
            self.voituresGaranties.remove(voiture)
            return True
        
        return False