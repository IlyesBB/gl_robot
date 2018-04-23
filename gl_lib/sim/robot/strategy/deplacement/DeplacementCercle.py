import json
from collections import OrderedDict
from threading import Thread
from time import sleep

import pyglet

from gl_lib.config import PAS_TEMPS
from gl_lib.sim.robot import RobotMotorise
from gl_lib.sim.robot.strategy.deplacement import StrategieDeplacement, Tourner
from math import pi, cos, sin
from gl_lib.sim.geometry import fonctions

class DeplacementCercle(Tourner):
    """Dirige le robot pour dessiner un cercle, approximé par un polygone dont tous les points sont sur ce cercle

    Le robot commence à dessiner le cercle dans le sens de sa direction
    """
    def __init__(self, robot:RobotMotorise, angle_max:float or int = 360, diametre:int or float = 0.5,
                 vitesse: int or float = 30, sens=None, turning=False, rot_angle=0):
        """

        :param robot: Robot à déplacer
        :param angle_max: Angle duquel se déplacer sur le cercle
        :param diametre: Diamètre du cercle en mètres
        :param vitesse: Vitesse en degrés par seconde
        """
        Tourner.__init__(self, robot,angle_max, vitesse,sens, turning, rot_angle)
        self.diametre = abs(diametre)

        if angle_max is not None:
            self.sens = fonctions.signe(angle_max)
            DeplacementCercle.init_movement(self,angle_max,self.diametre,vitesse)



    def init_movement(self, angle_max,diametre_cercle=1, dps_moy=30):
        """ Initilise la trajectoire circulaire

        On Initialise les vitesses en résolvant un système à deux équations, du fait qu'on connaît le diamètre,
        et le périmètre du cercle (approché) qu'on dessine selon les vitesses
        :param angle_max: float (°)
        :param diametre_cercle: float (m)
        :param dps_moy: (°/s)
        :return:
        """
        if angle_max is None:
            return
        self.angle_max = abs(angle_max)
        self.rot_angle = 0
        self.turning = True
        diametre = diametre_cercle
        vitesse = abs(dps_moy)*self.robot.rd.diametre / 2
        sens = fonctions.signe(angle_max)
        vg = 2*vitesse/self.robot.rd.diametre
        vd = (1-(self.robot.rd.diametre/(2*diametre))) * 2 * vitesse / self.robot.rd.diametre

        if sens < 0:
            aux = vg
            vg = vd
            vd = aux

        self.robot.set_wheels_rotation(1,vd)
        self.robot.set_wheels_rotation(2,vg)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = self.__class__.__name__
        dct["sens"] = self.sens
        dct["turning"] = self.turning
        dct["robot"] = self.robot.__dict__()

        dct["diametre"] = self.diametre
        dct["rot_angle"] = self.rot_angle
        dct["angle_max"] = self.angle_max

        return dct


    @staticmethod
    def hook(dct):
        res = Tourner.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == DeplacementCercle.__name__:
            return DeplacementCercle(dct["robot"], dct["angle_max"], dct["diametre"], 30, dct["sens"], dct["turning"], dct["rot_angle"])

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DeplacementCercle.hook)

    def clone(self):
        return Tourner(self.robot.clone(), self.angle_max, 30,self.sens, self.turning, self.rot_angle)


if __name__ == '__main__':
    from gl_lib.sim import Simulation
    from gl_lib.sim.display.d2.gui import AppAreneThread
    from gl_lib.sim.robot import *
    from gl_lib.sim.robot.sensor import Accelerometre
    from gl_lib.sim.geometry import *


    a = AreneRobot()
    r = RobotMotorise(Pave(centre=Point(3.7, 6.7, 0), width=1, height=1, length=1))
    r.tete.sensors["cam"].arene = AreneFermee(3,3,3)
    td= Thread(target=r.tete.sensors["cam"].run)
    sim = Simulation([DeplacementCercle(r, 360, 1)], 3)
    a.add(r)
    app = AppAreneThread(a)
    app.start()
    min_x, min_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
    max_x, max_y = sim.strategie.robot.centre.x, sim.strategie.robot.centre.y
    dps_wheels = sim.strategie.robot.get_wheels_rotations(3)
    #td.start()
    sim.start()
    print(sim.stop, sim.strategie.stop())
    while not sim.stop:
        sleep(1)
        print(sim.cpt, sim.strategie.robot.get_wheels_rotations(3))
        if sim.strategie.robot.centre.x < min_x:
            min_x = sim.strategie.robot.centre.x
        if sim.strategie.robot.centre.x > max_x:
            max_x = sim.strategie.robot.centre.x
        if sim.strategie.robot.centre.y < min_y:
            min_y = sim.strategie.robot.centre.y
        if sim.strategie.robot.centre.y > max_y:
            max_y = sim.strategie.robot.centre.y

    print(sim.stop)

    d_rot = abs(dps_wheels[0]-dps_wheels[1])*PAS_TEMPS*(pi/180)
    max_rot = max(dps_wheels[0], dps_wheels[1])*PAS_TEMPS*(pi/180)
    d_dist = max_rot*(sim.strategie.robot.rd.diametre/2)
    n=(2*pi)/d_rot
    gr_diametre = n*d_dist/(2*pi)
    app.stop()
    #pyglet.app.exit()

    print(abs(max_x-min_x), abs(max_y-min_y))

    #sim.strategie.save("deplacementcercle.json")

    strat2 = DeplacementCercle.load("deplacementcercle.json")

