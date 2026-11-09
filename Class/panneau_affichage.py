class PanneauAffichage:

    def afficherNbPlacesDisponibles(self, parking):
        return f"Places disponibles : {parking.nombre_places_libres()}"