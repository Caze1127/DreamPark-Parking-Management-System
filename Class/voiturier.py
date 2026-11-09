
from .acces import Acces
from .voiture import Voiture


class Voiturier:
    def __init__(self, nom):
        self.nom = nom

    def effectuer_livraison(self, immatriculation, parking):
        immatriculation = Voiture.normaliser_immatriculation(immatriculation)
        voiture = parking.rechercher_voiture(immatriculation)

        if voiture is None:
            return False

        placement = next(
            (p for p in reversed(voiture.placements) if p.estEnCours),
            None
        )

        if placement is None or placement.parking is not parking:
            return False

        if placement.service != "livraison":
            return False

        if not placement.adresseLivraison or not placement.heureLivraison:
            return False

        return Acces().lancer_livraison(voiture)
