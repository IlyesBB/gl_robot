# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.robot.strategy import Strategie
from gl_lib.sim.robot import AreneRobot, RobotMotorise
from threading import RLock

class StrategieVision(Strategie):
    """
        Classe qui facilite l'utilisation de la caméra du robot
    """
    ARGS = ["arene"]
    KEYS = Strategie.KEYS + ["arene"]
    INIT = {"arene":None}
    def __init__(self, robot:RobotMotorise, arene):
        Strategie.__init__(self, robot)
        self.arene=arene
        self.robot.tete.sensors["cam"].arene=arene

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = StrategieVision.__name__
        dct["robot"] = self.robot.__dict__()
        dct["arene"] = self.arene.__dict__()

        return dct


    def start_3D(self):
        """
            Lance l'application de la caméra

            A lancer dans un thread
        """
        try:
            self.robot.tete.sensors["cam"].run()
        except RuntimeError:
            # Si l'affichage est perturbé par la simulation
            pass
    def stop_3D(self):
        """
            Ferme la fenêtre
        """
        self.robot.tete.sensors["cam"].stop()

    def print_screen(self, filename):
        """
            Lance la caméra, et enregistre la première image capturée dans un fichier

        :param filename: Nom du fichier

        """
        self.robot.tete.sensors["cam"].get_picture()
        while not self.robot.tete.sensors["cam"].is_set:
            pass
        self.robot.tete.sensors["cam"].picture()
        self.robot.tete.sensors["cam"].print_picture(filename)

    @staticmethod
    def hook(dct):
        res = AreneRobot.hook(dct)
        if res is not None:
            return res
        elif dct["__class__"] == StrategieVision.__name__:
            return StrategieVision(dct["robot"], dct["arene"])

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet StrategieVision depuis un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=StrategieVision.hook)

if __name__=='__main__':
    st = StrategieVision(RobotMotorise(), AreneRobot())

    st.save("strategie_vision.json")
    print(st)

    st2 = StrategieVision.load("strategie_vision.json")
