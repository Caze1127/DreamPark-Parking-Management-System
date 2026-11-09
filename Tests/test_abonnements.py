import unittest
from unittest.mock import MagicMock

from Class.abonnement import Abonnement
from Class.acces import Acces
from Class.client import Client
from Class.parking import Parking
from Controleur.controleur_principal import ControleurPrincipal


class TestClientAbonnements(unittest.TestCase):
    def setUp(self):
        self.client = Client("Test", "Paris")
        self.client.numeroCarte = 1001

    def test_abonnement_classique(self):
        self.client.sAbonner()
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)

    def test_super_abonnement(self):
        self.client.superSAbonner()
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)

    def test_montee_en_gamme(self):
        self.client.sAbonner()
        self.client.superSAbonner()
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)

    def test_retrogradation(self):
        self.client.superSAbonner()
        self.client.SuperSeDesabonner()
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)

    def test_resiliation_classique(self):
        self.client.sAbonner()
        self.client.seDesabonner()
        self.assertFalse(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)

    def test_resiliation_super(self):
        self.client.superSAbonner()
        self.client.seDesabonner()
        self.assertFalse(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)

    def test_reabonnement_apres_resiliation(self):
        self.client.superSAbonner()
        self.client.seDesabonner()
        self.client.sAbonner()
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)


class TestSouscriptionParAcces(unittest.TestCase):
    def setUp(self):
        self.client = Client("Test", "Paris")
        self.parking = Parking([])
        self.parking.ajouter_abonnement(Abonnement("Abonné classique", 50, False))
        self.parking.ajouter_abonnement(Abonnement("Super-abonné", 100, True))
        self.acces = Acces()

    def test_souscription_classique(self):
        resultat = self.acces.gerer_abonnement(
            self.client, self.parking, "CB", "Abonné classique"
        )
        self.assertIsNone(resultat)
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)

    def test_souscription_super(self):
        resultat = self.acces.gerer_abonnement(
            self.client, self.parking, "Espece", "Super-abonné"
        )
        self.assertIsNone(resultat)
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)

    def test_mode_paiement_invalide(self):
        resultat = self.acces.gerer_abonnement(
            self.client, self.parking, "inconnu", "Abonné classique"
        )
        self.assertEqual(resultat, "Erreur veuillez choisir votre mode de paiement")
        self.assertFalse(self.client.estAbonne)

    def test_abonnement_invalide(self):
        resultat = self.acces.gerer_abonnement(
            self.client, self.parking, "CB", "Formule inconnue"
        )
        self.assertEqual(resultat, "Erreur : abonnement invalide")
        self.assertFalse(self.client.estAbonne)


