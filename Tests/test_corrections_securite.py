import unittest
from unittest.mock import MagicMock

from Class.acces import Acces
from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Class.voiture import Voiture
from Class.statistique import Statistique
from Class.teleporteur import Teleporteur
from Controleur.controleur_principal import ControleurPrincipal


class TestImmatriculationEtTickets(unittest.TestCase):
    def setUp(self):
        self.place = Place(1, 0, 2.2, 5.0)
        self.parking = Parking([self.place])
        self.acces = Acces()
        self.client = Client("Alice", "Paris")
        self.client.sAbonner()
        self.voiture = Voiture(1.8, 4.0, " aa-123-bb ")

    def entrer(self, client=None, voiture=None):
        return self.acces.lancer_procedure_entree(
            client or self.client, voiture or self.voiture, self.parking
        )

    def test_statistiques_reconnaissent_meme_plaque_dans_ancien_historique(self):
        premiere = Voiture(1.8, 4, "du-100-zz")
        seconde = Voiture(1.8, 4, " DU-100-ZZ ")
        parking = Parking([Place(1, 0, 2, 5)])
        teleporteur = Teleporteur()
        teleporteur.teleporter_voiture(premiere, parking.places[0], parking)
        premiere.sortir_du_parking()
        teleporteur.teleporter_voiture(seconde, parking.places[0], parking)
        stats = Statistique(parking)
        self.assertEqual(stats.nombre_voitures_distinctes(), 1)
        self.assertEqual(stats.nombre_passages_voiture(premiere), 2)
        self.assertEqual(len(stats.voitures_plus_frequentes()), 1)
        self.assertEqual(len(stats.voitures_regulieres(2)), 1)

    def test_normalisation_immatriculation(self):
        ticket = self.entrer()
        self.assertEqual(self.voiture.immatriculation, "AA-123-BB")
        self.assertTrue(ticket.startswith("Ticket - AA-123-BB - Place 1 - N° "))
        self.assertRegex(self.acces.borne.lire_ticket(ticket)[2], r"^[0-9A-F]{6}$")
        self.assertIs(self.parking.rechercher_voiture("  aa-123-bb "), self.voiture)
        self.assertIs(self.client.rechercherVoiture(" aA-123-bB "), self.voiture)

    def test_refus_doublon_actif_meme_client(self):
        self.entrer()
        resultat = self.entrer()
        self.assertEqual(resultat, "Ce véhicule possède déjà un stationnement actif")
        self.assertEqual(len(self.parking.placements), 1)

    def test_refus_doublon_actif_autre_client(self):
        self.entrer()
        autre_client = Client("Bob", "Lyon")
        autre_client.sAbonner()
        autre_voiture = Voiture(1.8, 4.0, "  AA-123-BB ")
        resultat = self.entrer(autre_client, autre_voiture)
        self.assertEqual(resultat, "Utilisez le véhicule déjà enregistré pour cette immatriculation")
        self.assertEqual(len(self.parking.placements), 1)

    def test_reentree_meme_voiture_et_ticket_different(self):
        premier_ticket = self.entrer()
        self.assertIs(self.acces.lancer_procedure_sortie(premier_ticket.split(" - N° ")[-1], self.parking), self.voiture)
        second_ticket = self.entrer()
        self.assertNotEqual(premier_ticket, second_ticket)
        self.assertEqual(len(self.parking.placements), 2)
        self.assertIs(self.parking.placements[0].voiture, self.parking.placements[1].voiture)
        self.assertEqual(len(self.client.voitures), 1)
        self.assertEqual(
            self.acces.lancer_procedure_sortie(premier_ticket.split(" - N° ")[-1], self.parking),
            "Ticket invalide ou expiré",
        )
        self.assertIs(self.acces.lancer_procedure_sortie(second_ticket.split(" - N° ")[-1], self.parking), self.voiture)

    def test_reference_ticket_invalide(self):
        ticket = self.entrer()
        reference = ticket.split(" - N° ")[-1]
        faux_ticket = reference[:-1] + ("0" if reference[-1] != "0" else "1")
        self.assertEqual(
            self.acces.lancer_procedure_sortie(faux_ticket, self.parking),
            "Ticket invalide ou expiré",
        )
        self.assertFalse(self.place.estLibre)

    def test_ancien_format_refuse(self):
        self.entrer()
        self.assertEqual(
            self.acces.lancer_procedure_sortie("Ticket - AA-123-BB - Place 1", self.parking),
            "Ticket invalide",
        )

    def test_reutilisation_apres_sortie_par_autre_client(self):
        ticket = self.entrer()
        self.acces.lancer_procedure_sortie(ticket.split(" - N° ")[-1], self.parking)
        bob = Client("Bob", "Lyon")
        bob.sAbonner()
        nouveau_ticket = self.entrer(bob, self.voiture)
        self.assertTrue(nouveau_ticket.startswith("Ticket - AA-123-BB - Place 1 - N° "))
        self.assertEqual(len(self.parking.registre_voitures), 1)
        self.assertIs(self.parking.rechercher_voiture("AA-123-BB"), self.voiture)
        self.assertNotIn(self.voiture, self.client.voitures)
        self.assertIn(self.voiture, bob.voitures)
        self.assertEqual(len(self.parking.placements), 2)

    def test_refus_nouvelle_entree_durant_maintenance(self):
        self.entrer()
        self.assertTrue(self.acces.modifier_service(self.client, self.voiture, "maintenance"))
        self.assertTrue(self.acces.lancer_service(self.voiture))
        self.assertEqual(self.parking.nombre_places_libres(), 1)
        autre_client = Client("Bob", "Lyon")
        autre_client.sAbonner()
        resultat = self.entrer(autre_client, self.voiture)
        self.assertEqual(resultat, "Ce véhicule est actuellement en service")
        self.assertEqual(len(self.parking.placements), 1)


