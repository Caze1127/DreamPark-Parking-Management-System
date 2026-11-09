from datetime import timedelta

class Statistique:
    def __init__(self, parking):
        self.parking = parking

    def nombre_total_passages(self):
        return len(self.parking.placements)

    def nombre_passages_voiture(self, voiture):

        passage = 0

        for placement in self.parking.placements:

            if placement.voiture.immatriculation == voiture.immatriculation :

                passage += 1
        
        return passage

    def voitures_plus_frequentes(self):
        compteurs = {}
        references = {}
        for placement in self.parking.placements:
            plaque = placement.voiture.immatriculation
            compteurs[plaque] = compteurs.get(plaque, 0) + 1
            references[plaque] = placement.voiture
        if not compteurs:
            return []
        maximum = max(compteurs.values())
        return [references[plaque] for plaque, compte in compteurs.items()
                if compte == maximum]

    def nombre_passages_service(self, service):
        
        cptr = 0

        for placement in self.parking.placements:
            
            if placement.service == service :
                
                cptr += 1
        
        return cptr 

    def activite_service(self):
        
        maintenance =  self.nombre_passages_service("maintenance")
        entretien = self.nombre_passages_service("entretien")
        livraison = self.nombre_passages_service("livraison")
        aucun = self.nombre_passages_service("aucun")

        activite = {
            "maintenance": maintenance,
            "entretien": entretien,
            "livraison": livraison,
            "aucun": aucun
            }
        
        return activite

    def nombre_passages_termines(self):

        cptr = 0

        for placement in self.parking.placements:
            
            if not placement.estEnCours :
                
                cptr += 1
        
        return cptr

    def nombre_passages_en_cours(self):

        cptr = 0 

        for placement in self.parking.placements : 
            
            if placement.estEnCours :
                
                cptr += 1 

        return cptr

    def duree_moyenne_stationnement(self):

        total = timedelta(0)
        placementTermine = self.nombre_passages_termines()

        if placementTermine == 0 :
            return timedelta(0)

        for placement in self.parking.placements:

            if not placement.estEnCours:
                
                total += placement.dateFin - placement.dateDebut

        return total / placementTermine

    def nombre_voitures_distinctes(self):
        return len({p.voiture.immatriculation for p in self.parking.placements})

    def nombre_moyen_passage_voiture_distinctes(self):

        nbrDistinctes = self.nombre_voitures_distinctes()
        nbrTotal = self.nombre_total_passages()

        if nbrDistinctes == 0:
            return 0

        return nbrTotal / nbrDistinctes 

    def services_plus_utilises(self):
        
        liste = []
        maxi = 0

        activite = self.activite_service()


        if self.nombre_total_passages() == 0 :

            return liste
        
        for service, valeur in activite.items() :
            
            if valeur > maxi :

                maxi = valeur
                liste.clear()
                liste.append(service)

            elif valeur == maxi :

                liste.append(service)

        return liste 
            
            
    def nombre_passages_niveau(self, niveau):

        cptr = 0 

        for placement in self.parking.placements: 

            if placement.place is not None :
                
                if placement.place.niveau == niveau:
                    cptr += 1

        return cptr

    def frequentation_niveaux(self):

        liste = []
        frequentation = {}
            
        for place in self.parking.places :
            
            if place.niveau not in liste:

                liste.append(place.niveau)

        for niveau in liste :
            
            nbr = self.nombre_passages_niveau(niveau)
            frequentation[niveau] = nbr
        
        return frequentation 

    def niveaux_plus_frequentes(self):

        liste = []
        maxi = 0
        
        niveaux = self.frequentation_niveaux()

        if sum(niveaux.values()) == 0 :
            
            return liste

        for niveau , valeur in niveaux.items() :
                    
            if valeur > maxi :

                maxi = valeur
                liste.clear()
                liste.append(niveau)

            elif valeur == maxi :

                liste.append(niveau)

        return liste 

    def nombre_passages_place(self, place):
        
        cptr = 0 
        
        for placement in self.parking.placements: 

            if placement.place is not None :
                
                if placement.place == place:
                    cptr += 1

        return cptr

    def frequentation_places(self):
        
        frequentation = {}
            
        for place in self.parking.places :
            
            nbr = self.nombre_passages_place(place)    
            frequentation[place.numero] = nbr
        
        return frequentation 
    
    def place_plus_frequentes(self):
    
            liste = []
            maxi = 0
            
            places = self.frequentation_places()
    
            if sum(places.values()) == 0 :
                        
                return liste
    
            for numero , valeur in places.items() :
                        
                if valeur > maxi :
    
                    maxi = valeur
                    liste.clear()
                    liste.append(numero)
    
                elif valeur == maxi :
    
                    liste.append(numero)
    
            return liste 

    def voitures_regulieres(self, seuil):
        voitures = {}
        for placement in self.parking.placements:
            voitures[placement.voiture.immatriculation] = placement.voiture
        return [voiture for voiture in voitures.values()
                if self.nombre_passages_voiture(voiture) >= seuil]

    def stationnement_max(self):

        maxi = timedelta(0)
        placementTermine = self.nombre_passages_termines()

        if placementTermine == 0 :
            return timedelta(0)

        for placement in self.parking.placements:

            if not placement.estEnCours :

                stationnement = placement.dateFin - placement.dateDebut

                if stationnement > maxi :

                    maxi = stationnement 
        
        return maxi

    def immatriculations_voitures(self, voitures):

        immatriculations = []

        for voiture in voitures:
           
           immatriculations.append(voiture.immatriculation)

        return immatriculations

    def formater_duree(self, duree):

        secondes = int(duree.total_seconds())

        heures = secondes // 3600
        restes = secondes % 3600

        minutes = restes // 60
        restes = restes % 60
       
        return f"{heures} h {minutes} min {restes} s"
    

    def resume_statistiques(self):

        resume = {}

        totalPassage = self.nombre_total_passages()
        plusFrequenteVoiture = self.immatriculations_voitures(self.voitures_plus_frequentes())
        activiteService = self.activite_service()
        passageTermine = self.nombre_passages_termines()
        passageEnCours = self.nombre_passages_en_cours()
        moyenneStationnement = self.formater_duree(self.duree_moyenne_stationnement())
        voituresDistinctes = self.nombre_voitures_distinctes()
        moyennePassageVoitureDistincte = self.nombre_moyen_passage_voiture_distinctes()
        sevicePlusUtilise = self.services_plus_utilises()
        frequenceNiveau = self.frequentation_niveaux()
        niveauPlusfrequente = self.niveaux_plus_frequentes()
        frequentationPlace = self.frequentation_places()
        placeFrequente = self.place_plus_frequentes()
        stationnementMax = self.formater_duree(self.stationnement_max())



        resume.update(
            {
                "Total passage" : totalPassage,
                "Voiture(s) la/les plus fréquente(s)" : plusFrequenteVoiture,
                "Activité des services" : activiteService,
                "Total des passages terminés" : passageTermine,
                "Total des passages en cours" : passageEnCours,
                "Durée moyenne de stationnement" : moyenneStationnement,
                "Nombre de voitures distinctes" : voituresDistinctes,
                "Nombre moyen de passage par voiture" : moyennePassageVoitureDistincte,
                "Service le plus utilisé" : sevicePlusUtilise,
                "Fréquence par niveau" : frequenceNiveau,
                "Niveau le plus fréquenté" : niveauPlusfrequente,
                "Fréquentation par place" : frequentationPlace,
                "Place(s) la/les plus fréquentée(s)" : placeFrequente,
                "Durée de stationnement maximum" : stationnementMax,
            }
        )

        return resume 