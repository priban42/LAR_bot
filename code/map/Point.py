import numpy as np
from Entity import Entity
import math
class Point(Entity):
    def __init__(self, position = np.array([-100, -100])):
        super().__init__(position)