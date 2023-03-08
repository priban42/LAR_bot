import numpy as np

class Entity:
    def __init__(self, position):
        self.position = np.array(position, dtype=np.float32)
        self.color = "grey"
    def set_position(self, x, y):
        self.position = np.array([x, y])
