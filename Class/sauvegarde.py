
import json
import os

from datetime import datetime
from pathlib import Path

from .abonnement import Abonnement
from .client import Client
from .place import Place
from .placement import Placement
from .voiture import Voiture


class Sauvegarde:

    def __init__(self, chemin_fichier):

        self.chemin_fichier = Path(chemin_fichier)

    def serialiser_client(self, client):

        return {
            "nom": client.nom,
            "adresse": client.adresse,
            "numeroCarte": client.numeroCarte,
            "estAbonne": client.estAbonne,
            "estSuperAbonne": client.estSuperAbonne,
            "nbFrequentations": client.nbFrequentations
        }

    def serialiser_voiture(self, voiture):

        return {
            "immatriculation": voiture.immatriculation,
            "hauteur": voiture.hauteur,
            "longueur": voiture.longueur,
            "estDansParking": voiture.estDansParking,
            "priseEnChargeGarantie": voiture.priseEnChargeGarantie,
            "serviceGaranti": voiture.serviceGaranti,
            "serviceEnCours": voiture.serviceEnCours,
            "retourServiceGaranti": voiture.retourServiceGaranti
        }

    def serialiser_place(self, place):

        return {
            "numero": place.numero,
            "niveau": place.niveau,
            "hauteur": place.hauteur,
            "longueur": place.longueur
        }

    def serialiser_placement(self, placement):

        return {
            "immatriculation": placement.voiture.immatriculation,
            "numeroPlace": placement.place.numero if placement.place is not None else None,
            "referenceTicket": placement.referenceTicket,
            "accesEntree": placement.accesEntree,
            "accesSortie": placement.accesSortie,
            "dateDebut": placement.dateDebut.isoformat(),
            "dateFin": placement.dateFin.isoformat() if placement.dateFin is not None else None,
            "estEnCours": placement.estEnCours,
            "service": placement.service,
            "heureLivraison": placement.heureLivraison,
            "adresseLivraison": placement.adresseLivraison
        }

    def enregistrer(self, parking, clients):

        tous_clients = list(clients)

        for client in parking.responsables_voitures.values():

            if client not in tous_clients:
                tous_clients.append(client)

        voitures = {}

        for voiture in parking.registre_voitures.values():
            voitures[voiture.immatriculation] = voiture

        for placement in parking.placements:
            voitures[placement.voiture.immatriculation] = placement.voiture

        for voiture in parking.voituresGaranties:
            voitures[voiture.immatriculation] = voiture

        for client in tous_clients:

            for voiture in client.voitures:
                voitures[voiture.immatriculation] = voiture

        responsables = {}

        for immatriculation, client in parking.responsables_voitures.items():

            if client in tous_clients:
                responsables[immatriculation] = tous_clients.index(client)

        donnees = {
            "version": 1,
            "clients": [self.serialiser_client(client) for client in tous_clients],
            "voitures": [self.serialiser_voiture(voiture) for voiture in voitures.values()],
            "places": [self.serialiser_place(place) for place in parking.places],
            "placements": [self.serialiser_placement(placement) for placement in parking.placements],
            "abonnements": [
                {
                    "libelle": abonnement.libelle,
                    "prix": abonnement.prix,
                    "estPackGar": abonnement.estPackGar
                }
                for abonnement in parking.abonnements
            ],
            "responsables": responsables,
            "voituresGaranties": [
                voiture.immatriculation
                for voiture in parking.voituresGaranties
            ]
        }

        self.chemin_fichier.parent.mkdir(parents=True, exist_ok=True)

        chemin_temporaire = self.chemin_fichier.with_name(
            self.chemin_fichier.name + ".tmp"
        )

        with open(chemin_temporaire, "w", encoding="utf-8") as fichier:

            json.dump(donnees, fichier, ensure_ascii=False, indent=4)

        os.replace(chemin_temporaire, self.chemin_fichier)

        return True

    def charger(self, parking):

        if not self.chemin_fichier.is_file():
            return []

        with open(self.chemin_fichier, "r", encoding="utf-8") as fichier:

            donnees = json.load(fichier)

        if donnees.get("version") != 1:
            raise ValueError("Version de sauvegarde incompatible")

        clients = []

        for informations in donnees["clients"]:

            client = Client(
                informations["nom"],
                informations["adresse"]
            )

            client.numeroCarte = informations["numeroCarte"]
            client.estAbonne = informations["estAbonne"]
            client.estSuperAbonne = informations["estSuperAbonne"]
            client.nbFrequentations = informations["nbFrequentations"]

            clients.append(client)

        places = {}

        for informations in donnees["places"]:

            place = Place(
                informations["numero"],
                informations["niveau"],
                informations["hauteur"],
                informations["longueur"]
            )

            places[place.numero] = place

        voitures = {}

        for informations in donnees["voitures"]:

            voiture = Voiture(
                informations["hauteur"],
                informations["longueur"],
                informations["immatriculation"]
            )

            voiture.estDansParking = informations["estDansParking"]
            voiture.priseEnChargeGarantie = informations["priseEnChargeGarantie"]
            voiture.serviceGaranti = informations["serviceGaranti"]
            voiture.serviceEnCours = informations["serviceEnCours"]
            voiture.retourServiceGaranti = informations["retourServiceGaranti"]

            voitures[voiture.immatriculation] = voiture

        abonnements = []

        for informations in donnees["abonnements"]:

            abonnement = Abonnement(
                informations["libelle"],
                informations["prix"],
                informations["estPackGar"]
            )

            abonnements.append(abonnement)

        placements = []

        for informations in donnees["placements"]:

            voiture = voitures[informations["immatriculation"]]
            numero_place = informations["numeroPlace"]

            place = places[numero_place] if numero_place is not None else None

            placement = Placement(
                voiture,
                place,
                parking,
                informations["service"]
            )

            placement.referenceTicket = informations["referenceTicket"]
            placement.accesEntree = informations.get("accesEntree")
            placement.accesSortie = informations.get("accesSortie")
            placement.dateDebut = datetime.fromisoformat(informations["dateDebut"])

            if informations["dateFin"] is not None:
                placement.dateFin = datetime.fromisoformat(informations["dateFin"])

            placement.estEnCours = informations["estEnCours"]
            placement.heureLivraison = informations["heureLivraison"]
            placement.adresseLivraison = informations["adresseLivraison"]

            voiture.placements.append(placement)
            placements.append(placement)

            if placement.estEnCours and place is not None:

                if not place.ajout_placement(placement):
                    raise ValueError("Plusieurs véhicules occupent la même place")

                voiture.place = place

        responsables = {}

        for immatriculation, index in donnees["responsables"].items():

            client = clients[index]
            voiture = voitures[immatriculation]

            responsables[immatriculation] = client

            if voiture not in client.voitures:
                client.voitures.append(voiture)

        garanties = []

        for immatriculation in donnees["voituresGaranties"]:
            garanties.append(voitures[immatriculation])

        parking.places = list(places.values())
        parking.abonnements = abonnements
        parking.placements = placements
        parking.registre_voitures = voitures
        parking.responsables_voitures = responsables
        parking.voituresGaranties = garanties

        return clients
