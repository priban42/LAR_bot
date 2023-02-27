import numpy as np

class Entity:
    def __init__(self):
        self.position = np.array([-100,-100])

    def set_position(self, x, y):
        self.position = np.array([x, y])