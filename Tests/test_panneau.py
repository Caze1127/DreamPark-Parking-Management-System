import unittest

from Class.panneau_affichage import PanneauAffichage
from Class.teleporteur import Teleporteur
from Class.voiture import Voiture
from Class.place import Place
from Class.acces import Acces
from Class.parking import Parking


class TestPanneau(unittest.TestCase):

    def test_panneau_affichage(self):
        place1 = Place(1, 1, 5, 2)
        place2 = Place(2, 1, 4, 2)

        parking = Parking([place1, place2])
        acces = Acces()

        resultat = acces.actionnerPanneau(parking)

        self.assertEqual(resultat, "Places disponibles : 2")

    def test_panneau_apres_stationnement(self):
        place1 = Place(1, 1, 5, 6)
        place2 = Place(2, 1, 5, 6)

        parking = Parking([place1, place2])

        voiture = Voiture(1.8, 4, "AA-111-BB")
        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture,
            place1,
            parking
        )

        panneau = PanneauAffichage()
        resultat = panneau.afficherNbPlacesDisponibles(parking)

        self.assertEqual(resultat, "Places disponibles : 1")


if __name__ == "__main__":
    unittest.main()
