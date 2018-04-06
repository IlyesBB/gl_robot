from gl_lib.sim.display.d2.gui import AppRobotAutonome
from gl_lib.sim.robot.RobotAutonome import RobotAutonome
from gl_lib.sim.display.d2.view import Vue2DArene
from gl_lib.sim.geometry.point import Vecteur
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.strategy.deplacement import DeplacementSimple

r=RobotAutonome(Pave(1,1,0, centre=point.Point(2,2,0)), Objet3D(), Objet3D(), Vecteur(0,-1,0))
r.stratDeplacement=DeplacementSimple(r)
a=Arene()
a.add(r)

app=AppRobotAutonome(r, Vue2DArene(a))
app.init() 

app.mainloop()

