class Strategie(object):
    """
    definit une strategy de robot de facon abstraite
    """
    def __init__(self, robot):
        """
        robot : Robot
        """
        self.robot = robot

    def stop(self):
        return False

    def update(self):
        self.robot.update()

