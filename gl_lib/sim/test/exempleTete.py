from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
from math import pi

t=Tete(r)
t.addsensor(sensor.CapteurIR(point.Point(0, 0, 0), point.Vecteur(1, 0, 0)))

a=Arene()
p=Pave(25,25,0)
p2=Pave(25,25,0)
p.move(point.Vecteur(50, 0, 0))
p2.move(point.Vecteur(-50, 0, 0))
a.add(p)

res=t.lcapteurs[Tete.IR].mesure(a)
print(res[0])

t.turn(pi)
res=t.lcapteurs[Tete.IR].mesure(a)
print(res[0])
