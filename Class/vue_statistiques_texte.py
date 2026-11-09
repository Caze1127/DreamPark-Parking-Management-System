class VueStatistiquesTexte:
    def generer(self, resume):

        titre = "===== STATISTIQUES DREAM PARK =====\n"

        for cle, valeur in resume.items() :
            titre += cle + " : " + str(valeur) + "\n"

        return titre 

    def enregistrer(self, resume, nom_fichier):

        genere = self.generer(resume)
        
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            fichier.write(genere)

        return True 
