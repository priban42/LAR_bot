import numpy as np
from .Object import Object
from .Line_segment import Line_segment
from .Point import Point
from .graph import Graph
from .algorithm import find_path


class Map:
    def __init__(self):
        self.objects = set() # every object is unique. This set is only accessed direcly from self.add_object().
        self.points = dict() # every point is unique. This set is only accessed direcly from self.add_point().
        self.line_segments = set() # every point is unique. This set is only accessed direcly from self.add_line_segment().
        self.path = []
        self.centre = [450, 250]  # offset pro vizualizaci (posule levy horni roh do stredu)
        self.graph = Graph()

    def find_path(self, A, B):
        self.path = find_path(self.graph, A, B).nodes
        return self.path

    def add_object(self, x, y, r):
        new_object = Object()
        new_object.set_position(x, y)
        new_object.set_radius(r)
        self.objects.add(new_object)
        return object

    def add_line_segment(self, line_segment):
        self.line_segments.add(line_segment)
        self.graph.add_edge(line_segment.A, line_segment.B, line_segment.get_length())
        self.graph.add_edge(line_segment.B, line_segment.A, line_segment.get_length())

    def add_points_from_objects(self):
        """
        takes all objects in map and generates points accordingly.
        (makes 2 points for each par of objects in between)
        """
        list_of_objects = list(self.objects)
        for a in range(len(list_of_objects)):
            for b in range(a + 1, len(list_of_objects)):
                position_a, position_b = list_of_objects[a].get_adjecent_points(list_of_objects[b])
                self.add_point_from_position(position_a)
                self.add_point_from_position(position_b)

    def add_points_in_grid(self, centre: np.array = np.array([0, 0])) -> None:
        """
        Generates points in a square with the centre in 'centre'. Too many points might result in way too long calculations when generating Line_segments.
        (End of the universe kind of long)
        :param centre:
        """
        size = 3 # in meters
        density = 2# in points per meter

        for x in range(int(size*density)):
            for y in range(int(size*density)):
                position = np.array([(x/density) - size/2, (y/density) - size/2])
                self.add_point_from_position(centre + position)

    def add_point_from_position(self, position: np.array) -> Point:
        """
        Generates a new point from position and inserts it into map.
        :param position: np.array([y, x])
        :return:
        """

        new_point = Point(position)
        if new_point.__hash__() in self.points:
            return self.points[new_point.__hash__()]
        else:
            self.add_point(new_point)
        return new_point

    def add_point(self, point: Point) -> None:
        """
        Adds a point to map.
        :param point:
        """
        self.points[point.__hash__()]=point

    def add_line_segment_from_positions(self, start: np.array, end: np.array) -> Line_segment:
        """
        Generates 2 new points from positions and a Line_segment between them.
        :param start: np.array([y, x])
        :param end:np.array([y, x])
        :return:
        """
        new_pointA = Point(start)
        new_pointB = Point(end)
        new_line_segment = Line_segment(new_pointA, new_pointB)
        if not self.intersects_any(new_line_segment):
            self.add_point(new_pointA)
            self.add_point(new_pointB)
            self.add_line_segment(new_line_segment)
            return new_line_segment
        return False

    def add_line_segment_from_points(self, A: Point, B: Point) -> Line_segment:
        """
        Generates a line segment from 2 points.
        :param A:
        :param B:
        :return:
        """
        self.add_point(A)
        self.add_point(B)
        new_line_segment = Line_segment(A, B)
        if not self.intersects_any(new_line_segment):
            self.add_line_segment(new_line_segment)
            return new_line_segment

    def add_all_possible_line_segments(self):
        """
        Generates a Line_segment for each pair of points (if possible).
        """
        points = list(self.points.values())
        for a in range(len(points)):
            for b in range(a + 1, len(points)):
                self.add_line_segment_from_points(points[a], points[b])

    def intersects_any(self, line_segment: Line_segment) -> bool:
        """
        Checks for each object on map weather it is intersected by 'line_segment'.
        :param line_segment:
        :return: False if no intersection occurs.
        """
        for object in self.objects:
            if object.line_segment_intersects_circle(line_segment):
                return True
        return False
