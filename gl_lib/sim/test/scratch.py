from gl_lib.sim.display.d2.view import Vue2DArene
from gl_lib.sim.display.d2.gui import AppRobotAutonome
from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.strategy.deplacement import *

r = RobotPhysique(Pave(50, 50, 0), Objet3D(), Objet3D(), point.Vecteur(0, -1, 0))
a = Arene()
r.tete.addsensor(sensor.CapteurIR(r.tete))
r.stratDeplacement = DeplacementSimpleAmeliore(r, a)
r.move(point.Vecteur(150, 150, 0))
p = Pave(50, 50, 0)
p.move(point.Vecteur(200, 200, 0))
a.add(r)
a.add(p)

app = AppRobotAutonome(r, Vue2DArene(a))
app.init()

app.mainloop()
