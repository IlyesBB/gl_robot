from gl_lib.sim.robot.sensor import Capteur
from gl_lib.sim.geometry.point import *
from gl_lib.config import PAS_TEMPS


class Accelerometre(Capteur):
    """
    Permet de mesurer la vitesse et l'accélération du robot à un instant donné

    Les données sont mises à jour tous les PAS_TEMPS
    sauf si PAS_TEMPS < DT_MESURE, la durée de la mesure
    """
    DT_MESURE = 0.01
    MAX_CPT = int(DT_MESURE/PAS_TEMPS)

    def __init__(self, centre=Point(0, 0, 0), direction=Vecteur(1, 0, 0), tete=None):
        """
        On initialise les variables nécessaires pour calculer une vitesse et une accélération entre deux instants
        """
        Capteur.__init__(self, centre=centre, direction=direction, tete=tete)
        self.prev_pos = centre.clone()
        self.speed = Vecteur(0,0,0)
        self.acc = Vecteur(0,0,0)
        # Compteur pour savoir quand prendre la mesure
        self.cpt = 1

    def get_mesure(self, value):
        """
        retourne la vitesse actuelle, et actualise le dernier point de mesure de la position
        Si value vaut 1 : retourne la dernière vitesse mesurée
        Si value vaut 2: retourne la dernière accélération mesurée
        :return: float ou tuple selon value
        """
        if value == 1:
            return self.speed
        if value == 2:
            return self.acc
        if value == 3:
            return self.speed, self.acc

    def update(self):
        """
        Fonction destinée à être appelée tous les PAS_TEMPS
        Ne met à jour les mesures que si l'accéléromètre est prêt à répondre
        Sinon avance d'une unitée de temps
        :return:
        """

        if Accelerometre.MAX_CPT <1 or self.cpt>=Accelerometre.MAX_CPT:
            # Si DT_MESURE < PAS_TEMPS, la mesure est mise à jour dès que possible
            # Ou alors on a attendu assez longtemps
            new_speed = (self.centre - self.prev_pos).to_vect() / PAS_TEMPS
            self.prev_pos = self.centre.clone()
            self.acc = (new_speed - self.speed) / PAS_TEMPS
            self.speed=new_speed

        else:
            # Sinon, on avance d'une unité de temps
            self.cpt += 1


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, Tete

    r=RobotMotorise()
    acc=Accelerometre(tete=r.tete)

    v=Vecteur(1,0,0)*PAS_TEMPS
    p0=r.centre.clone()

    print(r.tete.add_sensors(acc=Accelerometre(tete=r.tete)))
    print(r.tete.lcapteurs[Tete.ACC].get_mesure(3))

    n=int(1/PAS_TEMPS)
    for i in range(1,n):
        r.move(v)
        r.update()
        print("vitesse mesurée :", r.tete.lcapteurs[Tete.ACC].get_mesure(1))
        print((p0-r.centre).to_vect().get_mag()/(i*PAS_TEMPS), r.tete.lcapteurs[Tete.ACC].get_mesure(1))

    print(n*PAS_TEMPS, " s")


