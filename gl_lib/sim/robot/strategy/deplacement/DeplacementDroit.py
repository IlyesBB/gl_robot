from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.config import PAS_TEMPS
from gl_lib.config import PIX_PAR_M
from math import sin, pi


class DeplacementDroit(Strategie):
    """
    Fais avancer le robot de 70 cm
    """

    def __init__(self, robot: RobotMotorise, distance_max):
        """

        :param robot:
        """
        self.robot = robot
        self.robot.reset_wheels_angles()
        self.robot.set_wheels_rotation(3, 60)
        self.advancing = True  # Booléen indiquant si le robot est en marche

        self.distance = 0
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()

    def init_movement(self, distance_max):
        self.advancing = True  # Booléen indiquant si le robot est en marche

        self.distance = 0
        self.distance_max = distance_max
        self.posDepart = self.robot.forme.centre.clone()
        self.robot.set_wheels_rotation(3, 60)
        self.robot.reset_wheels_angles()

    def update(self):
        """
        Met à jour la robot, et mesure la distance parcourue
        :return:
        """

        if self.advancing:
            self.robot.update()
            d = max(abs(self.robot.get_wheels_rotations(1)), abs(self.robot.get_wheels_rotations(2))) * \
                max(self.robot.rd.diametre, self.robot.rg.diametre) * PAS_TEMPS * (pi / 180)
            self.distance += d

            if self.distance > self.distance_max:
                self.advancing = False
                print("distance réellement parcourue :"
                      + str((self.posDepart - self.robot.forme.centre).to_vect().get_mag()))

    def stop(self):
        """
        Si on a dépassé la distance voulue, on s'arrête
        :return:
        """
        return not self.advancing


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise, Roue
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.geometry import *
    from gl_lib.sim.display.d2.gui import AppSimulationThread
    from gl_lib.sim.robot.sensor import Accelerometre
    from tkinter import *
    from threading import Thread
    import time

    r = RobotMotorise(Pave(1, 1, 0, centre=point.Point(5, 5, 0)), direction=point.Vecteur(0, -1, 0))
    r.tete.add_sensors(acc=Accelerometre(tete=r.tete))

    s = Simulation(DeplacementDroit(r, 3))

    newGUIThread = AppSimulationThread(s)
    s.start()
    newGUIThread.start()
