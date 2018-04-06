from gl_lib.sim.robot import *
from gl_lib.sim.geometry.point import *
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.strategy.deplacement import *
from math import pi

a = Arene()
r = RobotAutonome(Pave(50,50,0), Objet3D(), Objet3D(), Vecteur(0,-1,0))
r.stratDeplacement=DeplacementSimple(r)
r.vitesse=2.0
r.vitesseRot=pi/100

a.add(r)

dest=Point(300, 300, 0)
print(dest.to_vect().get_angle())
r.deplacer_vers(dest)

while not r.destination is None:
    r.update()
    print(r.direction.get_angle())
    print(r)
    
    