class TestServicesGarantis(unittest.TestCase):
    def setUp(self):
        self.place = Place(1, 0, 1.5, 3.0)
        self.parking = Parking([self.place])
        self.acces = Acces()
        self.client = Client("Alice", "Paris")
        self.client.superSAbonner()
        self.voiture = Voiture(1.8, 4.0, "GG-100-AA")

    def test_cycle_service_garanti_sans_place(self):
        ticket_initial = self.acces.lancer_procedure_entree(self.client, self.voiture, self.parking)
        self.assertIn(" - Garantie - N° ", ticket_initial)
        self.assertEqual(len(self.parking.voituresGaranties), 1)
        self.assertTrue(self.acces.modifier_service(self.client, self.voiture, "maintenance"))
        self.assertTrue(self.acces.lancer_service(self.voiture))
        self.assertEqual(self.voiture.serviceEnCours, "maintenance")
        self.assertNotIn(self.voiture, self.parking.voituresGaranties)
        self.assertEqual(
            self.acces.lancer_procedure_sortie(ticket_initial.split(" - N° ")[-1], self.parking),
            "Ticket invalide ou expiré",
        )
        self.assertTrue(self.acces.terminer_service(self.voiture))
        self.assertEqual(self.voiture.serviceEnCours, "aucun")
        self.assertTrue(self.voiture.priseEnChargeGarantie)
        self.assertIn(self.voiture, self.parking.voituresGaranties)
        self.assertEqual(len(self.parking.placements), 2)
        ticket_nouveau = self.acces.borne.delivrer_ticket_garanti(self.voiture)
        self.assertNotEqual(ticket_initial, ticket_nouveau)
        self.assertEqual(
            self.acces.lancer_procedure_sortie(ticket_initial.split(" - N° ")[-1], self.parking),
            "Ticket invalide ou expiré",
        )
        self.assertIs(self.acces.lancer_procedure_sortie(ticket_nouveau.split(" - N° ")[-1], self.parking), self.voiture)
        self.assertEqual(self.parking.voituresGaranties, [])

    def test_retour_service_garanti_si_place_libre(self):
        self.acces.lancer_procedure_entree(self.client, self.voiture, self.parking)
        self.assertTrue(self.acces.modifier_service(self.client, self.voiture, "entretien"))
        self.assertTrue(self.acces.lancer_service(self.voiture))
        self.parking.places.append(Place(2, 0, 2.5, 5.0))
        self.assertTrue(self.acces.terminer_service(self.voiture))
        self.assertTrue(self.voiture.estDansParking)
        self.assertFalse(self.voiture.priseEnChargeGarantie)
        self.assertEqual(self.voiture.place.numero, 2)
        ticket_retour = self.acces.borne.delivrer_ticket(self.voiture, self.voiture.place)
        self.assertIs(self.acces.lancer_procedure_sortie(ticket_retour.split(" - N° ")[-1], self.parking), self.voiture)

    def test_non_abonne_sans_place_ne_peut_revenir(self):
        place = Place(2, 0, 2.5, 5.0)
        parking = Parking([place])
        client = Client("Clara", "Lille")
        client.sAbonner()
        voiture = Voiture(1.8, 4.0, "CL-101-BB")
        acces = Acces()
        acces.lancer_procedure_entree(client, voiture, parking)
        acces.modifier_service(client, voiture, "maintenance")
        self.assertTrue(acces.lancer_service(voiture))
        autre = Voiture(1.6, 4.2, "XX-000-XX")
        self.assertNotEqual(acces.lancer_procedure_entree(client, autre, parking), "Le parking est plein")
        self.assertFalse(acces.terminer_service(voiture))
        self.assertEqual(voiture.serviceEnCours, "maintenance")


