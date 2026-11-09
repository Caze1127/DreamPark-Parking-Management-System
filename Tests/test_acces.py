import unittest

from Class.teleporteur import Teleporteur
from Class.acces import Acces
from Class.client import Client
from Class.abonnement import Abonnement
from Class.place import Place
from Class.parking import Parking
from Class.voiture import Voiture


class TestAcces(unittest.TestCase):

    def test_voiture_invalide(self):
        voiture = Voiture(0, 4.5, "AB-123-CD")
        client = Client("Yoyo", "Toulouse")
        parking = Parking([])
        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking
        )

        self.assertEqual(
            resultat,
            "Informations du véhicule invalides"
        )

    def test_parking_plein(self):
        place1 = Place(1, 1, 4, 2)
        place2 = Place(2, 1, 4, 2.5)

        parking = Parking([
            place1,
            place2
        ])

        voiture1 = Voiture(2, 3, "AZER")
        voiture2 = Voiture(2, 3, "DFGS")

        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture1,
            place1,
            parking
        )

        teleporteur.teleporter_voiture(
            voiture2,
            place2,
            parking
        )

        voiture3 = Voiture(2, 3, "SFGG")

        client = Client(
            "yoyo",
            "Toulouse"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture3,
            parking
        )

        self.assertEqual(
            resultat,
            "Le parking est plein"
        )

    def test_pas_place_inadapatee(self):
        place1 = Place(1, 1, 4, 2)

        voiture1 = Voiture(
            3,
            3,
            "AZER"
        )

        parking = Parking([place1])

        resultat = parking.rechercher_place(
            voiture1
        )

        self.assertIsNone(resultat)

    def test_client_abonne_service_valide(self):
        place1 = Place(1, 1, 5, 6)

        parking = Parking([place1])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "AB-123-CD"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="aucun"
        )

        self.assertTrue(
            resultat.startswith("Ticket - AB-123-CD - Place 1 - N° ")
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertFalse(
            place1.estLibre
        )

    def test_client_non_abonne_sans_abonnement(self):
        place1 = Place(1, 1, 5, 7)

        parking = Parking([place1])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.8,
            4,
            "AB-456-CD"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="CB",
            choix_abonnement="Aucun"
        )

        self.assertTrue(
            resultat.startswith("Ticket - AB-456-CD - Place 1 - N° ")
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertFalse(
            place1.estLibre
        )

        self.assertFalse(
            client.estAbonne
        )

    def test_client_prend_abonnement_standard(self):
        place1 = Place(1, 1, 5, 6)

        parking = Parking([place1])

        abonnement_standard = Abonnement(
            "standard",
            20,
            False
        )

        parking.ajouter_abonnement(
            abonnement_standard
        )

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.8,
            4,
            "AA-111-BB"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="CB",
            choix_abonnement="standard"
        )

        self.assertTrue(
            resultat.startswith("Ticket - AA-111-BB - Place 1 - N° ")
        )

        self.assertTrue(
            client.estAbonne
        )

        self.assertFalse(
            client.estSuperAbonne
        )

        self.assertTrue(
            voiture.estDansParking
        )

    def test_client_prend_pack_garanti(self):
        place1 = Place(1, 1, 5, 4)

        parking = Parking([place1])

        abonnement_garanti = Abonnement(
            "garanti",
            40,
            True
        )

        parking.ajouter_abonnement(
            abonnement_garanti
        )

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.8,
            4,
            "CC-222-DD"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="CB",
            choix_abonnement="garanti"
        )

        self.assertTrue(
            resultat.startswith("Ticket - CC-222-DD - Place 1 - N° ")
        )

        self.assertTrue(
            client.estAbonne
        )

        self.assertTrue(
            client.estSuperAbonne
        )

        self.assertTrue(
            voiture.estDansParking
        )

    def test_super_abonne_parking_plein(self):
        place1 = Place(1, 1, 5, 2)

        parking = Parking([place1])

        voiture_occupee = Voiture(
            1.8,
            4,
            "XX-111-YY"
        )

        teleporteur = Teleporteur()

        teleporteur.teleporter_voiture(
            voiture_occupee,
            place1,
            parking
        )

        client = Client(
            "yoyo",
            "Toulouse"
        )

        client.estAbonne = True
        client.estSuperAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "SUPER-01"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking
        )

        self.assertTrue(
            resultat.startswith("Ticket - SUPER-01 - Garantie - N° ")
        )

    def test_client_abonne_service_invalide(self):
        place1 = Place(1, 1, 5, 6)

        parking = Parking([place1])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "EE-333-FF"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="lavage"
        )

        self.assertEqual(
            resultat,
            "Erreur veuillez faire un choix de service"
        )

        self.assertFalse(
            voiture.estDansParking
        )

    def test_mode_paiement_invalide(self):
        place1 = Place(1, 1, 5, 5)

        parking = Parking([place1])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.8,
            4,
            "GG-444-HH"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="cheque",
            choix_abonnement="Aucun"
        )

        self.assertEqual(
            resultat,
            "Erreur veuillez choisir votre mode de paiement"
        )

        self.assertFalse(
            voiture.estDansParking
        )

        self.assertTrue(
            place1.estLibre
        )

    def test_abonnement_invalide(self):
        place1 = Place(1, 1, 5, 5)

        parking = Parking([place1])

        abonnement_standard = Abonnement(
            "standard",
            20,
            False
        )

        parking.ajouter_abonnement(
            abonnement_standard
        )

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.8,
            4,
            "II-555-JJ"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="CB",
            choix_abonnement="premium"
        )

        self.assertEqual(
            resultat,
            "Erreur : abonnement invalide"
        )

        self.assertFalse(
            voiture.estDansParking
        )

        self.assertTrue(
            place1.estLibre
        )

    def test_refus_abonnement(self):
        place1 = Place(1, 1, 5, 6)

        parking = Parking([place1])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.8,
            4,
            "KK-666-LL"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="Espece",
            choix_abonnement="Aucun"
        )

        self.assertTrue(
            resultat.startswith("Ticket - KK-666-LL - Place 1 - N° ")
        )

        self.assertFalse(
            client.estAbonne
        )

        self.assertFalse(
            client.estSuperAbonne
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertFalse(
            place1.estLibre
        )

    def test_integration_se_garer(self):
        place1 = Place(1, 1, 5, 2)
        place2 = Place(2, 1, 4, 1.8)
        place3 = Place(3, 2, 6, 2.5)

        parking = Parking([
            place1,
            place2,
            place3
        ])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        voiture = Voiture(
            1.7,
            1.5,
            "MM-777-NN"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            mode_paiement="CB",
            choix_abonnement="Aucun"
        )

        self.assertIs(
            place1.voiture,
            voiture
        )

        self.assertIs(
            voiture.place,
            place1
        )

        self.assertTrue(
            resultat.startswith("Ticket - MM-777-NN - Place 1 - N° ")
        )

        self.assertTrue(
            voiture.estDansParking
        )

        self.assertFalse(
            place1.estLibre
        )

        self.assertEqual(
            parking.nombre_places_libres(),
            2
        )

    def test_reprendre_voiture(self):
        place = Place(1, 1, 5, 6)

        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "AA-111-BB"
        )

        acces = Acces()

        placement = acces.teleporteur1.teleporter_voiture(
            voiture,
            place,
            parking
        )

        ticket = acces.borne.delivrer_ticket(voiture, place)

        resultat = acces.lancer_procedure_sortie(
            ticket.split(" - N° ")[-1],
            parking
        )

        self.assertIs(
            resultat,
            voiture
        )

        self.assertFalse(
            voiture.estDansParking
        )

        self.assertIsNone(
            voiture.place
        )

        self.assertTrue(
            place.estLibre
        )

        self.assertIsNone(
            place.voiture
        )

        self.assertIsNone(
            place.placement
        )

        self.assertFalse(
            placement.estEnCours
        )

        self.assertIsNotNone(
            placement.dateFin
        )

        self.assertEqual(
            parking.nombre_places_libres(),
            1
        )

    def test_reference_inconnue_sans_place(self):
        place = Place(1, 1, 5, 6)

        parking = Parking([place])

        acces = Acces()

        ticket = "000000"

        resultat = acces.lancer_procedure_sortie(
            ticket.split(" - N° ")[-1],
            parking
        )

        self.assertEqual(
            resultat,
            "Ticket invalide ou expiré"
        )

    def test_reference_inconnue_place_libre(self):
        place = Place(1, 1, 5, 6)

        parking = Parking([place])

        acces = Acces()

        ticket = "000000"

        resultat = acces.lancer_procedure_sortie(
            ticket.split(" - N° ")[-1],
            parking
        )

        self.assertEqual(
            resultat,
            "Ticket invalide ou expiré"
        )

    def test_reference_inconnue_avec_voiture_garee(self):
        place = Place(1, 1, 5, 6)

        parking = Parking([place])

        voiture = Voiture(
            1.8,
            4,
            "ZZ-999-ZZ"
        )

        acces = Acces()

        acces.teleporteur1.teleporter_voiture(
            voiture,
            place,
            parking
        )

        ticket = "000000"

        resultat = acces.lancer_procedure_sortie(
            ticket.split(" - N° ")[-1],
            parking
        )

        self.assertEqual(
            resultat,
            "Ticket invalide ou expiré"
        )

    def test_ticket_invalide(self):
        parking = Parking([])

        acces = Acces()

        ticket = "bonjour"

        resultat = acces.lancer_procedure_sortie(
            ticket.split(" - N° ")[-1],
            parking
        )

        self.assertEqual(
            resultat,
            "Ticket invalide"
        )

    def test_service_livraison(self):
        place = Place(1, 1, 5, 6)

        parking = Parking([place])

        client = Client(
            "yoyo",
            "12 rue Victor Hugo"
        )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "LI-111-VR"
        )

        acces = Acces()

        ticket = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="livraison",
            heure_livraison="18:30"
        )

        self.assertTrue(
            ticket.startswith("Ticket - LI-111-VR - Place 1 - N° ")
        )

        self.assertEqual(
            place.placement.service,
            "livraison"
        )

        self.assertEqual(
            place.placement.adresseLivraison,
            "12 rue Victor Hugo"
        )

        self.assertEqual(
            place.placement.heureLivraison,
            "18:30"
        )

        self.assertIs(
            place.placement.parking,
            parking
        )

    def test_livraison_sans_heure(self):
        place = Place(1, 1, 5, 6)

        parking = Parking([place])

        client = Client(
            "yoyo",
            "12 rue Victor Hugo"
        )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "LI-222-VR"
        )

        acces = Acces()

        resultat = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="livraison"
        )

        self.assertEqual(
            resultat,
            "Erreur: Heure de livraison non fournie"
        )

        self.assertTrue(
            place.estLibre
        )

        self.assertFalse(
            voiture.estDansParking
        )

    def test_entree_sortie_voiture_garantie(self):
        place = Place(1, 1, 1.5, 3)

        parking = Parking([place])

        client = Client(
            "yoyo",
            "Toulouse"
        )

        client.superSAbonner()

        voiture = Voiture(
            1.8,
            4,
            "GG-111-GG"
        )

        acces = Acces()

        ticket = acces.lancer_procedure_entree(
            client,
            voiture,
            parking,
            choix_service="livraison",
            heure_livraison="18:30"
        )

        self.assertTrue(
            ticket.startswith("Ticket - GG-111-GG - Garantie - N° ")
        )

        self.assertTrue(
            voiture.priseEnChargeGarantie
        )

        self.assertEqual(
            voiture.serviceGaranti,
            "livraison"
        )

        self.assertIn(
            voiture,
            parking.voituresGaranties
        )

        placement = voiture.placements[-1]

        self.assertIsNone(
            placement.place
        )

        self.assertIs(
            placement.parking,
            parking
        )

        self.assertEqual(
            placement.service,
            "livraison"
        )

        resultat = acces.lancer_procedure_sortie(
            ticket.split(" - N° ")[-1],
            parking
        )

        self.assertIs(
            resultat,
            voiture
        )

        self.assertFalse(
            voiture.priseEnChargeGarantie
        )

        self.assertEqual(
            voiture.serviceGaranti,
            "aucun"
        )

        self.assertNotIn(
            voiture,
            parking.voituresGaranties
        )

        self.assertFalse(
            placement.estEnCours
        )

        self.assertIsNotNone(
            placement.dateFin
        )

    def test_livraison_pack_garanti(self):
        place = Place(1, 1, 1.5, 3)

        parking = Parking([place])

        client = Client(
            "yoyo",
            "12 rue Victor Hugo"
        )

        client.superSAbonner()

        voiture = Voiture(
            1.8,
            4,
            "GAR-123-LIV"
        )

        acces = Acces()

        ticket = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="livraison",
            heure_livraison="18:30"
        )

        self.assertTrue(
            ticket.startswith("Ticket - GAR-123-LIV - Garantie - N° ")
        )

        placement = voiture.placements[-1]

        self.assertIsNone(
            placement.place
        )

        self.assertIs(
            placement.parking,
            parking
        )

        self.assertEqual(
            placement.service,
            "livraison"
        )

        self.assertEqual(
            placement.adresseLivraison,
            "12 rue Victor Hugo"
        )

        self.assertEqual(
            placement.heureLivraison,
            "18:30"
        )

        self.assertTrue(
            voiture.priseEnChargeGarantie
        )

    def test_cycle_maintenance_depuis_acces(self):
        place = Place(1, 1, 5, 6)
        parking = Parking([place])

        client = Client(
            "yoyo",
            "Toulouse"
            )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "MA-333-AA"
            )

        acces = Acces()

        ticket = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="maintenance"
            )

        self.assertTrue(
            ticket.startswith("Ticket - MA-333-AA - Place 1 - N° ")
        )

        self.assertTrue(
            voiture.estDansParking
            )

        ancien_placement = voiture.placements[-1]

        self.assertEqual(
            ancien_placement.service,
            "maintenance"
            )

        resultat_depart = acces.lancer_service(
            voiture
            )

        self.assertTrue(
            resultat_depart
            )

        self.assertEqual(
            voiture.serviceEnCours,
            "maintenance"
            )

        self.assertFalse(
            voiture.estDansParking
            )

        self.assertIsNone(
            voiture.place
            )

        self.assertTrue(
            place.estLibre
            )

        self.assertFalse(
            ancien_placement.estEnCours
            )

        resultat_retour = acces.terminer_service(
            voiture
            )

        self.assertTrue(
            resultat_retour
            )

        self.assertEqual(
            voiture.serviceEnCours,
            "aucun"
            )   

        self.assertTrue(
            voiture.estDansParking
            )

        self.assertIsNotNone(
            voiture.place
            )

        self.assertFalse(
            voiture.place.estLibre
            )

        self.assertEqual(
            len(voiture.placements),
            2
            )

        nouveau_placement = voiture.placements[-1]

        self.assertIsNot(
            nouveau_placement,
            ancien_placement
            )

        self.assertTrue(
            nouveau_placement.estEnCours
            )

        self.assertIs(
            nouveau_placement.parking,
            parking
            )    

    def test_lancer_service_sans_maintenance_ni_entretien(self):
        place = Place(1, 1, 5, 6)
        parking = Parking([place])

        client = Client(
            "yoyo",
            "Toulouse"
            )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "NO-333-AA"
            )

        acces = Acces()

        client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="aucun"
            )

        resultat = acces.lancer_service(
            voiture
            )

        self.assertFalse(
            resultat
            )

        self.assertTrue(
            voiture.estDansParking
            )

        self.assertEqual(
            voiture.serviceEnCours,
            "aucun"
            )    

    def test_livraison_depuis_acces(self):
        place = Place(1, 1, 5, 6)
        parking = Parking([place])

        client = Client(
            "yoyo",
            "12 rue Victor Hugo"
            )

        client.estAbonne = True

        voiture = Voiture(
            1.8,
            4,
            "LI-666-AA"
            )

        acces = Acces()

        ticket = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="livraison",
            heure_livraison="18:30"
            )

        self.assertTrue(
            ticket.startswith("Ticket - LI-666-AA - Place 1 - N° ")
        )

        placement = voiture.placements[-1]

        self.assertEqual(
            placement.service,
            "livraison"
            )

        self.assertEqual(
            placement.adresseLivraison,
            "12 rue Victor Hugo"
            )

        self.assertEqual(
            placement.heureLivraison,
            "18:30"
            )

        resultat = acces.lancer_livraison(
            voiture
            )

        self.assertTrue(resultat)

        self.assertFalse(
            voiture.estDansParking
            )

        self.assertIsNone(
            voiture.place
            )

        self.assertTrue(
            place.estLibre
            )

        self.assertFalse(
            placement.estEnCours
            )

        self.assertIsNotNone(
            placement.dateFin
            )

    def test_livraison_pack_garanti_complete(self):
        place = Place(1, 1, 1.5, 3)
        parking = Parking([place])

        client = Client(
            "yoyo",
            "12 rue Victor Hugo"
            )

        client.superSAbonner()

        voiture = Voiture(
            1.8,
            4,
            "GAR-LIV-01"
            )

        acces = Acces()

        ticket = client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="livraison",
            heure_livraison="18:30"
            )   

        self.assertTrue(
            ticket.startswith("Ticket - GAR-LIV-01 - Garantie - N° ")
        )

        self.assertTrue(
            voiture.priseEnChargeGarantie
            )

        self.assertIn(
            voiture,
            parking.voituresGaranties
            )

        placement = voiture.placements[-1]

        self.assertIsNone(
            placement.place
            )

        self.assertEqual(
            placement.service,
            "livraison"
            )

        self.assertEqual(
            placement.adresseLivraison,
            "12 rue Victor Hugo"
            )

        self.assertEqual(
            placement.heureLivraison,
            "18:30"
            )

        resultat = acces.lancer_livraison(
            voiture
            )

        self.assertTrue(
            resultat
            )

        self.assertFalse(
            voiture.priseEnChargeGarantie
            )

        self.assertEqual(
            voiture.serviceGaranti,
            "aucun"
            )

        self.assertNotIn(
            voiture,
            parking.voituresGaranties
            )

        self.assertFalse(
            placement.estEnCours
            )

        self.assertIsNotNone(
            placement.dateFin
            )

    def test_modifier_service_vers_livraison(self):
        place = Place(1, 1, 5, 6)
        parking = Parking([place])

        client = Client("yoyo", "12 rue Victor Hugo")
        client.estAbonne = True

        voiture = Voiture(1.8, 4, "MOD-001")

        acces = Acces()

        client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="maintenance"
            )

        resultat = acces.modifier_service(
            client,
            voiture,
            "livraison",
            heure_livraison="19:00"
            )

        self.assertTrue(resultat)

        placement = voiture.placements[-1]

        self.assertEqual(
            placement.service,
            "livraison"
            )

        self.assertEqual(
            placement.adresseLivraison,
            "12 rue Victor Hugo"
            )

        self.assertEqual(
            placement.heureLivraison,
            "19:00"
            )

    def test_modifier_service_livraison_vers_entretien(self):
        place = Place(1, 1, 5, 6)
        parking = Parking([place])

        client = Client("yoyo", "12 rue Victor Hugo")
        client.estAbonne = True

        voiture = Voiture(1.8, 4, "MOD-002")

        acces = Acces()

        client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="livraison",
            heure_livraison="18:30"
            )

        resultat = acces.modifier_service(
            client,
            voiture,
            "entretien"
            )

        self.assertTrue(resultat)

        placement = voiture.placements[-1]

        self.assertEqual(
            placement.service,
            "entretien"
            )

        self.assertIsNone(
            placement.adresseLivraison
            )

        self.assertIsNone(
            placement.heureLivraison
            )

    def test_modifier_service_pack_garanti(self):
        place = Place(1, 1, 1.5, 3)
        parking = Parking([place])

        client = Client("yoyo", "Toulouse")
        client.superSAbonner()

        voiture = Voiture(1.8, 4, "MOD-GAR-01")

        acces = Acces()

        client.entrerParking(
            acces,
            voiture,
            parking,
            choix_service="maintenance"
            )

        resultat = acces.modifier_service(
            client,
            voiture,
            "entretien"
            )

        self.assertTrue(resultat)

        placement = voiture.placements[-1]

        self.assertEqual(
            placement.service,
            "entretien"
            )

        self.assertEqual(
            voiture.serviceGaranti,
            "entretien"
            )

        self.assertTrue(
            voiture.priseEnChargeGarantie
            )
        
    
    def test_passage_classique_vers_super(self):
        client = Client("Yoyo", "Toulouse")
        client.sAbonner()

        parking = Parking([])
        parking.ajouter_abonnement(
            Abonnement("Super-abonné", 40, True)
        )

        acces = Acces()

        resultat = acces.gerer_abonnement(
            client, parking, "CB", "Super-abonné"
        )

        self.assertIsNone(resultat)
        self.assertTrue(client.estAbonne)
        self.assertTrue(client.estSuperAbonne)

    def test_passage_classique_vers_super_paiement_invalide(self):
        client = Client("Yoyo", "Toulouse")
        client.sAbonner()

        parking = Parking([])
        parking.ajouter_abonnement(
            Abonnement("Super-abonné", 40, True)
        )

        acces = Acces()

        resultat = acces.gerer_abonnement(
            client, parking, "paiement_invalide", "Super-abonné"
        )

        self.assertEqual(
            resultat,
            "Erreur veuillez choisir votre mode de paiement"
        )
        self.assertTrue(client.estAbonne)
        self.assertFalse(client.estSuperAbonne)

    def test_conserver_abonnement_classique(self):
        client = Client("Yoyo", "Toulouse")
        client.sAbonner()

        parking = Parking([])
        acces = Acces()

        resultat = acces.gerer_abonnement(
            client, parking, None, "Aucun"
        )

        self.assertIsNone(resultat)
        self.assertTrue(client.estAbonne)
        self.assertFalse(client.estSuperAbonne)

    def test_super_abonne_conserve_son_abonnement(self):
        client = Client("Yoyo", "Toulouse")
        client.superSAbonner()

        parking = Parking([])
        parking.ajouter_abonnement(
            Abonnement("Super-abonné", 40, True)
        )

        acces = Acces()

        resultat = acces.gerer_abonnement(
            client, parking, None, "Super-abonné"
        )

        self.assertIsNone(resultat)
        self.assertTrue(client.estAbonne)
        self.assertTrue(client.estSuperAbonne)

        
if __name__ == "__main__":
    unittest.main()