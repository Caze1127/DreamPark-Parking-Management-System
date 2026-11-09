import unittest

from Class.place import Place
from Class.voiture import Voiture
from Class.placement import Placement
from Class.parking import Parking


class TestPlace(unittest.TestCase):

    def test_place_est_libre_a_la_creation(self):
        place = Place(1, 1, 5, 2)

        self.assertTrue(place.estLibre)

    def test_place_sans_voiture_a_la_creation(self):
        place = Place(1, 1, 5, 2)

        self.assertIsNone(place.voiture)

    def test_ajout_placement(self):
        place = Place(1, 1, 7, 2)
        parking = Parking([place])
        voiture = Voiture(2, 6, "AB-434-AZ")

        placement = Placement(
            voiture,
            place,
            parking
        )

        resultat = place.ajout_placement(placement)

        self.assertTrue(resultat)
        self.assertFalse(place.estLibre)
        self.assertIs(place.voiture, voiture)
        self.assertIs(place.placement, placement)

    def test_ajout_placement_sur_place_occupee(self):
        place = Place(1, 1, 7, 2)
        parking = Parking([place])

        voiture1 = Voiture(2, 6, "AB-434-AZ")
        voiture2 = Voiture(2, 6, "DG-534-AZ")

        placement1 = Placement(
            voiture1,
            place,
            parking
        )

        placement2 = Placement(
            voiture2,
            place,
            parking
        )

        place.ajout_placement(placement1)
        resultat = place.ajout_placement(placement2)

        self.assertFalse(resultat)
        self.assertFalse(place.estLibre)
        self.assertIs(place.voiture, voiture1)
        self.assertIs(place.placement, placement1)

    def test_liberer_place(self):
        place = Place(1, 1, 7, 2)
        parking = Parking([place])
        voiture = Voiture(2, 6, "AB-434-AZ")

        placement = Placement(
            voiture,
            place,
            parking
        )

        place.ajout_placement(placement)

        resultat = place.liberer_place()

        self.assertTrue(resultat)
        self.assertTrue(place.estLibre)
        self.assertIsNone(place.voiture)
        self.assertIsNone(place.placement)


if __name__ == "__main__":
    unittest.main()
