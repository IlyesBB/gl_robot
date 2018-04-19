import json
from collections import OrderedDict

from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Point
from gl_lib.config import PIX_PAR_M
from math import sin, pi
from math import sqrt

class DeplacementDroit(StrategieDeplacement):
    """
    Fais avancer le robot de 70 cm
    """

    def __init__(self, robot: RobotMotorise, distance_max, advancing=True, distance = 0,
                 posDepart:Point=None):
        """

        :param robot:
        """
        StrategieDeplacement.__init__(self,robot)
        self.robot = robot
        self.robot.reset_wheels_angles()
        self.robot.set_wheels_rotation(3, 60)
        self.advancing = advancing  # Booléen indiquant si le robot est en marche

        self.distance = distance
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()
        if posDepart is not None:
            self.posDepart = posDepart

    def init_movement(self, distance_max, vitesse=60):
        self.advancing = True  # Booléen indiquant si le robot est en marche

        self.distance = 0
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()
        self.robot.set_wheels_rotation(3, vitesse)
        self.robot.reset_wheels_angles()

    def update(self):
        """
        Met à jour la robot, et mesure la distance parcourue
        :return:
        """
        if self.advancing:
            with self.robot.lock_update_pos:
                self.robot.update()
            d = max(abs(self.robot.get_wheels_rotations(1)), abs(self.robot.get_wheels_rotations(2))) * \
                max(self.robot.rd.diametre, self.robot.rg.diametre) * PAS_TEMPS * (pi / 180)
            self.distance += d

            if self.distance > self.distance_max:
                self.advancing = False
                #print("Done advancing ", self.distance, " meters")
                DeplacementDroit.abort(self)

    def abort(self):
        self.advancing=False
        self.distance_max=0
        self.distance=0
        self.robot.reset_wheels_angles()

    def stop(self):
        """
        Si on a dépassé la distance voulue, on s'arrête
        :return:
        """
        return not self.advancing

class DeplacementDroitAmeliore(DeplacementDroit):
    def __init__(self, robot, distance_max, arene, proximite_max=None, advancing=True, distance=0, posDepart:Point=None,
                last_detected = None):
        DeplacementDroit.__init__(self, robot, distance_max, advancing, distance, posDepart)
        self.arene=arene
        self.proximite_max=self.robot.forme.get_length()*2
        self.last_detected = last_detected
        self.proximite_max = proximite_max if proximite_max is not None else robot.forme.get_length()*2

    def update(self):
        if self.advancing:
            res=self.robot.tete.lcapteurs[Tete.IR].get_mesure(self.arene, ignore=self.robot)
            if res > -1:
                if res < self.proximite_max:
                    #print("Obstacle ahead detected ( ", res, " meters )")
                    DeplacementDroit.abort(self)
            self.last_detected = res
        DeplacementDroit.update(self)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DeplacementDroitAmeliore.__name__
        dct["robot"] = self.robot.__dict__()
        dct["arene"] = self.arene.__dict__()

        dct["advancing"] = self.advancing
        dct["distance"] = self.distance
        dct["distance_max"] = self.distance_max
        dct["posDepart"] = self.posDepart.__dict__()

        dct["proximite_max"] = self.proximite_max
        dct["last_detected"] = self.last_detected

        return dct

    @staticmethod
    def deserialize(dct):
        res = StrategieDeplacement.deserialize(dct)
        if res is not None:
            return res
        elif dct["__class__"] == DeplacementDroitAmeliore.__name__:
            return DeplacementDroitAmeliore(dct)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementDroitAmeliore.deserialize)

    def clone(self):
        return DeplacementDroitAmeliore(self.robot.clone(), self.distance_max, self.arene.clone(), self.proximite_max, self.advancing,
                                        self.distance, self.posDepart.clone(), self.last_detected)

    def dict(self):
        dda = DeplacementDroitAmeliore.clone(self)
        return dda.__dict__()

class DDroitAmelioreVision(DeplacementDroitAmeliore, StrategieVision):
    def __init__(self, robot, distance, arene):
        StrategieVision.__init__(self, robot, arene)
        DeplacementDroitAmeliore.__init__(self, robot, distance, arene)

if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, Tete
    from gl_lib.sim.geometry import *
    from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore
    from gl_lib.sim import Simulation
    from gl_lib.sim.display.d2.gui import AppAreneThread
    v=Vecteur(1,1,0).norm()
    p = Pave(1, 1, 0)
    p.move(v*3)
    p.rotate(-pi/4)

    r=RobotMotorise(direction=v.clone())
    a = Arene()
    a.add(p)
    a.add(r)

    strat = DeplacementDroitAmeliore(r,3, a)
    # Le sensor suit le pave, et on affiche la mesure a chaque rotation
    s = Simulation(strat)

    newGUIThread = AppAreneThread(strat.arene)
    s.start()
    newGUIThread.start()

