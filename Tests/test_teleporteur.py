import unittest

from Class.place import Place
from Class.voiture import Voiture
from Class.teleporteur import Teleporteur
from Class.placement import Placement
from Class.parking import Parking


class TestTeleporteur(unittest.TestCase):

    def test_teleporter_voiture(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(1.8, 4, "AA-123-BB")
        teleporteur = Teleporteur()

        resultat = teleporteur.teleporter_voiture(
            voiture,
            place,
            parking
        )

        self.assertIsInstance(resultat, Placement)
        self.assertTrue(voiture.estDansParking)
        self.assertIs(voiture.place, place)
        self.assertFalse(place.estLibre)
        self.assertIn(resultat, voiture.placements)
        self.assertIs(place.placement, resultat)
        self.assertIs(place.voiture, voiture)
        self.assertIs(resultat.parking, parking)

    def test_envoyer_en_maintenance(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "MA-111-AA"
        )

        teleporteur = Teleporteur()

        placement = teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="maintenance"
        )

        resultat = teleporteur.envoyer_en_service(
            voiture
        )

        self.assertTrue(resultat)

        self.assertEqual(
            voiture.serviceEnCours,
            "maintenance"
        )

        self.assertFalse(
            voiture.estDansParking
        )

        self.assertIsNone(
            voiture.place
        )

        self.assertTrue(
            place.estLibre
        )

        self.assertIsNone(
            place.voiture
        )

        self.assertIsNone(
            place.placement
        )

        self.assertFalse(
            placement.estEnCours
        )

        self.assertIsNotNone(
            placement.dateFin
        )

        self.assertIs(
            placement.parking,
            parking
        )

    def test_envoyer_en_entretien(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "EN-111-AA"
        )

        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="entretien"
        )

        resultat = teleporteur.envoyer_en_service(
            voiture
        )

        self.assertTrue(resultat)

        self.assertEqual(
            voiture.serviceEnCours,
            "entretien"
        )

        self.assertFalse(
            voiture.estDansParking
        )

        self.assertIsNone(
            voiture.place
        )

        self.assertTrue(
            place.estLibre
        )

    def test_envoyer_en_service_aucun(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "NO-111-AA"
        )

        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="aucun"
        )

        resultat = teleporteur.envoyer_en_service(
            voiture
        )

        self.assertFalse(resultat)

        self.assertEqual(
            voiture.serviceEnCours,
            "aucun"
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertIs(
            voiture.place,
            place
        )

        self.assertFalse(
            place.estLibre
        )

    def test_retour_service_maintenance(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "MA-222-AA"
        )

        teleporteur = Teleporteur()

        ancien_placement = teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="maintenance"
        )

        resultat_depart = teleporteur.envoyer_en_service(
            voiture
        )

        self.assertTrue(resultat_depart)

        resultat_retour = teleporteur.retour_service(
            voiture
        )

        self.assertTrue(resultat_retour)

        self.assertEqual(
            voiture.serviceEnCours,
            "aucun"
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertIsNotNone(
            voiture.place
        )

        self.assertFalse(
            voiture.place.estLibre
        )

        self.assertEqual(
            len(voiture.placements),
            2
        )

        nouveau_placement = voiture.placements[-1]

        self.assertIsNot(
            nouveau_placement,
            ancien_placement
        )

        self.assertTrue(
            nouveau_placement.estEnCours
        )

        self.assertIs(
            nouveau_placement.parking,
            parking
        )

        self.assertFalse(
            ancien_placement.estEnCours
        )

    def test_retour_service_entretien(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "EN-222-AA"
        )

        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="entretien"
        )

        teleporteur.envoyer_en_service(
            voiture
        )

        resultat = teleporteur.retour_service(
            voiture
        )

        self.assertTrue(resultat)

        self.assertEqual(
            voiture.serviceEnCours,
            "aucun"
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertIsNotNone(
            voiture.place
        )

        self.assertFalse(
            voiture.place.estLibre
        )

    def test_retour_service_sans_service(self):
        voiture = Voiture(
            1.8,
            4,
            "NO-222-AA"
        )

        teleporteur = Teleporteur()

        resultat = teleporteur.retour_service(
            voiture
        )

        self.assertFalse(resultat)

    def test_livrer_voiture(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "LI-444-AA"
            )

        teleporteur = Teleporteur()

        placement = teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="livraison",
            adresse_livraison="12 rue Victor Hugo",
            heure_livraison="18:30"
            )

        resultat = teleporteur.livrer_voiture(
            voiture
            )

        self.assertTrue(resultat)

        self.assertFalse(
            voiture.estDansParking
            )

        self.assertIsNone(
            voiture.place
            )

        self.assertTrue(
            place.estLibre
            )

        self.assertIsNone(
            place.voiture
            )

        self.assertFalse(
            placement.estEnCours
            )

        self.assertIsNotNone(
            placement.dateFin
            )

        self.assertEqual(
            placement.adresseLivraison,
            "12 rue Victor Hugo"
            )

        self.assertEqual(
            placement.heureLivraison,
            "18:30"
            )

    def test_livrer_voiture_sans_service_livraison(self):
        place = Place(1, 1, 5, 7)
        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "NO-444-AA"
            )

        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture,
            place,
            parking,
            service="aucun"
            )

        resultat = teleporteur.livrer_voiture(
            voiture
            )

        self.assertFalse(resultat)

        self.assertTrue(
            voiture.estDansParking
            )

        self.assertIs(
            voiture.place,
            place
            )

        self.assertFalse(
            place.estLibre
            )

    def test_livrer_voiture_non_garee(self):
        voiture = Voiture(
            1.8,
            4,
            "LI-555-AA"
            )

        teleporteur = Teleporteur()

        resultat = teleporteur.livrer_voiture(
            voiture
            )

        self.assertFalse(resultat)

if __name__ == "__main__":
    unittest.main()