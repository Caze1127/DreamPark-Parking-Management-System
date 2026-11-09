import unittest

from Class.place import Place
from Class.voiture import Voiture
from Class.teleporteur import Teleporteur
from Class.parking import Parking


class TestPlacement(unittest.TestCase):

    def test_sortir_du_parking(self):
        place = Place(1, 1, 5, 2)
        parking = Parking([place])
        voiture = Voiture(1.8, 4, "AA-123-BB")
        teleporteur = Teleporteur()

        placement = teleporteur.teleporter_voiture(
            voiture,
            place,
            parking
        )

        self.assertIs(placement, place.placement)
        self.assertTrue(placement.estEnCours)
        self.assertIs(placement.parking, parking)

        resultat = voiture.sortir_du_parking()

        self.assertTrue(resultat)
        self.assertFalse(voiture.estDansParking)
        self.assertIsNone(voiture.place)

        self.assertTrue(place.estLibre)
        self.assertIsNone(place.voiture)
        self.assertIsNone(place.placement)

        self.assertFalse(placement.estEnCours)
        self.assertIsNotNone(placement.dateFin)


if __name__ == "__main__":
    unittest.main()