class TestControleurAbonnements(unittest.TestCase):
    def setUp(self):
        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.client = Client("Test", "Paris")
        self.client.numeroCarte = 1001
        self.ctrl.client_identifie = self.client
        self.ctrl.clients = [self.client]
        self.ctrl.vue_message = MagicMock()
        self.ctrl.vue_gestion_abonnement = MagicMock()
        self.ctrl.vue_desabonnement = MagicMock()
        self.ctrl.terminer_session = MagicMock()
        self.ctrl.sauvegarder_donnees = MagicMock(return_value=True)
        self.ctrl.vue_gestion_abonnement.choix_abonnement.get.return_value = "Super-abonné"
        self.ctrl.vue_gestion_abonnement.mode_paiement.get.return_value = "CB"
        self.ctrl.vue_desabonnement.choix_desabonnement.get.return_value = "Choisir une option"
        self.ctrl.parking = Parking([])
        self.ctrl.parking.ajouter_abonnement(Abonnement("Abonné classique", 50, False))
        self.ctrl.parking.ajouter_abonnement(Abonnement("Super-abonné", 100, True))

    def test_souscription_attribue_carte(self):
        self.client.numeroCarte = None
        self.ctrl.clients.clear()
        self.ctrl.vue_gestion_abonnement.choix_abonnement.get.return_value = "Abonné classique"
        self.ctrl.valider_souscription()
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertIsInstance(self.client.numeroCarte, int)
        self.assertGreaterEqual(self.client.numeroCarte, 10_000_000)
        self.assertLessEqual(self.client.numeroCarte, 99_999_999)
        self.assertIn(self.client, self.ctrl.clients)
        self.ctrl.terminer_session.assert_called_once()

    def test_souscription_super(self):
        self.ctrl.valider_souscription()
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)
        self.assertEqual(len(self.ctrl.clients), 1)

    def test_souscription_sans_paiement(self):
        self.ctrl.vue_gestion_abonnement.mode_paiement.get.return_value = "Choisir un paiement"
        self.ctrl.valider_souscription()
        self.assertFalse(self.client.estAbonne)
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_souscription_refusee_si_deja_abonne(self):
        self.client.sAbonner()
        self.ctrl.valider_souscription()
        self.assertFalse(self.client.estSuperAbonne)
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_modification_classique_vers_super(self):
        self.client.sAbonner()
        self.ctrl.valider_modification_abonnement()
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)
        self.ctrl.vue_message.afficher_information.assert_called_once()
        self.ctrl.vue_gestion_abonnement.fenetre.destroy.assert_called_once()
        self.ctrl.terminer_session.assert_called_once()

    def test_modification_impossible_si_deja_super(self):
        self.client.superSAbonner()
        self.ctrl.valider_modification_abonnement()
        self.assertTrue(self.client.estSuperAbonne)
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_modification_refusee_vers_classique(self):
        self.client.sAbonner()
        self.ctrl.vue_gestion_abonnement.choix_abonnement.get.return_value = "Abonné classique"
        self.ctrl.valider_modification_abonnement()
        self.assertFalse(self.client.estSuperAbonne)
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_modification_sans_paiement(self):
        self.client.sAbonner()
        self.ctrl.vue_gestion_abonnement.mode_paiement.get.return_value = "Choisir un paiement"
        self.ctrl.valider_modification_abonnement()
        self.assertFalse(self.client.estSuperAbonne)
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_resiliation_classique(self):
        self.client.sAbonner()
        self.ctrl.valider_desabonnement()
        self.assertFalse(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)
        self.assertIn(self.client, self.ctrl.clients)
        self.ctrl.vue_message.afficher_information.assert_called_once()
        self.ctrl.vue_desabonnement.fenetre.destroy.assert_called_once()
        self.ctrl.vue_gestion_abonnement.fenetre.destroy.assert_called_once()
        self.ctrl.terminer_session.assert_called_once()

    def test_retrogradation_super_vers_classique(self):
        self.client.superSAbonner()
        self.ctrl.vue_desabonnement.choix_desabonnement.get.return_value = "Devenir abonné classique"
        self.ctrl.valider_desabonnement()
        self.assertTrue(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)
        self.ctrl.terminer_session.assert_called_once()

    def test_resiliation_complete_super(self):
        self.client.superSAbonner()
        self.ctrl.vue_desabonnement.choix_desabonnement.get.return_value = "Résilier complètement"
        self.ctrl.valider_desabonnement()
        self.assertFalse(self.client.estAbonne)
        self.assertFalse(self.client.estSuperAbonne)
        self.assertEqual(self.client.numeroCarte, 1001)
        self.ctrl.terminer_session.assert_called_once()

    def test_super_sans_choix(self):
        self.client.superSAbonner()
        self.ctrl.valider_desabonnement()
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.vue_desabonnement.fenetre.destroy.assert_not_called()
        self.ctrl.terminer_session.assert_not_called()

    def test_resiliation_refusee_si_non_abonne(self):
        self.ctrl.valider_desabonnement()
        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_annulation_ne_change_rien(self):
        self.client.superSAbonner()
        self.ctrl.annuler_desabonnement()
        self.assertTrue(self.client.estAbonne)
        self.assertTrue(self.client.estSuperAbonne)
        self.ctrl.vue_desabonnement.fenetre.destroy.assert_called_once()
        self.ctrl.vue_gestion_abonnement.fenetre.grab_set.assert_called_once()
        self.ctrl.terminer_session.assert_not_called()

    def test_carte_retrouvee_apres_resiliation(self):
        self.client.superSAbonner()
        self.client.seDesabonner()
        retrouve = self.ctrl.rechercher_client(1001)
        self.assertIs(retrouve, self.client)
        self.assertFalse(retrouve.estAbonne)


if __name__ == "__main__":
    unittest.main(verbosity = 2)
