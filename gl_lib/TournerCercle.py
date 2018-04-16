from gl_lib.sim.robot.strategy.deplacement import Tourner, DeplacementCercle

class TournerCercle(DeplacementCercle):
    def __init__(self, robot, angle_max=90, diametre=1, average_dps=30):
        DeplacementCercle.__init__(self, robot, diametre, average_dps)
        self.angle_max = angle_max

    def init_movement(self,diametre_cercle, angle_max, dps_moy=30):
        DeplacementCercle.init_movement(self, diametre_cercle, dps_moy)


