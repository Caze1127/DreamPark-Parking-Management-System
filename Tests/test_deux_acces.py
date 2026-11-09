import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from Class.acces import Acces
from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Class.sauvegarde import Sauvegarde
from Class.voiture import Voiture


class TestDeuxAcces(unittest.TestCase):

    def setUp(self):
        self.parking = Parking([Place(1, 0, 2.5, 5.0), Place(2, 0, 2.5, 5.0)])
        self.client = Client("Alice", "Paris")
        self.client.sAbonner()
        self.voiture = Voiture(1.8, 4.0, "AA-123-BB")
        self.acces1 = Acces(1)
        self.acces2 = Acces(2)

    def test_equipements_distincts(self):
        self.assertIsNot(self.acces1.camera, self.acces2.camera)
        self.assertIsNot(self.acces1.borne, self.acces2.borne)
        self.assertIsNot(self.acces1.teleporteur1, self.acces2.teleporteur1)
        self.assertIsNot(self.acces1.teleporteur2, self.acces2.teleporteur2)

    def test_numero_acces_invalide(self):
        with self.assertRaises(ValueError):
            Acces(3)

    def test_entree_acces_1_sortie_acces_2(self):
        ticket = self.acces1.lancer_procedure_entree(self.client, self.voiture, self.parking)
        placement = self.voiture.placements[-1]
        self.assertEqual(placement.accesEntree, 1)
        self.assertIsNone(placement.accesSortie)
        reference = ticket.split(" - N° ")[-1]
        self.assertIs(self.acces2.lancer_procedure_sortie(reference, self.parking), self.voiture)
        self.assertEqual(placement.accesSortie, 2)
        self.assertEqual(self.parking.nombre_places_libres(), 2)

    def test_entree_acces_2_sortie_acces_1(self):
        ticket = self.acces2.lancer_procedure_entree(self.client, self.voiture, self.parking)
        placement = self.voiture.placements[-1]
        self.assertEqual(placement.accesEntree, 2)
        self.assertIs(self.acces1.lancer_procedure_sortie(ticket.split(" - N° ")[-1], self.parking), self.voiture)
        self.assertEqual(placement.accesSortie, 1)

    def test_places_partagees(self):
        self.assertEqual(self.acces1.actionnerPanneau(self.parking), self.acces2.actionnerPanneau(self.parking))
        self.acces2.lancer_procedure_entree(self.client, self.voiture, self.parking)
        self.assertEqual(self.acces1.actionnerPanneau(self.parking), "Places disponibles : 1")
        self.assertEqual(self.acces2.actionnerPanneau(self.parking), "Places disponibles : 1")

    def test_sauvegarde_conserve_les_acces(self):
        ticket = self.acces2.lancer_procedure_entree(self.client, self.voiture, self.parking)
        self.acces1.lancer_procedure_sortie(ticket.split(" - N° ")[-1], self.parking)
        with TemporaryDirectory() as dossier:
            sauvegarde = Sauvegarde(Path(dossier) / "donnees.json")
            sauvegarde.enregistrer(self.parking, [self.client])
            autre_parking = Parking([])
            sauvegarde.charger(autre_parking)
        self.assertEqual(autre_parking.placements[0].accesEntree, 2)
        self.assertEqual(autre_parking.placements[0].accesSortie, 1)

    def test_ancienne_sauvegarde_compatible(self):
        self.acces1.lancer_procedure_entree(self.client, self.voiture, self.parking)
        with TemporaryDirectory() as dossier:
            chemin = Path(dossier) / "donnees.json"
            sauvegarde = Sauvegarde(chemin)
            sauvegarde.enregistrer(self.parking, [self.client])
            donnees = json.loads(chemin.read_text(encoding="utf-8"))
            for placement in donnees["placements"]:
                placement.pop("accesEntree", None)
                placement.pop("accesSortie", None)
            chemin.write_text(json.dumps(donnees), encoding="utf-8")
            autre_parking = Parking([])
            sauvegarde.charger(autre_parking)
        self.assertIsNone(autre_parking.placements[0].accesEntree)
        self.assertIsNone(autre_parking.placements[0].accesSortie)


if __name__ == "__main__":
    unittest.main(verbosity=2)
