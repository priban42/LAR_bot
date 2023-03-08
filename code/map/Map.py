import numpy as np
from Object import Object
from Line_segment import Line_segment
from Point import Point
from dijkstar import Graph, find_path
import tkinter as tk

class Map:
    def __init__(self):
        self.objects = []
        self.points = []
        self.line_segments = []
        self.centre = [450, 250]#offset pro vizualizaci (posule levy horni roh do stredu)
        self.graph = Graph()
    def find_path(self, A, B):
        return find_path(self.graph, A, B)

    def add_object(self, x, y, r):
        new_object = Object()
        new_object.set_position(x, y)
        new_object.set_radius(r)
        self.objects.append(new_object)
        return object

    def add_line_segment(self, line_segment):
        self.line_segments.append(line_segment)
        self.graph.add_edge(line_segment.A, line_segment.B, line_segment.get_length())

    def add_point_from_position(self, position):
        new_point = Point(position)
        self.add_point(new_point)
        return new_point

    def add_point(self, point):
        self.points.append(point)

    def add_line_segment_from_positions(self, start, end):
        new_pointA = Point(start)
        new_pointB = Point(end)
        new_line_segment = Line_segment(new_pointA, new_pointB)
        if not self.intersects_any(new_line_segment):
            self.add_point(new_pointA)
            self.add_point(new_pointB)
            self.add_line_segment(new_line_segment)
            return new_line_segment
        return False

    def add_line_segmetn_from_points(self, A, B):
        new_line_segment = Line_segment(A, B)
        if not self.intersects_any(new_line_segment):
            self.add_line_segment(new_line_segment)
            return new_line_segment

    def intersects_any(self, line_segment):
        for object in self.objects:
            if object.line_segment_intersects_circle(line_segment):
                return True
        return False
