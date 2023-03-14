import numpy as np
from Point import Point
import math


class Line_segment():
    def __init__(self, point1, point2):
        self.A = point1
        self.B = point2
        self.color = "black"

    def get_length(self):
        dist = np.linalg.norm(self.A.position - self.B.position)
        return dist

    def __eq__(self, other: 'Object') -> bool:
        return (self.A == other.A and self.B == other.B) or (self.A == other.B and self.B == other.A)

    def __hash__(self):
        return int(self.A.position[0] + 2*(10 ** 5) * self.A.position[1] +
                   2*(10 ** 10)*self.B.position[0] + 2*(10 ** 15) * self.B.position[1])
