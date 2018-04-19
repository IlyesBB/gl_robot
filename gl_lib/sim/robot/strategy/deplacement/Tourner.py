import json
from collections import OrderedDict

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

    def __init__(self, robot: RobotMotorise, angle_max=None, vitesse=30,
                 sens = None, turning = False, rot_angle=0):
        """

        :param robot:
        """
        StrategieDeplacement.__init__(self, robot)
        self.rot_angle = 0

        if angle_max is not None and turning is False:
            self.turning = True
            self.sens = signe(angle_max)
            self.angle_max = abs(angle_max)
            self.rot_angle = 0

            if self.sens > 0:
                self.robot.set_wheels_rotation(1, vitesse)
                self.robot.set_wheels_rotation(2, 0)
            elif self.sens < 0:
                self.robot.set_wheels_rotation(2, vitesse)
                self.robot.set_wheels_rotation(1, 0)
        else:
            self.sens = sens
            self.angle_max = angle_max
            self.turning = turning
            self.rot_angle = rot_angle
        self.robot.reset_wheels_angles()
        self.prev_dir=self.robot.direction.clone()

    def init_movement(self, angle_max, vitesse=30):
        print("\nTurning ", angle_max, " degres...")

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
        self.angle_max = None

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = self.__class__.__name__
        dct["robot"] = self.robot.__dict__()

        dct["turning"] = self.turning
        dct["sens"] = self.sens
        dct["rot_angle"] = self.rot_angle
        dct["angle_max"] = self.angle_max

        return dct

    @staticmethod
    def deserialize(dct):
        res = StrategieDeplacement.deserialize(dct)
        if res is not None:
            return res
        elif dct["__class__"] == Tourner.__name__:
            return Tourner(dct["robot"], dct["angle_max"], 30, dct["sens"], dct["turning"], dct["rot_angle"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=Tourner.deserialize)

    def clone(self):
        return Tourner(self.robot.clone(), self.angle_max, 30,self.sens, self.turning, self.rot_angle)


if __name__ == '__main__':
    st = Tourner(RobotMotorise(), 45)

    st.save("tourner.json")

    st2 = Tourner.load("tourner.json")
    print(st2)
