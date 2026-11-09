import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from Class.acces import Acces
from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Class.placement import Placement
from Class.voiture import Voiture
from Controleur.controleur_principal import ControleurPrincipal


class TestNumeroCarte(unittest.TestCase):
    def setUp(self):
        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.ctrl.clients = []
        self.client = Client("Alice", "Paris")
        self.client.sAbonner()

    def test_format_carte(self):
        self.assertEqual(self.ctrl.formater_numero_carte(48273169), "4827 3169")

    def test_carte_aleatoire_8_chiffres(self):
        self.ctrl.attribuer_carte(self.client)
        self.assertIsInstance(self.client.numeroCarte, int)
        self.assertTrue(10_000_000 <= self.client.numeroCarte <= 99_999_999)
        numero = self.client.numeroCarte
        self.ctrl.attribuer_carte(self.client)
        self.assertEqual(self.client.numeroCarte, numero)

    def test_carte_differente_si_collision(self):
        autre = Client("Bob", "Lyon")
        autre.numeroCarte = 10_000_123
        self.ctrl.clients = [autre]
        with patch("Controleur.controleur_principal.randbelow", side_effect=[123, 123, 456]):
            self.ctrl.attribuer_carte(self.client)
        self.assertEqual(self.client.numeroCarte, 10_000_456)
        self.assertNotEqual(self.client.numeroCarte, autre.numeroCarte)

    def test_identification_accepte_numero_avec_espaces(self):
        self.client.numeroCarte = 48273169
        self.ctrl.clients = [self.client]
        self.ctrl.client_identifie = None
        self.ctrl.mode_identification = "carte"
        self.ctrl.vue_identification = MagicMock()
        self.ctrl.vue_message = MagicMock()
        self.ctrl.vue_identification.champ_numero_carte.get.return_value = "4827 3169"
        self.ctrl.valider_identification()
        self.assertIs(self.ctrl.client_identifie, self.client)
        self.ctrl.vue_identification.fenetre.destroy.assert_called_once()


class TestTicketLisible(unittest.TestCase):
    def setUp(self):
        self.parking = Parking([Place(1, 0, 2.5, 5.0)])
        self.client = Client("Alice", "Paris")
        self.client.sAbonner()
        self.voiture = Voiture(1.7, 4, "AA-123-BB")
        self.acces = Acces()

    def test_ticket_code_court_et_valide(self):
        ticket = self.acces.lancer_procedure_entree(self.client, self.voiture, self.parking)
        code = self.acces.borne.lire_ticket(ticket)[2]
        self.assertRegex(code, r"^[0-9A-F]{6}$")
        self.assertEqual(len(self.voiture.placements[-1].referenceTicket), 32)
        self.assertIn("N° " + code, ticket)
        self.assertIs(self.acces.lancer_procedure_sortie(ticket.split(" - N° ")[-1], self.parking), self.voiture)

    def test_ticket_ancien_perime_apres_reentree(self):
        t1 = self.acces.lancer_procedure_entree(self.client, self.voiture, self.parking)
        self.acces.lancer_procedure_sortie(t1.split(" - N° ")[-1], self.parking)
        t2 = self.acces.lancer_procedure_entree(self.client, self.voiture, self.parking)
        self.assertNotEqual(t1, t2)
        self.assertEqual(self.acces.lancer_procedure_sortie(t1.split(" - N° ")[-1], self.parking), "Ticket invalide ou expiré")
        self.assertIs(self.acces.lancer_procedure_sortie(t2.split(" - N° ")[-1], self.parking), self.voiture)

    def test_collision_code_visible_regenere(self):
        p1 = Placement(self.voiture, self.parking.places[0], self.parking)
        self.parking.ajouter_placement(p1)
        prefixe = p1.referenceTicket[:6]
        with patch("Class.placement.uuid4", side_effect=[
            SimpleNamespace(hex=prefixe + "a" * 26),
            SimpleNamespace(hex="f" * 32 if prefixe != "ffffff" else "e" * 32),
        ]):
            p2 = Placement(self.voiture, None, self.parking)
        self.assertNotEqual(p1.reference_courte, p2.reference_courte)


if __name__ == "__main__":
    unittest.main()
