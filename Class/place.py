class Place:
    def __init__(self,numero,niveau,hauteur,longueur):
        self.numero = numero
        self.niveau = niveau
        self.longueur = longueur
        self.hauteur = hauteur
        self.estLibre = True
        self.voiture = None
        self.placement = None

    def liberer_place(self):
        if not self.estLibre:
            self.voiture = None
            self.estLibre = True
            self.placement = None
            return True
        else:
            return False

    def ajout_placement(self, placement):
        if self.estLibre:
            self.placement = placement
            self.voiture = placement.voiture
            self.estLibre = False
            return True
        else:
            return False