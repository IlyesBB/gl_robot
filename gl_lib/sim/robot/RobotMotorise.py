import json
from _thread import RLock
from collections import OrderedDict

from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.config import PAS_TEMPS
from math import pi


class RobotMotorise(Robot):
    """
    Robot dont on commande les moteurs des roues
    """
    PAS_MAX = 0.01

    def __init__(self, pave=Pave(1, 1, 1, centre=Point(0, 0, 0)), rg=Roue(), rd=Roue(),
                 direction: Vecteur = Vecteur(1, 0, 0), tete:Tete=Tete()):
        """
        :param pave: forme du robot, a priori Pave
        :param rg: roue droite
        :param rd: roue gauche
        :param direction: direction du robot
        """
        Robot.__init__(self, pave, rg, rd, direction)
        self.tete = tete
        self.tete.attach(self.centre, self.direction)
        self.dist_wheels = (self.rd.centre - self.rg.centre).to_vect().get_mag()

        self.set_wheels_rotation(3, 0)

    def __str__(self):
        s = str(RobotMotorise.__name__)+", at "+str(self.centre)+", directed to "+str(self.direction)+"\n"
        return s

    # ports: 1 pour roue gauche, 2 pour roue droite
    # sommer pour modifier les deux

    def set_wheels_rotation(self, port, dps):
        """
        :param port:
        :param dps:
        :return:
        """
        if port == 1:
            self.rd.vitesseRot = dps
        elif port == 2:
            self.rg.vitesseRot = dps
        elif port == 3:
            self.rd.vitesseRot = dps
            self.rg.vitesseRot = dps

    def get_wheels_rotations(self, port:int):
        """
        :param port: 1,2 ou 3
        :return: int or tuple
        """
        if port == 1:
            return self.rd.vitesseRot
        elif port == 2:
            return self.rg.vitesseRot
        elif port == 3:
            return self.rd.vitesseRot, self.rg.vitesseRot

    def get_wheels_angles(self, port):
        if port == 1:
            return self.rg.angle
        elif port == 2:
            return self.rd.angle
        elif port == 3:
            return self.rd.angle, self.rg.angle

    def get_wheels_speed(self, port):
        if port == 1:
            return self.rg.vitesseRot
        elif port == 2:
            return self.rd.vitesseRot
        elif port == 3:
            return self.rd.vitesseRot, self.rg.vitesseRot

    def reset_wheels_angles(self):
        self.rg.angle = 0
        self.rd.angle = 0

    def update(self):
        self.update_pos()
        self.tete.update()

    def update_pos(self):
        """
        Met à jour la position du robot en fonction de la vitesse de rotation des roues
        :return:
        """
        # pas: float (représente la pas de temps)
        # angle_d, angle_g: float (angle de rotation de chaque roue pour cette mise à jour)
        pas = PAS_TEMPS
        angle_g = self.rg.vitesseRot * pas
        angle_d = self.rd.vitesseRot * pas
        # d_rot: float (la différence)
        d_rot = (self.rg.vitesseRot-self.rd.vitesseRot)*pas

        if d_rot == 0.0:
            # Dans ce cas, c'est un déplacement simple
            v = self.direction * (angle_d * self.rd.diametre * (pi / 180))
            self.move(v)
        else:
            # diffs: tuple[float] (contient les angles de rotation du robot par rapport à son centre
            diffs = (angle_d * (pi / 180) * (self.rd.diametre / self.dist_wheels),
                     angle_g * (pi / 180) * (self.rg.diametre / self.dist_wheels))

            # Angles dans le sens trigonométriques
            # négatif pour la roue droite, positif pour la roue gauche
            # v: Vecteur (celui dont le robot va avancer)
            if angle_d >= 0.0 and angle_g >= 0.0:
                v = self.direction * ((abs(angle_g-angle_d) + min(abs(angle_g), abs(angle_d))) *
                                      min(self.rd.diametre, self.rg.diametre) * (1/2.0) * (pi / 180))
            elif angle_d <= 0.0 and angle_g <= 0.0:
                v = self.direction * (-(abs(angle_g - angle_d) + min(abs(angle_g), abs(angle_d))) *
                                      min(self.rd.diametre, self.rg.diametre) * (1/2.0) * (pi / 180))
            else:
                # Cas non gérés
                v=Vecteur(0,0,0)

            self.move(v)
            self.direction.rotate(-diffs[0] + diffs[1])
            self.forme.rotate_all_around(self.centre, -diffs[0] + diffs[1])

        self.rg.angle += angle_g
        self.rd.angle += angle_d

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = RobotMotorise.__name__
        dct["direction"] = self.direction.__dict__()
        dct["tete"] = self.tete.__dict__() if self.tete is not None else None
        dct["forme"] = self.forme.__dict__()
        dct["dist_wheels"] = self.dist_wheels
        dct["rg"] = self.rg.__dict__()
        dct["rd"] = self.rd.__dict__()
        return dct

    @staticmethod
    def hook(dct):
        res = Tete.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == Roue.__name__:
            return Roue.hook(dct)
        elif dct["__class__"] == Pave.__name__:
            return Pave.hook(dct)
        elif dct["__class__"] == RobotMotorise.__name__:
            return RobotMotorise(dct["forme"], dct["rg"], dct["rd"] ,dct["direction"], dct["tete"])


    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=RobotMotorise.hook)

    def clone(self):
        return RobotMotorise(self.forme.clone(), self.rg.clone(), self.rd.clone(), self.direction.clone(), self.tete.clone())

if __name__ == '__main__':
    def test_mecanism():
        r = RobotMotorise(pave=Pave(1, 1, 0, centre=Point(5, 5, 0)), direction=Vecteur(1, 0, 0))
        r.set_wheels_rotation(1, 30)
        r.set_wheels_rotation(2, 30)
        p0 = r.centre.clone()
        n = int(1 / PAS_TEMPS) * 2

        for i in range(1, n):
            r.update()

        t_tot = n * PAS_TEMPS
        print("temps de la simulation: ", t_tot, " s")
        print("vitesse mesurée :", r.tete.lcapteurs[Tete.ACC].get_mesure(1))

        print(r.get_wheels_angles(3), " rads")
        print((r.get_wheels_angles(3)[0] / t_tot, r.get_wheels_angles(3)[1] / t_tot), " rads.s^-1")
        print("distance parcourue théorique: ", (p0 - r.centre).to_vect().get_mag())
        print("distance parcourue calculée: ", r.get_wheels_angles(1) * r.rd.diametre * (pi / 180))


    r=RobotMotorise()
    r.save("robotmotorise.json")
    r2 = RobotMotorise.load("robotmotorise.json")
    print(r2)

