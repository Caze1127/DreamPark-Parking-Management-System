import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Class.sauvegarde import Sauvegarde
from Controleur.controleur_principal import ControleurPrincipal


class TestCorrectionsIntegration(unittest.TestCase):

    def setUp(self):
        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.ctrl.vue = MagicMock()
        self.ctrl.vue_message = MagicMock()
        self.ctrl.parking = Parking([Place(1, 0, 2.5, 5.0)])
        self.ctrl.clients = []
        self.ctrl.client_identifie = None
        self.ctrl.mode_identification = None

    @patch("Controleur.controleur_principal.VueIdentification")
    def test_bouton_voiturier_connecte(self, classe_vue):
        self.ctrl.ouvrir_identification()
        self.ctrl.vue_identification.bouton_voiturier.config.assert_called_once_with(
            command=self.ctrl.ouvrir_espace_voiturier
        )
        self.ctrl.vue_identification.bouton_administrateur.config.assert_called_once_with(
            command=self.ctrl.ouvrir_espace_administrateur
        )

    @patch("Controleur.controleur_principal.VueService")
    def test_fenetre_service_sans_bouton_livraison_client(self, classe_vue):
        client = Client("Exemple", "Paris")
        client.sAbonner()
        self.ctrl.client_identifie = client
        self.ctrl.ouvrir_gestion_service()
        self.ctrl.vue_service.bouton_valider.config.assert_called_once()
        self.ctrl.vue_service.bouton_lancer_livraison.config.assert_not_called()

    @patch("Controleur.controleur_principal.VueIdentification")
    def test_nouveau_client_enregistre_en_json(self, classe_vue):
        with TemporaryDirectory() as dossier:
            self.ctrl.sauvegarde = Sauvegarde(Path(dossier) / "dreampark.json")
            self.ctrl.ouvrir_identification()
            self.ctrl.mode_identification = "nouveau"
            self.ctrl.vue_identification.champ_nom.get.return_value = "Nouveau"
            self.ctrl.vue_identification.champ_adresse.get.return_value = "Lyon"
            self.ctrl.valider_identification()
            self.assertEqual(len(self.ctrl.clients), 1)
            self.assertIs(self.ctrl.client_identifie, self.ctrl.clients[0])
            nouveau_parking = Parking([])
            clients = self.ctrl.sauvegarde.charger(nouveau_parking)
            self.assertEqual(len(clients), 1)
            self.assertEqual(clients[0].nom, "Nouveau")

    def test_fermeture_sauvegarde(self):
        self.ctrl.sauvegarder_donnees = MagicMock(return_value=True)
        self.ctrl.fermer_application()
        self.ctrl.sauvegarder_donnees.assert_called_once()
        self.ctrl.vue.fenetre.destroy.assert_called_once()

    def test_fermeture_refusee_si_echec_sauvegarde(self):
        self.ctrl.sauvegarder_donnees = MagicMock(return_value=False)
        self.ctrl.fermer_application()
        self.ctrl.vue.fenetre.destroy.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
