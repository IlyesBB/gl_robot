from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement
from gl_lib.sim.geometry.fonctions import signe
from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import Tete, RobotMotorise
from math import pi
from time import sleep


class Tourner(StrategieDeplacement):
    """
    Fais décrire au robot un carré de coté 70 cm
    """

    def __init__(self, robot: RobotMotorise, angle_max=None, vitesse=30):
        """

        :param robot:
        """
        StrategieDeplacement.__init__(self, robot)
        self.rot_angle = 0

        if angle_max is not None:
            self.turning = True
            self.sens = signe(angle_max)
            self.angle_max = abs(angle_max)

            if self.sens > 0:
                self.robot.set_wheels_rotation(1, vitesse)
                self.robot.set_wheels_rotation(2, 0)
            elif self.sens < 0:
                self.robot.set_wheels_rotation(2, vitesse)
                self.robot.set_wheels_rotation(1, 0)
        else:
            self.sens = None
            self.angle_max = None
            self.turning = False
        self.robot.reset_wheels_angles()
        self.prev_dir=self.robot.direction.clone()

    def init_movement(self, angle_max, vitesse=30):
        #print("Turning ", angle_max, " degres...")

        self.turning = True
        self.rot_angle = 0

        self.sens=signe(angle_max)
        self.angle_max = abs(angle_max)

        if self.sens > 0:
            self.robot.set_wheels_rotation(2, vitesse)
            self.robot.set_wheels_rotation(1, 0)
        elif self.sens < 0:
            self.robot.set_wheels_rotation(1, vitesse)
            self.robot.set_wheels_rotation(2, 0)
        else:
            self.robot.set_wheels_rotation(3, 0)
        self.robot.reset_wheels_angles()

    def update(self):
        if self.turning is True:
            self.robot.update()
            dps_wheels = self.robot.get_wheels_rotations(3)
            vitesse_rot = abs(dps_wheels[0]-dps_wheels[1])*(pi/180)
            self.rot_angle += vitesse_rot * PAS_TEMPS * (self.robot.rd.diametre / self.robot.dist_wheels)

            v=self.robot.direction
            try:
                # Peut générer des erreurs si la vitesse est nulle
                if self.rot_angle>(self.angle_max*pi/180):
                    #print("Done turning ", self.sens*self.angle_max, "degrees")
                    Tourner.abort(self)
                    self.robot.set_wheels_rotation(3,0)
            except:
                pass

    def stop(self):
        return not self.turning

    def abort(self):
        self.turning=False
        self.sens = None
        self.rot_angle = 0


if __name__ == '__main__':
    from gl_lib.sim.simulation import Simulation
    from gl_lib.sim.robot.display.d2.gui import AppSimulationThread
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *

    r = RobotMotorise(Pave(centre=Point(3, 6, 0), width=1, height=1, length=1), direction=Vecteur(1,0,0))
    sim = Simulation(Tourner(r, 90))
    app = AppSimulationThread(sim)

    sim.start()
    app.start()
