import random

import numpy as np
from .Object import Object
from .Line_segment import Line_segment
from .Point import Point
from .graph import Graph
from .algorithm import find_path


class Map:
    COLORS = ["blue", "green", "yellow", "purple", "red", "grey"]
    def __init__(self):
        #self.objects = set() # every object is unique. This set is only accessed direcly from self.add_object().
        self.objects = {"red": dict(), "blue": dict(), "green": dict(), "purple": dict(), "yellow": dict(), "grey": dict()}
        self.points = dict()  # every point is unique. This set is only accessed direcly from self.add_point().
        self.line_segments = set()  # every point is unique. This set is only accessed direcly from self.add_line_segment().
        self.path = []
        self.centre = [450, 250]  # offset pro vizualizaci (posule levy horni roh do stredu)
        self.graph = Graph()
        self.start_point = None
        self.final_point = None
        self.point_of_interest = None
        self.quality = 10  # based on how the value of objects detected. the lower the better.
        self.path_extension = []
        self.GARAGE_DEPTH = 0.22  # in meters
        self.GARAGE_CLEARANCE = 2  # in meters
        self.robot = None

    def find_path_old(self, A, B):
        self.path = find_path(self.graph, A, B).nodes + self.path_extension
        return self.path

    def find_path(self):
        try:
            self.path = find_path(self.graph, self.start_point, self.final_point).nodes + self.path_extension
            return True
        except:
            return False

    def path_exists(self, point):
        try:
            self.path = find_path(self.graph, self.start_point, point).nodes
            return True
        except:
            return False
    def add_object_from_position(self, x, y, r, color):
        new_object = Object()
        new_object.set_position(x, y)
        new_object.radius = r
        new_object.color = color
        self.add_object(new_object)
        return object

    def get_list_of_objects(self, whitelist_colors = [], blacklist_colors = []):
        """
        this function is meant to make working with groups of object easier.
        :param whitelist_colors: list of strings naming colors. for ex. ["red", "blue"...]. Has priority over blacklist
        :param blacklist_colors: list of strings naming colors. for ex. ["red", "blue"...].
        :return: list of objects with colors according to white/blacklist.
        """
        list_of_objects = []
        if len(whitelist_colors) > 0:
            for color in whitelist_colors:
                list_of_objects += list(self.objects[color].values())
        else:
            for color in Map.COLORS:
                if color not in blacklist_colors:
                    list_of_objects += list(self.objects[color].values())
        return list_of_objects

    def add_object(self, object):
        self.objects[object.color][object.__hash__()] = object

    def add_line_segment(self, line_segment):
        self.line_segments.add(line_segment)
        self.graph.add_edge(line_segment.A, line_segment.B, line_segment.get_length())
        self.graph.add_edge(line_segment.B, line_segment.A, line_segment.get_length())

    def add_points_from_objects(self):
        """
        takes all objects in map and generates points accordingly.
        (makes 2 points for each par of objects in between)
        """
        list_of_objects = self.get_list_of_objects(whitelist_colors=["red", "green", "blue"])

        for a in range(len(list_of_objects)):
            for b in range(a + 1, len(list_of_objects)):
                position_a, position_b = list_of_objects[a].get_adjecent_points(list_of_objects[b])
                pa = self.add_point_from_position(position_a)
                pb = self.add_point_from_position(position_b)
        self.find_purple_gate()

    def find_purple_gate(self):
        """
        if 2 purple objects are present in map,
         this function finds a point in front of them such,
          that the purple gate is stull visible for the robot from that point.
        """
        purple_objects = self.get_list_of_objects(whitelist_colors=["purple"])
        if len(purple_objects) == 2:
            position_a, position_b = purple_objects[0].get_adjecent_points(purple_objects[1], self.GARAGE_CLEARANCE)
            if np.linalg.norm(position_a - self.start_point.position) > np.linalg.norm(position_b - self.start_point.position):
                closer_adjacent_position = position_b
                farther_adjacent_position = position_a
            else:
                closer_adjacent_position = position_a
                farther_adjacent_position = position_b
            self.final_point = self.add_point_from_position(closer_adjacent_position)
            self.final_point.final = True
            extension_position_vect = (farther_adjacent_position - closer_adjacent_position)
            extension_position = (closer_adjacent_position + farther_adjacent_position)/2 + self.GARAGE_DEPTH*extension_position_vect/np.linalg.norm(extension_position_vect)
            self.path_extension = [self.add_point_from_position(extension_position)]
            return True
        return False

    def find_point_of_interest(self):
        """
        A heurestic function meant fo find a point near the final destination.
        """
        purple_objects = self.get_list_of_objects(whitelist_colors=["purple"])
        yellow_objects = self.get_list_of_objects(whitelist_colors=["yellow"])
        color_objects = self.get_list_of_objects(blacklist_colors=["grey"])
        if len(purple_objects) == 2:
            self.point_of_interest = self.add_point_from_position((purple_objects[0].position + purple_objects[1].position)/2) # centre of gate
            self.point_of_interest.color = "purple"
            self.quality = 1
        elif len(purple_objects) == 1:
            position = purple_objects[0].position / len(yellow_objects)
            vect = (position - self.robot.position)
            vect = vect / np.linalg.norm(vect)
            vect_right = np.array([-vect[1], vect[0]])
            self.point_of_interest = self.add_point_from_position(self.robot.position - vect*0.4 + vect_right*0.2) # centre of gate
            self.point_of_interest = self.add_point_from_position(purple_objects[0].position)  # centre of gate
            self.point_of_interest.color = "purple"
            self.quality = 2
        elif len(yellow_objects) > 0:
            position_sum = np.array([0, 0], dtype='float64')
            for object in yellow_objects:
                position_sum += object.position
            position = position_sum/len(yellow_objects)
            vect = (position - self.robot.position)
            vect = vect/np.linalg.norm(vect)
            vect_right = np.array([-vect[1], vect[0]])
            print(vect, vect_right)
            self.point_of_interest = self.add_point_from_position(position + 1.0*vect_right + vect*0.5)  # avg yellow position
            self.point_of_interest.color = "yellow"
            self.quality = 3
        elif len(color_objects) > 0:
            position_sum = np.array([0, 0], dtype='float64')
            for object in color_objects:
                position_sum += object.position
            self.point_of_interest = self.add_point_from_position(position_sum/len(color_objects))  # avg yellow position
            self.point_of_interest.color = "cyan2"
            self.quality = 4
        else:
            self.point_of_interest = self.add_point_from_position(np.array([random.randint(-100, 100), random.randint(-100, 100)], dtype='float64'))
            self.point_of_interest.color = "gray26"
            self.quality = 5
            print("random point of interest added")

    def get_sorted_points(self):
        """
        this function returns a list of points sorted by distance from the point of interest
        """
        list_of_points = list(self.points.values())
        list_of_points.sort(key=lambda x: np.linalg.norm(x.position - self.point_of_interest.position))
        return list_of_points

    def add_points_in_grid(self, centre: np.array = np.array([0, 0])) -> None:
        """
        Generates points in a square with the centre in 'centre'. Too many points might result in way too long calculations when generating Line_segments.
        (End of the universe kind of long)
        :param centre:
        """
        size = 5  # in meters
        density = 1  # in points per meter

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
        list_of_objects = self.get_list_of_objects()
        for object in list_of_objects:
            if object.line_segment_intersects_circle(line_segment):
                return True
        return False
