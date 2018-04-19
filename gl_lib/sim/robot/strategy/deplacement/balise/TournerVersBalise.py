import json
from collections import OrderedDict

from gl_lib.sim.robot.strategy.deplacement import Tourner
from gl_lib.sim.robot.strategy import Balise
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise
from gl_lib.sim.robot import RobotMotorise, Tete
from gl_lib.sim.robot.sensor.camera import Camera
from gl_lib.sim.geometry import *
from gl_lib.config import DT_SCREENSHOT
from gl_lib.sim.geometry import fonctions
import multiprocessing as mp
from math import pi
import os
import imageio as imo
from gl_lib.config import PAS_TEMPS, REPNAME_SCREENSHOTS, FILENAME_SCREENSHOT, FORMAT_SCREENSHOT

class TournerVersBalise(Tourner, StrategieVision):
    """
    Stratégie qui permet de tourner le robot robot vers une balise devant lui, si elle est visible

    Pour cela, on utilise les images capturée pour la caméra du robot

    """
    PRECISION = 10

    def __init__(self, robot: RobotMotorise, arene :Arene = None, balise: Balise = None, time_before_picture=DT_SCREENSHOT,
                 cpt_t:int=0, cpt:int=0, cpt_not_found:int=0, prev_res:tuple=(None, None)):
        """
        :param balise: contient des couleurs, si aucune n'est donnée en argument, on en crée une
        """
        StrategieVision.__init__(self, robot, arene)
        Tourner.__init__(self, robot)
        self.balise = balise
        self.cpt_t = cpt_t
        self.cpt = cpt
        self.cpt_not_found = cpt_not_found
        self.cpt_before_picture = int(time_before_picture/PAS_TEMPS)
        self.prev_res = prev_res
        if self.balise is None:
            self.balise = Balise()
        self.robot.set_wheels_rotation(3,0)

    def get_angle(self):
        """
        Retourne 1 si la balise est à droite, -1 si elle est à gauche

        Si l'angle formé par le vecteur formé par le milieu bas de l'écran et le centre de la balise
        avec la verticale est supérieur à 5 degrés, la balis est considérée devant le robot
        on retourne alors 0

        Si aucune balise trouvée retourne None
        :return: int
        """
        if self.cpt >= self.robot.tete.lcapteurs[Tete.CAM].cpt:
            if self.sens is not None and self.angle_max is not None:
                return self.angle_max*self.sens, self.sens
            else:
                return self.angle_max, self.sens

        #print("\nAnalysing image ", self.cpt,"...")
        p=trouver_balise(self.balise.colors, image=self.robot.tete.lcapteurs[Tete.CAM].get_image())
        if p is None:
            #print("No target found")
            self.cpt_not_found += 1
            self.cpt += 1
            return None, None

        angle = -(p[0]-0.5)*Camera.ANGLE_VY/4
        sens = signe(angle)
        if abs(angle) < TournerVersBalise.PRECISION:
            #print("Target ahead (", angle, " degres from vertical)")
            sens = 0
        self.prev_res = (angle, sens)
        self.cpt += 1
        self.cpt_not_found = 0

        return (angle, sens)

    def update(self):
        Tourner.update(self)
        StrategieVision.update(self)
        if self.cpt < self.robot.tete.lcapteurs[Tete.CAM].cpt:
            res = self.get_angle()
            self.action(res[1], res[0])
            self.last_res = res

        if self.cpt_t >= self.cpt_before_picture:
            self.robot.tete.lcapteurs[Tete.CAM].take_picture()
            self.cpt_t = 0
        self.cpt_t += 1

    def action(self, sens, angle):
        res = (angle, sens)
        if res[1] is None:
            Tourner.abort(self)
        elif res[1] == 0:
            Tourner.abort(self)
            self.sens = 0
        else:
            Tourner.init_movement(self, res[0])

    def stop(self):
        if self.sens == 0:
            #print("Target ahead")
            return True
        return False

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = TournerVersBalise.__name__
        dct["robot"] = self.robot.__dict__()
        dct["arene"] = self.arene.__dict__()

        dct["balise"] = self.balise.__dict__()
        dct["cpt_before_picture"] = self.cpt_before_picture
        dct["cpt_t"] = self.cpt_t
        dct["cpt"] = self.cpt
        dct["cpt_not_found"] = self.cpt_not_found

        dct["prev_res"] = tuple(self.prev_res) if self.prev_res is not None else None

        return dct

    @staticmethod
    def deserialize(dct):
        res = StrategieVision.deserialize(dct)
        if res is not None:
            return res
        elif dct["__class__"] == TournerVersBalise.__name__:
            return TournerVersBalise(dct)

    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=TournerVersBalise.deserialize)

