import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from Class.client import Client
from Class.place import Place
from Class.parking import Parking
from Class.voiture import Voiture
from Class.acces import Acces
from Controleur.controleur_principal import ControleurPrincipal


class TestInterfaceStatistiques(unittest.TestCase):

    def setUp(self):

        self.ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        self.ctrl.parking = Parking([Place(1, 0, 2.5, 6.0)])
        self.ctrl.vue = MagicMock()
        self.ctrl.vue_statistiques = MagicMock()
        self.ctrl.vue_message = MagicMock()

    def test_actualiser_statistiques_vide(self):

        resume = self.ctrl.actualiser_statistiques()

        self.assertEqual(resume["Total passage"], 0)
        self.assertEqual(resume["Total des passages en cours"], 0)
        self.ctrl.vue_statistiques.afficher_statistiques.assert_called_once_with(resume)

    def test_actualiser_statistiques_apres_entree(self):

        client = Client("Test", "Toulouse")
        client.sAbonner()
        voiture = Voiture(1.7, 4.5, "AA-123-BB")
        Acces().lancer_procedure_entree(client, voiture, self.ctrl.parking)

        resume = self.ctrl.actualiser_statistiques()

        self.assertEqual(resume["Total passage"], 1)
        self.assertEqual(resume["Total des passages en cours"], 1)

    @patch("Controleur.controleur_principal.VueStatistiques")
    def test_ouvrir_statistiques_configure_boutons(self, vue_classe):

        self.ctrl.ouvrir_statistiques()

        vue_classe.assert_called_once_with(self.ctrl.vue.fenetre)
        self.ctrl.vue_statistiques.bouton_actualiser.config.assert_called_once_with(
            command=self.ctrl.actualiser_statistiques
        )
        self.ctrl.vue_statistiques.bouton_exporter_texte.config.assert_called_once_with(
            command=self.ctrl.exporter_statistiques_texte
        )
        self.ctrl.vue_statistiques.bouton_exporter_html.config.assert_called_once_with(
            command=self.ctrl.exporter_statistiques_html
        )
        self.ctrl.vue_statistiques.bouton_fermer.config.assert_called_once_with(
            command=self.ctrl.fermer_statistiques
        )
        self.ctrl.vue_statistiques.afficher_statistiques.assert_called_once()

    @patch("Controleur.controleur_principal.filedialog.asksaveasfilename")
    def test_exporter_statistiques_texte(self, dialogue):

        with TemporaryDirectory() as repertoire:

            fichier = Path(repertoire) / "statistiques.txt"
            dialogue.return_value = str(fichier)
            self.ctrl.exporter_statistiques_texte()

            self.assertTrue(fichier.is_file())
            self.assertIn("Total passage : 0", fichier.read_text(encoding="utf-8"))
            self.ctrl.vue_message.afficher_information.assert_called_once()

    @patch("Controleur.controleur_principal.filedialog.asksaveasfilename")
    def test_exporter_statistiques_html(self, dialogue):

        with TemporaryDirectory() as repertoire:

            fichier = Path(repertoire) / "statistiques.html"
            dialogue.return_value = str(fichier)
            self.ctrl.exporter_statistiques_html()

            self.assertTrue(fichier.is_file())
            self.assertIn("<html", fichier.read_text(encoding="utf-8"))
            self.assertIn("Total passage : 0", fichier.read_text(encoding="utf-8"))
            self.ctrl.vue_message.afficher_information.assert_called_once()

    @patch("Controleur.controleur_principal.filedialog.asksaveasfilename", return_value="")
    def test_annulation_export(self, dialogue):

        self.ctrl.exporter_statistiques_texte()

        self.ctrl.vue_message.afficher_information.assert_not_called()
        self.ctrl.vue_message.afficher_erreur.assert_not_called()
        self.ctrl.vue_statistiques.afficher_statistiques.assert_not_called()

    @patch("Controleur.controleur_principal.VueStatistiquesTexte.enregistrer", side_effect=OSError("Accès refusé"))
    @patch("Controleur.controleur_principal.filedialog.asksaveasfilename", return_value="statistiques.txt")
    def test_erreur_enregistrement(self, dialogue, enregistrer):

        self.ctrl.exporter_statistiques_texte()

        self.ctrl.vue_message.afficher_erreur.assert_called_once()
        self.ctrl.vue_message.afficher_information.assert_not_called()

    def test_fermer_statistiques(self):

        self.ctrl.fermer_statistiques()

        self.ctrl.vue_statistiques.fenetre.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
