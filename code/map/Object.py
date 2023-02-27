import numpy as np
from Entity import Entity
class Object(Entity):
    def __init__(self):
        super().__init__()
        self.radius = 100

    def set_radius(self, radius):
        self.radius = radius
