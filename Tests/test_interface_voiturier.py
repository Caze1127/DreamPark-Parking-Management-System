import unittest
from unittest.mock import MagicMock, patch

from Class.parking import Parking
from Class.place import Place
from Class.voiture import Voiture
from Class.teleporteur import Teleporteur
from Controleur.controleur_principal import ControleurPrincipal


class TestInterfaceVoiturier(unittest.TestCase):

    def setUp(self):
        self.parking = Parking([Place(1, 0, 2.5, 5.0), Place(2, 0, 2.5, 5.0)])
        self.voiture = Voiture(1.8, 4.0, "AA-123-BB")
        self.parking.registre_voitures[self.voiture.immatriculation] = self.voiture
        self.teleporteur = Teleporteur()

        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.ctrl.parking = self.parking
        self.ctrl.vue = MagicMock()
        self.ctrl.vue_identification = MagicMock()
        self.ctrl.vue_voiturier = MagicMock()
        self.ctrl.vue_message = MagicMock()
        self.ctrl.client_identifie = MagicMock()
        self.ctrl.actualiser_places = MagicMock()
        self.ctrl.sauvegarder_donnees = MagicMock(return_value=True)
        self.ctrl.ouvrir_identification = MagicMock()

    def ajouter_livraison(self, adresse="10 rue de Paris", heure="15:00", service="livraison"):
        placement = self.teleporteur.teleporter_voiture(
            self.voiture, self.parking.places[0], self.parking,
            service, adresse, heure
        )
        return placement

    def test_liste_vide(self):
        self.ctrl.actualiser_livraisons_voiturier()
        self.ctrl.vue_voiturier.afficher_livraisons.assert_called_once_with([])

    def test_livraison_en_attente_affichee(self):
        self.ajouter_livraison()
        self.ctrl.actualiser_livraisons_voiturier()
        self.ctrl.vue_voiturier.afficher_livraisons.assert_called_once_with([
            ("AA-123-BB", "10 rue de Paris", "15:00")
        ])

    def test_service_autre_que_livraison_non_affiche(self):
        self.ajouter_livraison(service="entretien")
        self.ctrl.actualiser_livraisons_voiturier()
        self.ctrl.vue_voiturier.afficher_livraisons.assert_called_once_with([])

    def test_livraison_incomplete_non_affichee(self):
        self.ajouter_livraison(heure=None)
        self.ctrl.actualiser_livraisons_voiturier()
        self.ctrl.vue_voiturier.afficher_livraisons.assert_called_once_with([])

    def test_livraison_terminee_non_affichee(self):
        placement = self.ajouter_livraison()
        placement.partirPlace()
        self.ctrl.actualiser_livraisons_voiturier()
        self.ctrl.vue_voiturier.afficher_livraisons.assert_called_once_with([])

    def test_sans_selection_affiche_erreur(self):
        self.ctrl.vue_voiturier.immatriculation_selectionnee.return_value = None
        self.ctrl.effectuer_livraison_voiturier()
        self.ctrl.vue_message.afficher_erreur.assert_called_once_with(
            "Veuillez sélectionner une livraison"
        )
        self.ctrl.sauvegarder_donnees.assert_not_called()

    @patch("Controleur.controleur_principal.messagebox.askyesno", return_value=False)
    def test_confirmation_refusee(self, confirmation):
        self.ajouter_livraison()
        self.ctrl.vue_voiturier.immatriculation_selectionnee.return_value = "AA-123-BB"
        self.ctrl.effectuer_livraison_voiturier()
        self.assertFalse(self.parking.places[0].estLibre)
        self.ctrl.sauvegarder_donnees.assert_not_called()
        self.ctrl.vue_message.afficher_information.assert_not_called()

    @patch("Controleur.controleur_principal.messagebox.askyesno", return_value=True)
    def test_livraison_validee_et_sauvegardee(self, confirmation):
        placement = self.ajouter_livraison()
        self.ctrl.vue_voiturier.immatriculation_selectionnee.return_value = "AA-123-BB"
        self.ctrl.effectuer_livraison_voiturier()
        self.assertFalse(placement.estEnCours)
        self.assertTrue(self.parking.places[0].estLibre)
        self.ctrl.actualiser_places.assert_called_once()
        self.ctrl.sauvegarder_donnees.assert_called_once()
        self.ctrl.vue_voiturier.afficher_livraisons.assert_called_once_with([])
        self.ctrl.vue_message.afficher_information.assert_called_once()

    @patch("Controleur.controleur_principal.messagebox.askyesno", return_value=True)
    def test_livraison_introuvable_refusee(self, confirmation):
        self.ctrl.vue_voiturier.immatriculation_selectionnee.return_value = "ZZ-999-ZZ"
        self.ctrl.effectuer_livraison_voiturier()
        self.ctrl.vue_message.afficher_erreur.assert_called_once_with(
            "Impossible d'effectuer cette livraison"
        )
        self.ctrl.sauvegarder_donnees.assert_not_called()

    def test_fermeture_retour_identification(self):
        self.ctrl.fermer_espace_voiturier()
        self.ctrl.vue_voiturier.fenetre.destroy.assert_called_once()
        self.ctrl.ouvrir_identification.assert_called_once()

    @patch("Controleur.controleur_principal.VueVoiturier")
    def test_ouverture_espace_voiturier(self, vue_voiturier):
        fenetre = vue_voiturier.return_value.fenetre
        self.ctrl.ouvrir_espace_voiturier()
        self.ctrl.vue_identification.fenetre.destroy.assert_called_once()
        self.assertIsNone(self.ctrl.client_identifie)
        vue_voiturier.assert_called_once_with(self.ctrl.vue.fenetre)
        fenetre.grab_set.assert_called_once()
        self.assertTrue(vue_voiturier.return_value.bouton_actualiser.config.called)
        self.assertTrue(vue_voiturier.return_value.bouton_livrer.config.called)
        self.assertTrue(vue_voiturier.return_value.bouton_retour.config.called)
        vue_voiturier.return_value.afficher_livraisons.assert_called_once_with([])


if __name__ == "__main__":
    unittest.main(verbosity=2)
