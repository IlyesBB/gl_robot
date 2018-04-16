import sys
sys.path.insert(0, "/Users/Macbook pro/PycharmProjects/GurrenLagann-dev")

from gl_lib.sim.robot.display.d2.gui import AppRobot
from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from gl_lib.sim.robot.display.d2.view import *

"""
Creation et display d'un robot basique avec modulateurs de vitesses pour tester
"""

rt=Robot(Pave(1,1,0),Objet3D(),Objet3D(), Vecteur(0,-1,0))

rt.move(Vecteur(2, 1, 0))
a=Arene()
a.add(rt)

app=AppRobot(rt, Vue2DArene(a))
app.init()
app.mainloop()