class TestControleurSansTk(unittest.TestCase):
    def test_deux_entrees_normalisees_et_meme_objet(self):
        ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        ctrl.parking = Parking([Place(1, 0, 2.5, 5.0)])
        ctrl.client_identifie = Client("Alice", "Paris")
        ctrl.client_identifie.sAbonner()
        ctrl.clients = [ctrl.client_identifie]
        ctrl.vue_entree = MagicMock()
        ctrl.vue_message = MagicMock()
        ctrl.actualiser_places = MagicMock()
        ctrl.terminer_session = MagicMock()
        ctrl.sauvegarder_donnees = MagicMock(return_value=True)
        ctrl.vue_entree.champ_immatriculation.get.return_value = " aa-123-bb "
        ctrl.vue_entree.champ_hauteur.get.return_value = "1.8"
        ctrl.vue_entree.champ_longueur.get.return_value = "4.0"
        ctrl.vue_entree.mode_paiement.get.return_value = "Choisir un paiement"
        ctrl.vue_entree.choix_abonnement.get.return_value = "Choisir un abonnement"
        ctrl.valider_entree()
        self.assertEqual(len(ctrl.parking.registre_voitures), 1)
        voiture = ctrl.parking.rechercher_voiture("AA-123-BB")
        ticket = ctrl.vue_message.afficher_information.call_args[0][0].split("\n\n")[-1]
        sortie = Acces().lancer_procedure_sortie(ticket.split(" - N° ")[-1], ctrl.parking)
        self.assertIs(sortie, voiture)
        ctrl.vue_entree.champ_immatriculation.get.return_value = " AA-123-BB "
        ctrl.valider_entree()
        self.assertIs(ctrl.parking.rechercher_voiture("AA-123-BB"), voiture)
        self.assertEqual(len(voiture.placements), 2)
        self.assertEqual(len(ctrl.client_identifie.voitures), 1)

class TestNouveauTicketApresMaintenance(unittest.TestCase):
    def setUp(self):
        self.parking = Parking([Place(1, 0, 2.0, 5.0)])
        self.client = Client("Alice", "Paris")
        self.client.sAbonner()
        self.voiture = Voiture(1.8, 4.0, "MA-999-AA")
        self.acces = Acces()
        self.ticket_original = self.acces.lancer_procedure_entree(
            self.client, self.voiture, self.parking
        )
        self.assertTrue(self.acces.modifier_service(self.client, self.voiture, "maintenance"))
        self.assertTrue(self.acces.lancer_service(self.voiture))

    def test_retour_interface_affiche_nouveau_ticket(self):
        ctrl = ControleurPrincipal.__new__(ControleurPrincipal)
        ctrl.parking = self.parking
        ctrl.client_identifie = self.client
        ctrl.vue_message = MagicMock()
        ctrl.vue_service = MagicMock()
        ctrl.vue_service.champ_immatriculation.get.return_value = " ma-999-aa "
        ctrl.actualiser_places = MagicMock()
        ctrl.terminer_session = MagicMock()
        ctrl.sauvegarder_donnees = MagicMock(return_value=True)
        ctrl.terminer_service_interface()
        msg = ctrl.vue_message.afficher_information.call_args.args[0]
        self.assertIn("Nouveau ticket :", msg)
        second_ticket = msg.split("Nouveau ticket : ")[1]
        self.assertNotEqual(self.ticket_original, second_ticket)
        self.assertEqual(
            Acces().lancer_procedure_sortie(self.ticket_original.split(" - N° ")[-1], self.parking),
            "Ticket invalide ou expiré",
        )
        self.assertIs(Acces().lancer_procedure_sortie(second_ticket.split(" - N° ")[-1], self.parking), self.voiture)
        ctrl.terminer_session.assert_called_once()

    def test_retour_sans_place_et_sans_pack_est_refuse(self):
        voiture2 = Voiture(1.5, 3.8, "PP-200-AA")
        self.acces.teleporteur1.teleporter_voiture(voiture2, self.parking.places[0], self.parking)
        self.assertFalse(self.acces.terminer_service(self.voiture))
        self.assertEqual(self.voiture.serviceEnCours, "maintenance")
