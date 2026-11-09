import unittest
from datetime import datetime, timedelta

from Class.place import Place
from Class.voiture import Voiture
from Class.parking import Parking
from Class.placement import Placement
from Class.statistique import Statistique


class TestStatistiques(unittest.TestCase):

    def setUp(self):

        self.place1 = Place(1, 0, 2.0, 5.0)
        self.place2 = Place(2, 0, 2.0, 5.0)
        self.place3 = Place(3, 1, 2.0, 5.0)

        self.parking = Parking([
            self.place1,
            self.place2,
            self.place3
        ])

        self.voiture1 = Voiture(1.5, 4.0, "AA-111-AA")
        self.voiture2 = Voiture(1.6, 4.2, "BB-222-BB")
        self.voiture3 = Voiture(1.7, 4.3, "CC-333-CC")

        self.placement1 = Placement(
            self.voiture1,
            self.place1,
            self.parking,
            "maintenance"
        )

        self.placement1.dateDebut = datetime(2026, 10, 20, 8, 0)
        self.placement1.dateFin = datetime(2026, 10, 20, 10, 0)
        self.placement1.estEnCours = False

        self.placement2 = Placement(
            self.voiture1,
            self.place2,
            self.parking,
            "aucun"
        )

        self.placement2.dateDebut = datetime(2026, 10, 20, 11, 0)
        self.placement2.dateFin = datetime(2026, 10, 20, 12, 0)
        self.placement2.estEnCours = False

        self.placement3 = Placement(
            self.voiture2,
            self.place3,
            self.parking,
            "livraison"
        )

        self.placement3.dateDebut = datetime(2026, 10, 20, 13, 0)
        self.placement3.dateFin = datetime(2026, 10, 20, 16, 0)
        self.placement3.estEnCours = False

        self.placement4 = Placement(
            self.voiture2,
            self.place3,
            self.parking,
            "livraison"
        )

        self.placement4.dateDebut = datetime(2026, 10, 20, 17, 0)
        self.placement4.dateFin = None
        self.placement4.estEnCours = True

        self.placement5 = Placement(
            self.voiture3,
            self.place1,
            self.parking,
            "entretien"
        )

        self.placement5.dateDebut = datetime(2026, 10, 20, 18, 0)
        self.placement5.dateFin = datetime(2026, 10, 20, 20, 0)
        self.placement5.estEnCours = False

        self.parking.placements = [
            self.placement1,
            self.placement2,
            self.placement3,
            self.placement4,
            self.placement5
        ]

        self.stats = Statistique(self.parking)

    def test_nombre_total_passages(self):
        self.assertEqual(
            self.stats.nombre_total_passages(),
            5
        )

    def test_nombre_passages_voiture(self):
        self.assertEqual(
            self.stats.nombre_passages_voiture(self.voiture1),
            2
        )

        self.assertEqual(
            self.stats.nombre_passages_voiture(self.voiture3),
            1
        )

    def test_voitures_plus_frequentes(self):

        resultat = self.stats.voitures_plus_frequentes()

        self.assertEqual(len(resultat), 2)
        self.assertIn(self.voiture1, resultat)
        self.assertIn(self.voiture2, resultat)

    def test_nombre_passages_service(self):

        self.assertEqual(
            self.stats.nombre_passages_service("livraison"),
            2
        )

        self.assertEqual(
            self.stats.nombre_passages_service("maintenance"),
            1
        )

        self.assertEqual(
            self.stats.nombre_passages_service("entretien"),
            1
        )

        self.assertEqual(
            self.stats.nombre_passages_service("aucun"),
            1
        )

    def test_activite_service(self):

        resultat = self.stats.activite_service()

        self.assertEqual(
            resultat,
            {
                "maintenance": 1,
                "entretien": 1,
                "livraison": 2,
                "aucun": 1
            }
        )

    def test_services_plus_utilises(self):

        resultat = self.stats.services_plus_utilises()

        self.assertEqual(
            resultat,
            ["livraison"]
        )

    def test_nombre_passages_termines(self):

        self.assertEqual(
            self.stats.nombre_passages_termines(),
            4
        )

    def test_nombre_passages_en_cours(self):

        self.assertEqual(
            self.stats.nombre_passages_en_cours(),
            1
        )

    def test_duree_moyenne_stationnement(self):

        resultat = self.stats.duree_moyenne_stationnement()


        self.assertEqual(
            resultat,
            timedelta(hours=2)
        )

    def test_nombre_voitures_distinctes(self):

        self.assertEqual(
            self.stats.nombre_voitures_distinctes(),
            3
        )

    def test_nombre_moyen_passage_voiture_distinctes(self):

        resultat = (
            self.stats.nombre_moyen_passage_voiture_distinctes()
        )

        self.assertAlmostEqual(
            resultat,
            5 / 3
        )

    def test_nombre_passages_niveau(self):


        self.assertEqual(
            self.stats.nombre_passages_niveau(0),
            3
        )


        self.assertEqual(
            self.stats.nombre_passages_niveau(1),
            2
        )

    def test_frequentation_niveaux(self):

        resultat = self.stats.frequentation_niveaux()

        self.assertEqual(
            resultat,
            {
                0: 3,
                1: 2
            }
        )

    def test_niveaux_plus_frequentes(self):

        resultat = self.stats.niveaux_plus_frequentes()

        self.assertEqual(
            resultat,
            [0]
        )

    def test_nombre_passages_place(self):

        self.assertEqual(
            self.stats.nombre_passages_place(self.place1),
            2
        )

        self.assertEqual(
            self.stats.nombre_passages_place(self.place2),
            1
        )

        self.assertEqual(
            self.stats.nombre_passages_place(self.place3),
            2
        )

    def test_frequentation_places(self):

        resultat = self.stats.frequentation_places()

        self.assertEqual(
            resultat,
            {
                1: 2,
                2: 1,
                3: 2
            }
        )

    def test_place_plus_frequentes(self):

        resultat = self.stats.place_plus_frequentes()

        self.assertEqual(len(resultat), 2)
        self.assertIn(1, resultat)
        self.assertIn(3, resultat)

    def test_voitures_regulieres(self):


        resultat = self.stats.voitures_regulieres(2)

        self.assertEqual(len(resultat), 2)
        self.assertIn(self.voiture1, resultat)
        self.assertIn(self.voiture2, resultat)

    def test_stationnement_max(self):


        self.assertEqual(
            self.stats.stationnement_max(),
            timedelta(hours=3)
        )

    def test_immatriculations_voitures(self):

        resultat = self.stats.immatriculations_voitures([
            self.voiture1,
            self.voiture2
        ])

        self.assertEqual(
            resultat,
            [
                "AA-111-AA",
                "BB-222-BB"
            ]
        )

    def test_formater_duree(self):

        duree = timedelta(
            hours=2,
            minutes=15,
            seconds=30
        )

        self.assertEqual(
            self.stats.formater_duree(duree),
            "2 h 15 min 30 s"
        )

    def test_resume_statistiques(self):

        resultat = self.stats.resume_statistiques()

        self.assertEqual(
            resultat["Total passage"],
            5
        )

        self.assertEqual(
            resultat["Total des passages terminés"],
            4
        )

        self.assertEqual(
            resultat["Total des passages en cours"],
            1
        )

        self.assertEqual(
            resultat["Durée moyenne de stationnement"],
            "2 h 0 min 0 s"
        )

        self.assertEqual(
            resultat["Durée de stationnement maximum"],
            "3 h 0 min 0 s"
        )


if __name__ == "__main__":
    unittest.main()