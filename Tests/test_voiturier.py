
import unittest

from Class.parking import Parking
from Class.place import Place
from Class.teleporteur import Teleporteur
from Class.voiture import Voiture
from Class.voiturier import Voiturier


class TestVoiturier(unittest.TestCase):

    def setUp(self):
        self.parking = Parking([Place(1, 0, 2.5, 5.0)])
        self.voiture = Voiture(1.8, 4.0, "AA-123-BB")
        self.parking.registre_voitures[self.voiture.immatriculation] = self.voiture
        self.voiturier = Voiturier("Alex")
        self.teleporteur = Teleporteur()

    def stationner(self, service="livraison", adresse="10 rue de Paris", heure="15:00"):
        return self.teleporteur.teleporter_voiture(
            self.voiture, self.parking.places[0], self.parking,
            service, adresse, heure
        )

    def test_livraison_valide(self):
        self.stationner()
        self.assertTrue(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))
        self.assertTrue(self.parking.places[0].estLibre)
        self.assertFalse(self.voiture.placements[-1].estEnCours)

    def test_immatriculation_normalisee(self):
        self.stationner()
        self.assertTrue(self.voiturier.effectuer_livraison(" aa-123-bb ", self.parking))

    def test_voiture_inconnue(self):
        self.assertFalse(self.voiturier.effectuer_livraison("XX-999-XX", self.parking))

    def test_sans_livraison(self):
        self.stationner(service="aucun")
        self.assertFalse(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))
        self.assertFalse(self.parking.places[0].estLibre)

    def test_heure_manquante(self):
        self.stationner(heure=None)
        self.assertFalse(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))

    def test_adresse_manquante(self):
        self.stationner(adresse=None)
        self.assertFalse(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))

    def test_deuxieme_livraison_refusee(self):
        self.stationner()
        self.assertTrue(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))
        self.assertFalse(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))

    def test_livraison_garantie(self):
        self.teleporteur.teleporter_voiture_super_abonne(
            self.voiture, self.parking, "livraison", "10 rue de Paris", "15:00"
        )
        self.parking.ajouter_voiture_garantie(self.voiture)

        self.assertTrue(self.voiturier.effectuer_livraison("AA-123-BB", self.parking))
        self.assertFalse(self.voiture.priseEnChargeGarantie)
        self.assertEqual(self.parking.voituresGaranties, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
