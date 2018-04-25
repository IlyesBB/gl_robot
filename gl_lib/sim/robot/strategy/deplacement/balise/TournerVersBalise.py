# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot.sensor import Camera
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot.strategy import Balise
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise
from gl_lib.sim.robot.strategy.deplacement import Tourner
from gl_lib.config import DT_SCREENSHOT, PAS_TEMPS


class TournerVersBalise(Tourner, StrategieVision):
    """
    Stratégie qui permet de tourner le robot robot vers une balise devant lui, si elle est visible
    Pour cela, on utilise les images capturée pour la caméra du robot
    """
    # Précision en degrés avec laquelle n considère que la balise est devant
    PRECISION = 5
    INIT = {"prev_res": None, "balise": Balise(), "cpt": 0, "cpt_before_picture": DT_SCREENSHOT,
            "cpt_not_found": 0}
    KEYS = set(Tourner.KEYS + ["prev_res", "balise", "cpt", "cpt_before_picture", "cpt_not_found"] + StrategieVision.KEYS)

    def __init__(self, **kwargs):
        """
        :param balise: contient des couleurs, si aucune n'est donnée en argument, on en crée une
        """
        keys = kwargs.keys()
        for key in TournerVersBalise.INIT.keys():
            if not key in keys:
                kwargs[key] = TournerVersBalise.INIT[key]
        keys = kwargs.keys()

        StrategieVision.__init__(self, **{key: kwargs[key] for key in StrategieVision.KEYS if key in keys})
        Tourner.__init__(self, **{key: kwargs[key] for key in Tourner.KEYS if key in keys})
        self.balise = kwargs["balise"]
        self.cpt = kwargs["cpt"]
        self.cpt_not_found = kwargs["cpt_not_found"]
        self.cpt_before_picture = int(kwargs["cpt_before_picture"] / PAS_TEMPS)
        self.prev_res = kwargs["prev_res"]
        self.robot.set_wheels_rotation(3, 0)

    def get_angle(self):
        """
        Retourne 1 si la balise est à droite, -1 si elle est à gauche

        Si l'angle formé par le vecteur formé par le milieu bas de l'écran et le centre de la balise
        avec la verticale est supérieur à 5 degrés, la balis est considérée devant le robot
        on retourne alors 0

        Si aucune balise trouvée retourne None
        :return: int
        """
        # print("\nAnalysing image ", self.cpt,"...")
        p = trouver_balise(self.balise.colors, image=self.robot.tete.sensors["cam"].get_image())
        if p is None:
            # print("No target found")
            self.cpt_not_found += 1
            self.cpt += 1
            return None, None
        angle = -(p[0] - 0.5) * Camera.ANGLE_VY / 4
        sens = signe(angle)
        if abs(angle) < TournerVersBalise.PRECISION:
            # print("Target ahead (", angle, " degres from vertical)")
            sens = 0
        self.prev_res = (angle, sens)
        self.cpt += 1

        self.cpt_not_found = 0

        return (angle, sens)

    def update(self):
        res = self.get_angle()
        self.action(res[1], res[0])
        Tourner.update(self)
        self.robot.tete.sensors["cam"].take_picture()

    def action(self, sens, angle):
        res = (angle, sens)
        if res[1] is None:
            Tourner.abort(self)
        elif res[1] == 0:
            Tourner.abort(self)
            self.sens = 0
        else:
            Tourner.init_movement(self, res[0], self.diametre)

    def stop(self):
        if self.sens == 0:
            # print("Target ahead")
            return True
        return False

    def show_last_pic(self):
        self.robot.tete.sensors["cam"].raw_im.show()

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = TournerVersBalise.__name__
        for key in TournerVersBalise.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

    @staticmethod
    def hook(dct):
        res = StrategieVision.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == TournerVersBalise.__name__:
            return TournerVersBalise(**dct)

    def __str__(self):
        return Tourner.__str__(self)+""
    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=TournerVersBalise.hook)


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.geometry import Arene
    st = TournerVersBalise(robot=RobotMotorise(), arene=Arene())
    st.save("TournerVersBalise.json")
    st2 = TournerVersBalise.load("TournerVersBalise.json")
    print(st2.clone())
