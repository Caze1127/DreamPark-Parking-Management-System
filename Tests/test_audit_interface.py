import unittest
from unittest.mock import MagicMock, patch

from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Controleur.controleur_principal import ControleurPrincipal


class TestAuditInterface(unittest.TestCase):

    def setUp(self):
        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.ctrl.vue = MagicMock()
        self.ctrl.vue_message = MagicMock()
        self.ctrl.parking = Parking([Place(1, 0, 2.5, 5.0)])
        self.ctrl.client_identifie = Client("Test", "Paris")
        self.ctrl.client_identifie.sAbonner()

    @patch("Controleur.controleur_principal.VueService")
    def test_changement_service_connecte_a_l_heure(self, vue_service):
        self.ctrl.ouvrir_gestion_service()
        self.ctrl.vue_service.choix_service.trace_add.assert_called_once_with(
            "write", self.ctrl.actualiser_heure_service
        )

    def test_heure_visible_pour_livraison(self):
        self.ctrl.vue_service = MagicMock()
        self.ctrl.vue_service.choix_service.get.return_value = "livraison"
        self.ctrl.actualiser_heure_service()
        self.ctrl.vue_service.afficher_heure.assert_called_once()
        self.ctrl.vue_service.masquer_heure.assert_not_called()

    def test_heure_cachee_pour_entretien(self):
        self.ctrl.vue_service = MagicMock()
        self.ctrl.vue_service.choix_service.get.return_value = "entretien"
        self.ctrl.actualiser_heure_service()
        self.ctrl.vue_service.masquer_heure.assert_called_once()
        self.ctrl.vue_service.afficher_heure.assert_not_called()

    def test_fermeture_statistiques_reactive_admin(self):
        self.ctrl.vue_statistiques = MagicMock()
        self.ctrl.vue_administrateur = MagicMock()
        self.ctrl.vue_administrateur.fenetre.winfo_exists.return_value = True
        self.ctrl.fermer_statistiques()
        self.ctrl.vue_statistiques.fenetre.destroy.assert_called_once()
        self.ctrl.vue_administrateur.fenetre.grab_set.assert_called_once()

    def test_fermeture_statistiques_sans_admin(self):
        self.ctrl.vue_statistiques = MagicMock()
        self.ctrl.fermer_statistiques()
        self.ctrl.vue_statistiques.fenetre.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
