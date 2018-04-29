# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot.sensor import Camera
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot.sensor.camera import Balise
from gl_lib.sim.robot.strategy.analyse.image import trouver_balise
from gl_lib.sim.robot.strategy.deplacement import Tourner
from gl_lib.config import DT_SCREENSHOT, PAS_TEMPS
from gl_lib.sim.geometry import signe


class TournerVersBalise(Tourner, StrategieVision):
    """
        Stratégie qui permet de tourner le robot robot vers une balise devant lui, si elle est visible

        Nécessite le lancement de l'application pyglet de la caméra du robot (de gl_lib.sim.robot.sensor.camera.Camera)
    """
    # Précision en degrés avec laquelle on considère que la balise est devant
    PRECISION = 5
    INIT = dict(prev_res=None, balise=Balise(), cpt=0, cpt_before_picture=DT_SCREENSHOT, cpt_not_found=0)
    KEYS = set(Tourner.KEYS + ["prev_res", "balise", "cpt", "cpt_before_picture", "cpt_not_found"] + StrategieVision.KEYS)

    def __init__(self, **kwargs):
        """
        :param balise: Balise à chercher dans les images. Si aucune donnée en argument, on en crée une par défaut
        :type balise: Balise
        """
        keys = kwargs.keys()
        for key in TournerVersBalise.INIT.keys():
            if not key in keys:
                kwargs[key] = TournerVersBalise.INIT[key]
        keys = kwargs.keys()

        StrategieVision.__init__(self, **{key: kwargs[key] for key in StrategieVision.KEYS if key in keys})
        Tourner.__init__(self, **{key: kwargs[key] for key in Tourner.KEYS if key in keys})
        # Balise à chercher
        self.balise = kwargs["balise"]
        # Compteur d'image analysées
        self.cpt = kwargs["cpt"]
        # Compteur d'images dont l'analyse n'a pas été concluante
        self.cpt_not_found = kwargs["cpt_not_found"]
        # Temps de latence avant laquelle prendre analyser l'image
        self.cpt_before_picture = int(kwargs["cpt_before_picture"] / PAS_TEMPS)
        # Dernier résultat obtenu lors de l'anayse de l'image
        self.prev_res = kwargs["prev_res"]
        self.robot.set_wheels_rotation(3, 0)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = TournerVersBalise.__name__
        for key in TournerVersBalise.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

    def __str__(self):
        return Tourner.__str__(self)+""

    def get_angle(self):
        """
            Retourne un tuple (angle, sens), indiquant la position de la balise sur la dernière image
            Si aucune balise trouvée retourne None

            Angle:

            Retourne l'angle formé par le vecteur formé par le milieu bas de l'écran et le centre de la balise avec la
            verticale. Si cet angle est inférieur à TournerVersBalise.PRECISION, la balise est considérée devant le
            robot. On retourne alors 0

            Signe:
            Correspond au signe de l'angle

            Si aucune balise trouvée retourne None

        :return: tuple

        """
        # print("\nAnalysing image ", self.cpt,"...")
        p = trouver_balise(self.balise.colors, image=self.robot.tete.sensors["cam"].get_image())
        if p is None:
            # print("No target found")
            self.cpt_not_found += 1
            self.cpt += 1
            return None, None
        angle = -(p[0] - 0.5) * Camera.ANGLE_VY / 4
        # print(angle)
        sens = signe(angle)
        if abs(angle) < TournerVersBalise.PRECISION:
            # print("Target ahead (", angle, " degres from vertical)")
            sens = 0
        self.prev_res = (angle, sens)
        self.cpt += 1

        self.cpt_not_found = 0

        return (angle, sens)

    def update(self):
        """
            Met à jour la stratégie et demande la prise d'une photo à la caméra
        """
        res = self.get_angle()
        self.action(res[1], res[0])
        Tourner.update(self)
        self.robot.tete.sensors["cam"].take_picture()

    def action(self, sens, angle):
        """
            Définit et exécute les actions à réaliser en fonction des résultats de la recherche de la balise

        :param sens: Son signe donne la rotation à effectuer (prise dans le sens trigonométrique)
        :param angle: Angle duquel tourner en radians
        """
        res = (angle, sens)
        if res[1] is None:
            Tourner.abort(self)
        elif res[1] == 0:
            Tourner.abort(self)
            self.sens = 0
        else:
            Tourner.init_movement(self, res[0], self.diametre)

    def reset(self):
        """
            Désactive la mise à jour, et réinitialise l'angle de rotation
        """
        Tourner.abort(self)
        self.rot_angle = 0
        self.angle_max = None


    def stop(self):
        """
            Si on a trouvé une balise devant, on renvoie True
        """
        if self.sens == 0:
            # print("Target ahead")
            return True
        return False

    def show_last_pic(self):
        """
            Permet d'afficher la dernière image analysée par la stratégie
        """
        try:
            self.robot.tete.sensors["cam"].raw_im.show()
        except TypeError:
            # Au cas où aucune image n'a été analysée
            pass

    @staticmethod
    def hook(dct):
        res = StrategieVision.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == TournerVersBalise.__name__:
            return TournerVersBalise(**dct)

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet TournerVersBalise depuis un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=TournerVersBalise.hook)


if __name__ == '__main__':
    from gl_lib.sim.robot import RobotMotorise
    from gl_lib.sim.geometry import Arene, signe

    st = TournerVersBalise(robot=RobotMotorise(), arene=Arene())
    st.save("TournerVersBalise.json")
    st2 = TournerVersBalise.load("TournerVersBalise.json")
    print(st2.clone())
