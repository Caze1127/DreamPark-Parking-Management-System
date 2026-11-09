import unittest

from Class.acces import Acces
from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Class.voiture import Voiture


class TestReferenceTicket(unittest.TestCase):

    def setUp(self):

        self.parking = Parking([
            Place(1, 0, 2.5, 5.0),
            Place(2, 0, 2.5, 5.0)
        ])

        self.client = Client("Yoyo", "Paris")
        self.client.sAbonner()

        self.voiture = Voiture(1.8, 4.0, "AA-123-BB")
        self.acces = Acces()

        self.ticket = self.acces.lancer_procedure_entree(
            self.client,
            self.voiture,
            self.parking
        )

        self.reference = self.ticket.split(" - N° ")[-1]

    def test_reference_six_caracteres(self):

        self.assertEqual(len(self.reference), 6)
        self.assertRegex(self.reference, r"^[0-9A-F]{6}$")

    def test_ticket_complet_conserve(self):

        self.assertTrue(
            self.ticket.startswith("Ticket - AA-123-BB - Place 1 - N° ")
        )

        self.assertTrue(self.ticket.endswith(self.reference))

    def test_sortie_reference_valide(self):

        resultat = self.acces.lancer_procedure_sortie(
            self.reference,
            self.parking
        )

        self.assertIs(resultat, self.voiture)
        self.assertTrue(self.parking.places[0].estLibre)

    def test_reference_minuscules(self):

        resultat = self.acces.lancer_procedure_sortie(
            self.reference.lower(),
            self.parking
        )

        self.assertIs(resultat, self.voiture)

    def test_reference_avec_espaces(self):

        resultat = self.acces.lancer_procedure_sortie(
            f"  {self.reference}  ",
            self.parking
        )

        self.assertIs(resultat, self.voiture)

    def test_reference_incomplete(self):

        resultat = self.acces.lancer_procedure_sortie(
            self.reference[:3],
            self.parking
        )

        self.assertEqual(resultat, "Ticket invalide")
        self.assertFalse(self.parking.places[0].estLibre)

    def test_reference_invalide(self):

        resultat = self.acces.lancer_procedure_sortie(
            "ZZZZZZ",
            self.parking
        )

        self.assertEqual(resultat, "Ticket invalide")

    def test_reference_inexistante(self):

        reference = "FFFFFF"

        if reference == self.reference:
            reference = "EEEEEE"

        resultat = self.acces.lancer_procedure_sortie(
            reference,
            self.parking
        )

        self.assertEqual(resultat, "Ticket invalide ou expiré")

    def test_reference_expiree(self):

        self.acces.lancer_procedure_sortie(
            self.reference,
            self.parking
        )

        resultat = self.acces.lancer_procedure_sortie(
            self.reference,
            self.parking
        )

        self.assertEqual(resultat, "Ticket invalide ou expiré")

    def test_nouvelle_reference_apres_reentree(self):

        self.acces.lancer_procedure_sortie(
            self.reference,
            self.parking
        )

        nouveau_ticket = self.acces.lancer_procedure_entree(
            self.client,
            self.voiture,
            self.parking
        )

        nouvelle_reference = nouveau_ticket.split(" - N° ")[-1]

        self.assertNotEqual(self.reference, nouvelle_reference)

        self.assertEqual(
            self.acces.lancer_procedure_sortie(
                self.reference,
                self.parking
            ),
            "Ticket invalide ou expiré"
        )

        self.assertIs(
            self.acces.lancer_procedure_sortie(
                nouvelle_reference,
                self.parking
            ),
            self.voiture
        )

    def test_sortie_pack_garanti(self):

        parking = Parking([])
        client = Client("Super", "Paris")
        client.superSAbonner()

        voiture = Voiture(1.8, 4.0, "GG-123-AA")

        ticket = self.acces.lancer_procedure_entree(
            client,
            voiture,
            parking
        )

        reference = ticket.split(" - N° ")[-1]

        self.assertIn("Garantie", ticket)

        resultat = self.acces.lancer_procedure_sortie(
            reference,
            parking
        )

        self.assertIs(resultat, voiture)
        self.assertEqual(parking.voituresGaranties, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
