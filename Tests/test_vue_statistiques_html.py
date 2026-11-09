
import unittest
import os

from Class.vue_statistiques_html import VueStatistiquesHTML


class TestVueStatistiquesHTML(unittest.TestCase):

    def setUp(self):

        self.vue = VueStatistiquesHTML()

        self.resume = {
            "Total passage": 5,
            "Total des passages terminés": 4,
            "Total des passages en cours": 1,
            "Durée moyenne de stationnement": "2 h 0 min 0 s"
        }

    def test_generer(self):

        resultat = self.vue.generer(self.resume)

        self.assertIn("<html", resultat)
        self.assertIn("<h1>", resultat)
        self.assertIn("STATISTIQUES DREAM PARK", resultat)

        self.assertIn(
            "<p>Total passage : 5</p>",
            resultat
        )

        self.assertIn(
            "<p>Total des passages terminés : 4</p>",
            resultat
        )

        self.assertIn(
            "</body>",
            resultat
        )

        self.assertIn(
            "</html>",
            resultat
        )

    def test_enregistrer(self):

        nom_fichier = "statistiques_test.html"

        resultat = self.vue.enregistrer(
            self.resume,
            nom_fichier
        )

        self.assertTrue(resultat)
        self.assertTrue(os.path.exists(nom_fichier))

        with open(
            nom_fichier,
            "r",
            encoding="utf-8"
        ) as fichier:
            contenu = fichier.read()

        self.assertIn(
            "STATISTIQUES DREAM PARK",
            contenu
        )

        self.assertIn(
            "<p>Total passage : 5</p>",
            contenu
        )

        os.remove(nom_fichier)


if __name__ == "__main__":
    unittest.main()