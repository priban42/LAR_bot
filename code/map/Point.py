import numpy as np
from Entity import Entity
import math
class Point(Entity):
    def __init__(self, position = np.array([-100, -100])):
        super().__init__(position)
        self.color = "red"
    def __eq__(self, other):
        comparison = self.position == other.position
        return comparison.all()
    def __hash__(self):
        return int(self.position[0] + (10**10)*self.position[1])