# -*- coding: utf-8 -*-
import json
from collections import OrderedDict

from gl_lib.sim.geometry import Arene
from gl_lib.sim.robot.strategy.deplacement.balise import TournerVersBalise
from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore, Tourner
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import Tete, RobotMotorise


class DroitVersBalise(TournerVersBalise, DeplacementDroitAmeliore):
    """Cherche une balise visible
    S'il y en à une, tourne le robot dans sa direction, puis avancejusqu'à atteindre un obstacle
    """

    def __init__(self, **kwargs):
        keys = kwargs.keys()
        DeplacementDroitAmeliore.__init__(self,
                                          **{key: kwargs[key] for key in DeplacementDroitAmeliore.KEYS if key in keys})
        TournerVersBalise.__init__(self, **{key: kwargs[key] for key in TournerVersBalise.KEYS if key in keys})
        DroitVersBalise.abort(self)
        self.robot.set_wheels_rotation(3, 0)

    def __dict__(self):
        dct = OrderedDict()
        dct["__class__"] = DroitVersBalise.__name__
        for key in DroitVersBalise.KEYS:
            try:
                dct[key] = self.__getattribute__(key).__dict__()
            except:
                dct[key] = self.__getattribute__(key)
        return dct

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
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f, object_hook=DroitVersBalise.hook)

    def update(self):
        TournerVersBalise.update(self)
        if self.sens == 0:
            if not self.advancing:
                DeplacementDroitAmeliore.init_movement(self, 100, 100)
            DeplacementDroitAmeliore.update(self)
        elif self.sens is None:
            try:
                Tourner.init_movement(self, self.prev_res[1] * 30)
            except:
                pass
        else:
            res = self.robot.tete.lcapteurs["ir"].get_mesure(self.arene, ignore=self.robot)
            if -1 < res < self.proximite_max:
                DroitVersBalise.abort(self)
            self.last_detected = res

    def abort(self):
        TournerVersBalise.abort(self)
        DeplacementDroitAmeliore.abort(self)

    def stop(self):
        try:
            if self.last_detected < self.proximite_max:
                return True
        except:
            pass
        return False

    def __str__(self):
        s1 = TournerVersBalise.__str__(self)
        l = s1.split("\n")
        return DeplacementDroitAmeliore.__str__(self)+"\n"+l[len(l)-1]

class DroitVersBaliseVision(DroitVersBalise, StrategieVision):
    def __init__(self, robot, arene):
        DroitVersBalise.__init__(self, robot=robot, arene=arene)
        StrategieVision.__init__(self, robot=robot, arene=arene)

    def update(self):
        DroitVersBalise.update(self)
        StrategieVision.update(self)


if __name__=='__main__':
    st = DroitVersBalise(robot=RobotMotorise(), arene=Arene())

    st.save("droitVersBalise.json")

    st2 = DroitVersBalise.load("droitVersBalise.json")

    print(st2.clone())