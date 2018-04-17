from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.config import PAS_TEMPS
from gl_lib.config import PIX_PAR_M
from math import sin, pi
from math import sqrt

class DeplacementDroit(StrategieDeplacement):
    """
    Fais avancer le robot de 70 cm
    """

    def __init__(self, robot: RobotMotorise, distance_max):
        """

        :param robot:
        """
        StrategieDeplacement.__init__(self,robot)
        self.robot = robot
        self.robot.reset_wheels_angles()
        self.robot.set_wheels_rotation(3, 60)
        self.advancing = True  # Booléen indiquant si le robot est en marche

        self.distance = 0
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()

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
    def __init__(self, robot, distance_max, arene):
        DeplacementDroit.__init__(self, robot, distance_max)
        self.arene=arene
        self.proximite_max=self.robot.forme.get_length()*2
        self.last_detected = None

    def update(self):
        if self.advancing:
            res=self.robot.tete.lcapteurs[Tete.IR].get_mesure(self.arene, ignore=self.robot)
            if res > -1:
                if res < self.proximite_max:
                    #print("Obstacle ahead detected ( ", res, " meters )")
                    DeplacementDroit.abort(self)
            self.last_detected = res
        DeplacementDroit.update(self)

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

