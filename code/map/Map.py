import numpy as np
from Object import Object
class Map:
    def __init__(self):
        self.objects = []

    def draw_object(self, canvas, object):
        canvas.create_oval(object.position[0] - object.radius,
                                  object.position[1] - object.radius,
                                  object.position[0] + object.radius,
                                  object.position[1] + object.radius)
        canvas.create_oval(object.position[0] - 3,
                                  object.position[1] - 3,
                                  object.position[0] + 3,
                                  object.position[1] + 3, fill = "black")
    def draw_objects(self, canvas):
        for object in self.objects:
            self.draw_object(canvas, object)
    def add_object(self, x, y):
        new_object = Object()
        new_object.set_position(x, y)
        self.objects.append(new_object)