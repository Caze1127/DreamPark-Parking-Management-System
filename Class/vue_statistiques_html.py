class VueStatistiquesHTML:

    def generer(self, resume):

        titre = "STATISTIQUES DREAM PARK "
        html = f"<!DOCTYPE html> \n    <html lang='fr'> \n\n        <head> \n             <meta charset= 'UTF-8' /> \n             <title> {titre} </title> \n        </head> \n\n        <body> \n\n                <h1> {titre} </h1> \n\n                "

        for cle, valeur in resume.items() :
            
            html += "<p>" +  cle + " : " + str(valeur) + "</p>" +"\n"
        
        html += "\n        </body> \n\n    </html>" 

        return html 

    def enregistrer(self, resume, nom_fichier):
    
            genere = self.generer(resume)
            
            with open(nom_fichier, "w", encoding="utf-8") as fichier:
                fichier.write(genere)
    
            return True 
    

