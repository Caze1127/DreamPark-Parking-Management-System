
import tkinter as tk

from pathlib import Path
from tkinter import messagebox

from .place import Place
from .parking import Parking
from .abonnement import Abonnement
from .sauvegarde import Sauvegarde

from Vue.vue_principale import VuePrincipale
from Controleur.controleur_principal import ControleurPrincipal


if __name__ == "__main__":

    places = []

    for numero in range(1, 21):

        if numero <= 7:
            niveau = 0

        elif numero <= 14:
            niveau = 1

        else:
            niveau = 2

        if numero % 3 == 0:
            hauteur = 2.5
            longueur = 6.0

        elif numero % 3 == 1:
            hauteur = 2.2
            longueur = 5.0

        else:
            hauteur = 2.0
            longueur = 4.5

        places.append(Place(numero, niveau, hauteur, longueur))

    parking = Parking(places)

    abonne = Abonnement("Abonné classique", 20)
    superAbonne = Abonnement("Super-abonné", 40, True)

    parking.ajouter_abonnement(abonne)
    parking.ajouter_abonnement(superAbonne)

    chemin = Path(__file__).resolve().parent.parent / "donnees" / "dreampark.json"
    sauvegarde = Sauvegarde(chemin)

    try:

        clients = sauvegarde.charger(parking)

    except (OSError, ValueError, KeyError, TypeError, IndexError) as erreur:

        root_erreur = tk.Tk()
        root_erreur.withdraw()

        messagebox.showerror(
            "Erreur de chargement",
            f"Impossible de charger les données : {erreur}",
            parent=root_erreur
        )

        root_erreur.destroy()
        raise SystemExit(1)

    numeros_existants = {place.numero for place in parking.places}

    for place in places:

        if place.numero not in numeros_existants:
            parking.places.append(place)

    root = tk.Tk()

    vue = VuePrincipale(root)

    controleur = ControleurPrincipal(
        vue,
        parking
    )

    controleur.clients = clients
    controleur.sauvegarde = sauvegarde

    controleur.actualiser_places()

    root.protocol(
        "WM_DELETE_WINDOW",
        controleur.fermer_application
    )

    vue.bouton_quitter.config(
        command=controleur.fermer_application
    )

    root.mainloop()
