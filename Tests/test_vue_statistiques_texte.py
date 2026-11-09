import unittest
import os

from Class.vue_statistiques_texte import VueStatistiquesTexte


class TestVueStatistiquesTexte(unittest.TestCase):

    def setUp(self):

        self.vue = VueStatistiquesTexte()

        self.resume = {
            "Total passage": 5,
            "Total des passages terminés": 4,
            "Total des passages en cours": 1,
            "Durée moyenne de stationnement": "2 h 0 min 0 s"
        }

    def test_generer(self):

        resultat = self.vue.generer(self.resume)

        self.assertIn(
            "===== STATISTIQUES DREAM PARK =====",
            resultat
        )

        self.assertIn(
            "Total passage : 5",
            resultat
        )

        self.assertIn(
            "Total des passages terminés : 4",
            resultat
        )

        self.assertIn(
            "Durée moyenne de stationnement : 2 h 0 min 0 s",
            resultat
        )

    def test_enregistrer(self):

        nom_fichier = "statistiques_test.txt"

        resultat = self.vue.enregistrer(
            self.resume,
            nom_fichier
        )

        self.assertTrue(resultat)
        self.assertTrue(os.path.exists(nom_fichier))

        with open(nom_fichier, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()

        self.assertIn(
            "Total passage : 5",
            contenu
        )

        os.remove(nom_fichier)


if __name__ == "__main__":
    unittest.main()