import numpy as np
from Object import Object
from Line_segment import Line_segment
from Point import Point

class Map:
    def __init__(self):
        self.objects = []
        self.points = []
        self.line_segments = []
        self.centre = [450, 250]#offset pro vizualizaci (posule levy horni roh do stredu)

    def draw_object(self, canvas, object):
        canvas.create_oval(object.position[0] + self.centre[0] - object.radius,
                                  object.position[1] + self.centre[1] - object.radius,
                                  object.position[0] + self.centre[0] + object.radius,
                                  object.position[1] + self.centre[1] + object.radius, outline = object.color)
        canvas.create_oval(object.position[0] + self.centre[0] - 3,
                                  object.position[1] + self.centre[1] - 3,
                                  object.position[0] + self.centre[0] + 3,
                                  object.position[1] + self.centre[1] + 3, fill = object.color)

    def draw_point(self, canvas, point):
        canvas.create_oval(point.position[0] + self.centre[0] - 3,
                                  point.position[1] + self.centre[1] - 3,
                                  point.position[0] + self.centre[0] + 3,
                                  point.position[1] + self.centre[1] + 3, fill = point.color)

    def draw_line_segment(self, canvas, line_segment):
        canvas.create_line(line_segment.A.position[0] + self.centre[0],
                           line_segment.A.position[1] + self.centre[1],
                           line_segment.B.position[0] + self.centre[0],
                           line_segment.B.position[1] + self.centre[1],
                           fill=line_segment.color, width=5)


    def draw(self, canvas):
        for object in self.objects:
            self.draw_object(canvas, object)
        for line_segment in self.line_segments:
            self.draw_line_segment(canvas, line_segment)
        for point in self.points:
            self.draw_point(canvas, point)

    def add_object(self, x, y, r):
        new_object = Object()
        new_object.set_position(x, y)
        new_object.set_radius(r)
        self.objects.append(new_object)

    def add_line_segment(self, point_start, point_end):
        self.line_segments.append(Line_segment(point_start, point_end))

    def add_point(self, position = [-100, -100]):
        new_point = Point(position)
        self.points.append(new_point)

    def add_line_segment_from_positions(self, start, end):
        new_pointA = Point(start)
        new_pointB = Point(end)
        new_line_segment = Line_segment(new_pointA, new_pointB)
        # v budoucnu vubec tento line segment nepridavat pokud neco protina
        if self.intersects_any(new_line_segment):
            new_line_segment.color = "red"
        self.points.append(new_pointA)
        self.points.append(new_pointB)
        self.line_segments.append(new_line_segment)

    def intersects_any(self, line_segment):
        for object in self.objects:
            if object.line_segment_intersects_circle(line_segment):
                return True
        return False
