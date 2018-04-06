from gl_lib.sim.robot.strategy.deplacement.StrategieDeplacement import StrategieDeplacement
from gl_lib.sim.robot import *

class DeplacementSimple(StrategieDeplacement):
    def __init__(self, robot):
        """
        initialisation avec la classe mere
        """
        StrategieDeplacement.__init__(self, robot)
        
    def deplacement_vers(self, destination):
        """
        le robot excute un mouvement de rotation, puis avance vers la destination
        """
        v=(destination-self.robot.forme.centre).to_vect()
        distance=v.get_mag()
        diffAngle=v.diff_angle(self.robot.direction)
        if distance>25:
            if abs(diffAngle)>self.robot.vitesseRot:
                self.robot.turn(diffAngle)
            else :
                self.robot.move_forward(1)
                v2=(destination-self.robot.forme.centre).to_vect()
                if v2.get_mag()-distance>0:
                    self.robot.destination=None
            
        else:
            self.robot.destination=None
            

