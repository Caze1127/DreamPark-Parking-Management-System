from .voiture import Voiture
class Client:
    def __init__(self, nom, adresse):
        self.nom = nom
        self.adresse = adresse
        self.numeroCarte = None 
        self.estAbonne = False
        self.estSuperAbonne = False
        self.nbFrequentations = 0
        self.voitures = []

    def nouvelleVoiture(self, hauteur, longueur, immatriculation):

        voiture = self.rechercherVoiture(immatriculation)

        if voiture is not None:
            return voiture

        voiture = Voiture(hauteur, longueur, immatriculation)
        self.voitures.append(voiture)

        return voiture

    def sAbonner(self):
        
        self.estAbonne = True
        return True

    def seDesabonner(self):
        
        self.estAbonne = False
        self.estSuperAbonne = False
        
        return True

    def superSAbonner(self):
        
        self.estAbonne = True
        self.estSuperAbonne = True
        
        return True

    def SuperSeDesabonner(self):
        
        self.estSuperAbonne = False
        return True

    def rechercherVoiture(self, immatriculation):

        immatriculation = Voiture.normaliser_immatriculation(immatriculation)
        voitures_trouvees = [
            voiture
            for voiture in self.voitures
            if voiture.immatriculation == immatriculation
        ]

        for voiture in reversed(voitures_trouvees):
            for placement in voiture.placements:
                if placement.estEnCours:
                    return voiture

        for voiture in reversed(voitures_trouvees):
            if voiture.serviceEnCours in ["maintenance", "entretien"]:
                return voiture

        if voitures_trouvees:
            return voitures_trouvees[-1]

        return None

    def entrerParking(
            self,
            acces,
            voiture,
            parking,
            choix_service = None,
            mode_paiement = None,
            choix_abonnement = None,
            heure_livraison = None
            ):

        return acces.lancer_procedure_entree(
            self,
            voiture,
            parking,
            choix_service,
            mode_paiement,
            choix_abonnement,
            heure_livraison 
            )




