from .voiture import Voiture

class BorneTicket:
    def delivrer_ticket(self, voiture, place):
        placement = place.placement
        if placement is None or not placement.estEnCours:
            raise ValueError("Aucun placement actif pour délivrer un ticket")
        return (
            f"Ticket - {voiture.immatriculation} - Place {place.numero}"
            f" - N° {placement.reference_courte}"
        )

    def delivrer_ticket_garanti(self, voiture):
        placement = next(
            (p for p in reversed(voiture.placements)
             if p.estEnCours and p.place is None), None
        )
        if placement is None:
            raise ValueError("Aucun placement garanti actif")
        return (
            f"Ticket - {voiture.immatriculation} - Garantie"
            f" - N° {placement.reference_courte}"
        )

    def proposer_services(self):
        return "Services disponibles : maintenance, entretien, livraison, aucun"

    def recuperer_infos_carte(self, client):
        return client.estAbonne, client.estSuperAbonne

    def valider_choix_service(self, choix):
        
        if choix in ["maintenance", "entretien", "livraison", "aucun"]:
            return choix
        
        return None

    def valider_mode_paiement(self,mode):
        
        if mode in ["CB", "Espece"]:
            return mode
        
        return None

    def proposer_abonnements(self, parking):
        return parking.abonnements

    def valider_choix_abonnement(self, choix, parking):
        
        for abonnement in parking.abonnements:
            
            if abonnement.libelle == choix:
                return abonnement

        return None

    def lire_ticket(self, ticket):
        parties = ticket.strip().split(" - ")
        if len(parties) != 4 or parties[0] != "Ticket":
            return None

        immatriculation = Voiture.normaliser_immatriculation(parties[1])
        localisation = parties[2]
        reference = parties[3]
        if not immatriculation or not reference.startswith("N° "):
            return None

        reference = reference[3:].upper()
        import re
        if re.fullmatch(r"[0-9A-F]{6}", reference) is None:
            return None

        if localisation == "Garantie":
            return immatriculation, "Garantie", reference

        morceaux = localisation.split()
        if len(morceaux) != 2 or morceaux[0] != "Place" or not morceaux[1].isdigit():
            return None

        return immatriculation, int(morceaux[1]), reference
