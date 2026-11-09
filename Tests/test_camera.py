import unittest
from Class.camera import Camera
from Class.voiture import Voiture

class TestCamera(unittest.TestCase):
    def test_camera(self):
        voiture = Voiture(2,6,"AB-434-AZ")
        camera = Camera()

        resultat1 = camera.capturer_hauteur(voiture)
        resultat2 = camera.capturer_longueur(voiture)
        resultat3 = camera.capturer_immatriculation(voiture)

        self.assertEqual(resultat1, voiture.hauteur)
        self.assertEqual(resultat2, voiture.longueur)
        self.assertEqual(resultat3, voiture.immatriculation)

if __name__ == "__main__":
    unittest.main()