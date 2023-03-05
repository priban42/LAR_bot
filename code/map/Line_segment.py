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
