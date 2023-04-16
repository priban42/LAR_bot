import numpy as np
from .Entity import Entity
import math


class Point(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.color = "red"
        self.final = False

    def __eq__(self, other: 'Point') -> bool:
        comparison = self.position == other.position
        return comparison.all()

    def __str__(self):
        return  f'[Point: {self.color}, [{self.position[0]:.2f}, {self.position[1]:.2f}]]'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.position[0], self.position[1]))
