from datetime import datetime
from uuid import uuid4

class Placement:
    def __init__(self, voiture, place, parking, service = "aucun"):
        self.voiture = voiture
        self.place = place
        codes_existants = {p.referenceTicket[:6] for p in parking.placements}
        reference = uuid4().hex
        while reference[:6] in codes_existants:
            reference = uuid4().hex
        self.referenceTicket = reference
        self.dateDebut = datetime.now()
        self.dateFin = None
        self.estEnCours = True
        self.service = service
        self.heureLivraison = None 
        self.adresseLivraison = None 
        self.parking = parking
        self.accesEntree = None
        self.accesSortie = None



    @property
    def reference_courte(self):
        return self.referenceTicket[:6].upper()

    def partirPlace(self):

        if self.estEnCours:
            
            self.dateFin = datetime.now()
            self.estEnCours = False
            
            if self.place is not None:
                self.place.liberer_place()
            
            self.voiture.estDansParking = False
            self.voiture.place = None
            
            return True
        
        else:
            return False

