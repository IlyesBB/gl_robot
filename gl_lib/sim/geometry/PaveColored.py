from gl_lib.sim.geometry import Pave, Point

class PaveColored(Pave):
    def __init__(self, width: float or int, length: float or int, height: float or int, centre=Point(0, 0, 0),vertices=None, color=None):
        Pave.__init__(self, width, length, height, centre, vertices)
        self.color=color
        if color is None:
            self.color=(255,255,255,255)

    def color(self):
        return self.color

    def clone(self):
        return PaveColored(self.width, self.length, self.height, self.centre, self.vertices, self.color)
