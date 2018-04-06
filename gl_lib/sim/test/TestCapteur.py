from gl_lib.sim.robot.sensor import CapteurIR
from gl_lib.sim.robot import *
from gl_lib.sim.geometry import *
import math

a = Arene()
a.high = 100
a.width = 100
p = Pave(20, 20, 10)
p.rotate(math.pi / 3)
a.add(p)
r = RobotPhysique(Pave(1, 1, 0))
r.tete.turn(math.pi)
r.move(point.Vecteur(20, 20, 0))
t = Tete(r)
t.direction = point.Vecteur(-1 , -2 , 0)
c = CapteurIR(t )

res = c.mesure(a)
print(res[0])
for l in res[1]:
    for c in l:
        print(c, end=' ')
    print('\n')
print(r.tete.lcapteurs)
