from gl_lib.sim.geometry import Pave
from gl_lib.sim.geometry.point import Point

class PaveColored(Pave):
    def __init__(self, width: float or int, length: float or int, height: float or int, centre=Point(0, 0, 0), color=None):
        Pave.__init__(self, width, length, height, centre)
        self.color=color
        if color is None:
            self.color=(255,255,255,255)

    def color(self):
        return self.color
