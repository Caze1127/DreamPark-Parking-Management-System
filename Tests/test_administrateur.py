import unittest
from unittest.mock import MagicMock, patch

from Class.administrateur import Administrateur
from Class.parking import Parking
from Class.place import Place
from Controleur.controleur_principal import ControleurPrincipal


class TestAdministrateur(unittest.TestCase):

    def setUp(self):
        self.parking = Parking([Place(1, 0, 2.5, 5.0)])
        self.administrateur = Administrateur("Responsable")

    def test_nom(self):
        self.assertEqual(self.administrateur.nom, "Responsable")

    def test_statistiques_parking_vide(self):
        resume = self.administrateur.consulter_statistiques(self.parking)
        self.assertEqual(resume["Total passage"], 0)
        self.assertEqual(resume["Total des passages en cours"], 0)

    def test_statistiques_sans_modifier_historique(self):
        self.administrateur.consulter_statistiques(self.parking)
        self.assertEqual(self.parking.placements, [])


class TestInterfaceAdministrateur(unittest.TestCase):

    def setUp(self):
        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.ctrl.parking = Parking([Place(1, 0, 2.5, 5.0)])
        self.ctrl.vue = MagicMock()
        self.ctrl.vue_identification = MagicMock()
        self.ctrl.vue_message = MagicMock()
        self.ctrl.client_identifie = MagicMock()

    @patch("Controleur.controleur_principal.VueAdministrateur")
    def test_ouvrir_espace(self, vue_classe):
        self.ctrl.ouvrir_espace_administrateur()
        vue_classe.assert_called_once_with(self.ctrl.vue.fenetre)
        self.assertIsNone(self.ctrl.client_identifie)
        self.ctrl.vue_identification.fenetre.destroy.assert_called_once()

    @patch("Controleur.controleur_principal.VueAdministrateur")
    def test_bouton_statistiques(self, vue_classe):
        self.ctrl.ouvrir_espace_administrateur()
        self.ctrl.vue_administrateur.bouton_statistiques.config.assert_called_once_with(
            command=self.ctrl.ouvrir_statistiques
        )

    @patch("Controleur.controleur_principal.VueAdministrateur")
    def test_bouton_retour(self, vue_classe):
        self.ctrl.ouvrir_espace_administrateur()
        self.ctrl.vue_administrateur.bouton_retour.config.assert_called_once_with(
            command=self.ctrl.fermer_espace_administrateur
        )

    @patch("Controleur.controleur_principal.VueAdministrateur")
    def test_fermeture_fenetre(self, vue_classe):
        self.ctrl.ouvrir_espace_administrateur()
        self.ctrl.vue_administrateur.fenetre.protocol.assert_called_once_with(
            "WM_DELETE_WINDOW", self.ctrl.fermer_espace_administrateur
        )

    def test_retour_identification(self):
        self.ctrl.vue_administrateur = MagicMock()
        self.ctrl.ouvrir_identification = MagicMock()
        self.ctrl.fermer_espace_administrateur()
        self.ctrl.vue_administrateur.fenetre.destroy.assert_called_once()
        self.ctrl.ouvrir_identification.assert_called_once()

    def test_stats_depuis_modele_administrateur(self):
        self.ctrl.vue_statistiques = MagicMock()
        resume = self.ctrl.actualiser_statistiques()
        self.assertEqual(resume["Total passage"], 0)
        self.ctrl.vue_statistiques.afficher_statistiques.assert_called_once_with(resume)


if __name__ == "__main__":
    unittest.main(verbosity=2)
