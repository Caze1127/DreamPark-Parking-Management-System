class Voiture:
    @staticmethod
    def normaliser_immatriculation(immatriculation):
        return immatriculation.strip().upper()

    def __init__(self,hauteur,longueur,immatriculation):
        self.hauteur = hauteur
        self.longueur = longueur
        self.immatriculation = self.normaliser_immatriculation(immatriculation)
        self.place = None
        self.estDansParking = False
        self.placements = []
        self.priseEnChargeGarantie = False
        self.serviceGaranti = "aucun"
        self.serviceEnCours = "aucun"
        self.retourServiceGaranti = False
        


    def sortir_du_parking(self):
        if not self.estDansParking:
            return False

        placement = self.place.placement

        if placement is None:
            return False

        return placement.partirPlace()

    def ajout_placement(self, placement):
        self.placements.append(placement)