from gl_lib.sim.robot.display.d2 import view, gui
from gl_lib.sim.robot import RobotPhysique
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.strategy.deplacement import DeplacementSimpleAmeliore
from gl_lib.sim.robot import sensor

r=RobotPhysique(Pave(50,50,0), direction=Vecteur(0,-1,0))
r.tete.vitesseRot=0.3
a=Arene()
r.tete.add_sensors(ir=sensor.CapteurIR(tete=r.tete, portee=200))
r.stratDeplacement=DeplacementSimpleAmeliore(r, a)
p=Pave(50,50,0)
p.move(Vecteur(200, 200, 0))
a.add(p)
a.add(r)

app=gui.AppRobotAutonome(r, view.Vue2DArene(a))
app.init()

app.mainloop()
