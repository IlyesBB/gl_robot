# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.config import PAS_TEMPS
from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot.strategy.deplacement.balise import TournerVersBalise
from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore, Tourner
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import Tete, RobotMotorise


class DroitVersBalise(TournerVersBalise, DeplacementDroitAmeliore):
    """
        Permet au robot de foncer droit vers une balise dès qu'il l'a détecté et qu'il s'est mis dans la bonne direction
        Il s'arrête si il y à un obstacle sur sa route
    """

    def __init__(self, **kwargs):
        """
            Initialise la stratégie

            L'initialisation est semblable aux classes dont hérite DroitVersBalise
        """
        keys = kwargs.keys()
        DeplacementDroitAmeliore.__init__(self,
                                          **{key: kwargs[key] for key in DeplacementDroitAmeliore.KEYS if key in keys})
        TournerVersBalise.__init__(self, **{key: kwargs[key] for key in TournerVersBalise.KEYS if key in keys})
        DroitVersBalise.reset(self)
        self.robot.tete.attach(self.robot.centre, self.robot.direction)
        self.robot.set_wheels_rotation(3, 0)
        self.searching = True
        self.cpt_t = 0

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DroitVersBalise.__name__
        for key in DroitVersBalise.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

    def __str__(self):
        s1 = TournerVersBalise.__str__(self)
        l = s1.split("\n")
        return DeplacementDroitAmeliore.__str__(self)+"\n"+l[len(l)-1]

    def update(self):
        """
            Si une balise est en vue, enclenche les actions pour s'en rapprocher et actualise la stratégie
        """
        self.robot.update()
        if not self.searching:
            return
        TournerVersBalise.update(self)
        if self.sens == 0:
            if not self.advancing:
                DeplacementDroitAmeliore.init_movement(self, 100, 100)
            DeplacementDroitAmeliore.update(self)
            if not self.advancing:
                DroitVersBalise.reset(self)
                self.robot.set_wheels_rotation(3,0)
        elif self.sens is None:
            if self.cpt_t*PAS_TEMPS > 1:
                # Si on ne trouve pas la balise au bout de 1 s, on arrête tout mouvement
                DroitVersBalise.reset(self)
                self.robot.set_wheels_rotation(3,0)
        else:
            if self.advancing:
                DeplacementDroitAmeliore.reset(self)
            res = self.robot.tete.sensors["ir"].get_mesure(self.arene, ignore=self.robot, direction=self.robot.direction)
            if -1 < res < self.proximite_max:
                DroitVersBalise.reset(self)
                self.robot.set_wheels_rotation(3,0)
            self.last_detected = res
        self.cpt_t += 1

    def abort(self):
        """
            Désactive la mise à jour
        """
        self.searching = False
        TournerVersBalise.abort(self)
        DeplacementDroitAmeliore.abort(self)

    def reset(self):
        """
            Désactive la mise à jour, réinitialise les variables du mouvement
        """
        TournerVersBalise.reset(self)
        DeplacementDroitAmeliore.reset(self)

    def stop(self):
        """
            Ne renvoie True que si un obstacle est à proximité du robot
        """
        try:
            if self.last_detected < self.proximite_max:
                return True
        except:
            pass
        return False

    @staticmethod
    def hook(dct):
        res = TournerVersBalise.hook(dct)
        res = DeplacementDroitAmeliore.hook(dct) if res is None else res
        if res is not None:
            return res

        elif dct["__class__"] == DroitVersBalise.__name__:
            return DroitVersBalise(**dct)

    @staticmethod
    def load(filename):
        """
            Permet de charger un objet DroitVersbalise depuis un fichier au format json adapté

        :param filename: Nom du fichier

        """
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DroitVersBalise.hook)


class DroitVersBaliseVision(DroitVersBalise, StrategieVision):
    def __init__(self, robot, arene):
        DroitVersBalise.__init__(self, robot=robot, arene=arene)
        StrategieVision.__init__(self, robot=robot, arene=arene)

    def update(self):
        DroitVersBalise.update(self)


if __name__=='__main__':
    st = DroitVersBalise(robot=RobotMotorise(), arene=Arene())

    st.save("droitVersBalise.json")

    st2 = DroitVersBalise.load("droitVersBalise.json")

    print(st2.clone())