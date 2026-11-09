from .statistique import Statistique


class Administrateur:
    def __init__(self, nom):
        self.nom = nom

    def consulter_statistiques(self, parking):
        return Statistique(parking).resume_statistiques()
