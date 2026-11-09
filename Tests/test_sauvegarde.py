import json
import tempfile
import unittest

from pathlib import Path

from Class.abonnement import Abonnement
from Class.client import Client
from Class.parking import Parking
from Class.place import Place
from Class.placement import Placement
from Class.sauvegarde import Sauvegarde
from Class.voiture import Voiture
from Class.acces import Acces


class TestSauvegarde(unittest.TestCase):

    def setUp(self):
        self.dossier_temporaire = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier_temporaire.cleanup)

        self.chemin = Path(self.dossier_temporaire.name) / "donnees" / "dreampark.json"
        self.sauvegarde = Sauvegarde(self.chemin)

        self.parking = Parking([
            Place(1, 0, 2.2, 5.0),
            Place(2, 0, 2.5, 6.0),
            Place(3, 1, 2.0, 4.5)
        ])

        self.parking.ajouter_abonnement(Abonnement("Abonné classique", 20))
        self.parking.ajouter_abonnement(Abonnement("Super-abonné", 40, True))

        self.client = Client("Yoyo", "Paris")
        self.client.numeroCarte = 12345678
        self.client.sAbonner()
        self.client.nbFrequentations = 3

        self.clients = [self.client]

    def recharger(self):
        nouveau_parking = Parking([])
        nouveaux_clients = self.sauvegarde.charger(nouveau_parking)
        return nouveau_parking, nouveaux_clients

    def ajouter_voiture_stationnee(self):
        voiture = Voiture(1.8, 4.2, "AA-123-BB")
        self.parking.enregistrer_voiture(self.client, voiture)

        place = self.parking.places[0]
        placement = Placement(voiture, place, self.parking)
        self.parking.ajouter_placement(placement)
        voiture.ajout_placement(placement)
        place.ajout_placement(placement)
        voiture.place = place
        voiture.estDansParking = True

        return voiture, placement

    def test_chargement_sans_fichier(self):
        parking = Parking([Place(1, 0, 2.2, 5.0)])

        clients = self.sauvegarde.charger(parking)

        self.assertEqual(clients, [])
        self.assertEqual(len(parking.places), 1)
        self.assertEqual(parking.places[0].numero, 1)

    def test_enregistrement_cree_fichier_json(self):
        self.sauvegarde.enregistrer(self.parking, self.clients)

        self.assertTrue(self.chemin.is_file())

        with self.chemin.open("r", encoding="utf-8") as fichier:
            contenu = json.load(fichier)

        self.assertIsInstance(contenu, dict)

    def test_parking_vide_recharge(self):
        self.sauvegarde.enregistrer(self.parking, [])

        parking, clients = self.recharger()

        self.assertEqual(clients, [])
        self.assertEqual(len(parking.places), 3)
        self.assertEqual(parking.nombre_places_libres(), 3)
        self.assertEqual(parking.placements, [])

    def test_dimensions_et_niveaux_conserves(self):
        self.sauvegarde.enregistrer(self.parking, [])

        parking, _ = self.recharger()

        self.assertEqual(
            [(p.numero, p.niveau, p.hauteur, p.longueur) for p in parking.places],
            [(1, 0, 2.2, 5.0), (2, 0, 2.5, 6.0), (3, 1, 2.0, 4.5)]
        )

    def test_client_et_numero_carte_conserves(self):
        self.sauvegarde.enregistrer(self.parking, self.clients)

        _, clients = self.recharger()

        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0].nom, "Yoyo")
        self.assertEqual(clients[0].adresse, "Paris")
        self.assertEqual(clients[0].numeroCarte, 12345678)
        self.assertEqual(clients[0].nbFrequentations, 3)

    def test_abonnement_classique_conserve(self):
        self.sauvegarde.enregistrer(self.parking, self.clients)

        parking, clients = self.recharger()

        self.assertTrue(clients[0].estAbonne)
        self.assertFalse(clients[0].estSuperAbonne)
        self.assertEqual(len(parking.abonnements), 2)
        self.assertEqual(parking.abonnements[0].libelle, "Abonné classique")
        self.assertEqual(parking.abonnements[0].prix, 20)

    def test_super_abonnement_conserve(self):
        self.client.superSAbonner()
        self.sauvegarde.enregistrer(self.parking, self.clients)

        parking, clients = self.recharger()

        self.assertTrue(clients[0].estAbonne)
        self.assertTrue(clients[0].estSuperAbonne)
        self.assertTrue(parking.abonnements[1].estPackGar)

    def test_voiture_et_proprietaire_conserves(self):
        self.ajouter_voiture_stationnee()
        self.sauvegarde.enregistrer(self.parking, self.clients)

        parking, clients = self.recharger()

        voiture = parking.rechercher_voiture("AA-123-BB")
        self.assertIsNotNone(voiture)
        self.assertEqual(voiture.hauteur, 1.8)
        self.assertEqual(voiture.longueur, 4.2)
        self.assertIs(parking.responsables_voitures["AA-123-BB"], clients[0])
        self.assertIs(clients[0].rechercherVoiture("AA-123-BB"), voiture)

    def test_placement_actif_et_place_occupee_conserves(self):
        self.ajouter_voiture_stationnee()
        self.sauvegarde.enregistrer(self.parking, self.clients)

        parking, _ = self.recharger()

        voiture = parking.rechercher_voiture("AA-123-BB")
        place = parking.rechercher_place_numero(1)

        self.assertEqual(parking.nombre_places_libres(), 2)
        self.assertFalse(place.estLibre)
        self.assertIs(place.voiture, voiture)
        self.assertIs(voiture.place, place)
        self.assertTrue(voiture.estDansParking)
        self.assertTrue(place.placement.estEnCours)

    def test_reference_ticket_conservee(self):
        _, placement = self.ajouter_voiture_stationnee()
        reference_initiale = placement.reference_courte
        ticket_initial = placement.referenceTicket

        self.sauvegarde.enregistrer(self.parking, self.clients)
        parking, _ = self.recharger()

        self.assertEqual(parking.placements[0].referenceTicket, ticket_initial)
        self.assertEqual(parking.placements[0].reference_courte, reference_initiale)

    def test_sortie_avec_reference_apres_redemarrage(self):
        _, placement = self.ajouter_voiture_stationnee()
        reference = placement.reference_courte

        self.sauvegarde.enregistrer(self.parking, self.clients)
        parking, _ = self.recharger()

        voiture = parking.rechercher_voiture("AA-123-BB")
        resultat = Acces().lancer_procedure_sortie(reference, parking)

        self.assertIs(resultat, voiture)
        self.assertEqual(parking.nombre_places_libres(), 3)
        self.assertFalse(parking.placements[0].estEnCours)

    def test_historique_de_sortie_conserve(self):
        voiture, placement = self.ajouter_voiture_stationnee()
        reference = placement.reference_courte
        Acces().lancer_procedure_sortie(reference, self.parking)

        self.sauvegarde.enregistrer(self.parking, self.clients)
        parking, _ = self.recharger()

        self.assertEqual(len(parking.placements), 1)
        self.assertFalse(parking.placements[0].estEnCours)
        self.assertIsNotNone(parking.placements[0].dateFin)
        self.assertEqual(parking.nombre_places_libres(), 3)
        self.assertEqual(len(parking.rechercher_voiture("AA-123-BB").placements), 1)

    def test_service_et_livraison_conserves(self):
        voiture, placement = self.ajouter_voiture_stationnee()
        placement.service = "livraison"
        placement.heureLivraison = "18:30"
        placement.adresseLivraison = "Paris"
        voiture.serviceEnCours = "livraison"

        self.sauvegarde.enregistrer(self.parking, self.clients)
        parking, _ = self.recharger()

        nouveau_placement = parking.placements[0]
        nouvelle_voiture = parking.rechercher_voiture("AA-123-BB")

        self.assertEqual(nouveau_placement.service, "livraison")
        self.assertEqual(nouveau_placement.heureLivraison, "18:30")
        self.assertEqual(nouveau_placement.adresseLivraison, "Paris")
        self.assertEqual(nouvelle_voiture.serviceEnCours, "livraison")

    def test_deux_clients_et_voitures_sans_doublon(self):
        self.ajouter_voiture_stationnee()
        autre_client = Client("Autre", "Lyon")
        autre_client.numeroCarte = 87654321
        autre_voiture = Voiture(1.7, 4.0, "CC-456-DD")
        self.parking.enregistrer_voiture(autre_client, autre_voiture)
        self.clients.append(autre_client)

        self.sauvegarde.enregistrer(self.parking, self.clients)
        parking, clients = self.recharger()

        self.assertEqual(len(clients), 2)
        self.assertEqual(len(parking.registre_voitures), 2)
        self.assertEqual(len(clients[0].voitures), 1)
        self.assertEqual(len(clients[1].voitures), 1)
        self.assertIs(parking.responsables_voitures["CC-456-DD"], clients[1])

    def test_enregistrement_multiple_ne_duplique_pas(self):
        self.ajouter_voiture_stationnee()

        self.sauvegarde.enregistrer(self.parking, self.clients)
        self.sauvegarde.enregistrer(self.parking, self.clients)

        parking, clients = self.recharger()

        self.assertEqual(len(clients), 1)
        self.assertEqual(len(parking.placements), 1)
        self.assertEqual(len(parking.registre_voitures), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
