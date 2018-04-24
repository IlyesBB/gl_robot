from collections import OrderedDict

from gl_lib.sim.robot.strategy.deplacement.balise import TournerVersBalise
from gl_lib.sim.robot.strategy.deplacement import DeplacementDroitAmeliore, Tourner
from gl_lib.sim.robot.strategy.vision import StrategieVision
from gl_lib.sim.robot import Tete


class DroitVersBalise(TournerVersBalise, DeplacementDroitAmeliore):
    def __init__(self, robot, arene):
        DeplacementDroitAmeliore.__init__(self,robot=robot, distance_max=100, arene=arene)
        TournerVersBalise.__init__(self,robot)
        DroitVersBalise.abort(self)
        self.robot.set_wheels_rotation(3,0)
        self.is_missing = True

    def update(self):
        TournerVersBalise.update(self)
        if self.sens == 0:
            self.is_missing = False
            if not self.advancing:
                DeplacementDroitAmeliore.init_movement(self,100, 100)
            DeplacementDroitAmeliore.update(self)
        elif self.sens is None:
            self.is_missing = True
            try:
                Tourner.init_movement(self, self.prev_res[1] * 30)
            except:
                pass
        else:
            self.is_missing = False
            res = self.robot.tete.lcapteurs["ir"].get_mesure(self.arene, ignore=self.robot)
            if -1 < res < self.proximite_max:
                DroitVersBalise.abort(self)
            self.last_detected = res

    def abort(self):
        TournerVersBalise.abort(self)
        DeplacementDroitAmeliore.abort(self)


    def stop(self):
        try:
            if self.last_detected<self.proximite_max:
                return True
        except:
            pass
        return False



class DroitVersBaliseVision(DroitVersBalise, StrategieVision):
    def __init__(self, robot, arene):
        DroitVersBalise.__init__(self,robot, arene)
        StrategieVision.__init__(self,robot, arene)

    def update(self):
        DroitVersBalise.update(self)
        StrategieVision.update(self)


