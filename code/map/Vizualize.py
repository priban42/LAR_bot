import numpy as np
from .Object import Object
from .Map import Map
from .Line_segment import Line_segment
from .Point import Point
from .graph import Graph
from .algorithm import find_path
import tkinter as tk
import random
import sys


class Vizualize():
    def __init__(self):
        self._window = tk.Tk()
        self.width = 600
        self.height = 700
        self.scale = 100
        self.grid_size = 0.5  # size of grid squares in meters
        self.centre = [self.width / 2, self.height / 2]
        self._window.geometry(str(self.width) + "x" + str(self.height))
        self.canvas = tk.Canvas(self._window, width=self.width, height=self.height, bg='light gray')
        self.canvas.pack()
        # self._window.mainloop()
        self.map = None
        self.robot = None

    def set_map(self, map):
        self.map = map

    def set_robot(self, robot):
        self.robot = robot

    def _center_view(self):
        if self.robot != None:
            self.centre = [self.width / 2 + self.robot.position[1] * self.scale,
                           self.height / 2 + self.robot.position[0] * self.scale]
        else:
            self.centre = [self.width / 2, self.height / 2]

    def _draw_object(self, object: Object) -> None:
        """
        draws the object on canvas as a circle with a centre
        :param canvas: tkinter canvas
        :param object:
        """
        self._center_view()
        self.canvas.create_oval(object.position[0] * self.scale + self.centre[0] - object.radius * self.scale,
                                object.position[1] * self.scale + self.centre[1] - object.radius * self.scale,
                                object.position[0] * self.scale + self.centre[0] + object.radius * self.scale,
                                object.position[1] * self.scale + self.centre[1] + object.radius * self.scale,
                                outline=object.color, width=3)
        self.canvas.create_oval(object.position[0] * self.scale + self.centre[0] - 3,
                                object.position[1] * self.scale + self.centre[1] - 3,
                                object.position[0] * self.scale + self.centre[0] + 3,
                                object.position[1] * self.scale + self.centre[1] + 3, fill=object.color)

    def _draw_robot(self, robot):
        if robot == None:
            return
        self._center_view()
        size = 0.2
        self.canvas.create_oval(robot.position[0] * self.scale + self.centre[0] - size * self.scale,
                                robot.position[1] * self.scale + self.centre[1] - size * self.scale,
                                robot.position[0] * self.scale + self.centre[0] + size * self.scale,
                                robot.position[1] * self.scale + self.centre[1] + size * self.scale,
                                outline="green", width=10)

        line_start_x = robot.position[0] * self.scale + self.centre[0]
        line_start_y = robot.position[1] * self.scale + self.centre[1]
        line_end_x = robot.position[0] * self.scale + self.centre[0] + self.robot.direction[0] * size * self.scale
        line_end_y = robot.position[1] * self.scale + self.centre[1] + self.robot.direction[1] * size * self.scale

        self.canvas.create_line(line_start_x, line_start_y, line_end_x, line_end_y, fill="green", width=5)

    def _draw_point(self, point):
        self._center_view()
        self.canvas.create_oval(point.position[0] * self.scale + self.centre[0] - 3,
                                point.position[1] * self.scale + self.centre[1] - 3,
                                point.position[0] * self.scale + self.centre[0] + 3,
                                point.position[1] * self.scale + self.centre[1] + 3, fill=point.color)

    def _draw_line_segment(self, line_segment):
        self._center_view()
        self.canvas.create_line(line_segment.A.position[0] * self.scale + self.centre[0],
                                line_segment.A.position[1] * self.scale + self.centre[1],
                                line_segment.B.position[0] * self.scale + self.centre[0],
                                line_segment.B.position[1] * self.scale + self.centre[1],
                                fill=line_segment.color, width=2)

    def _draw_grid(self):
        color = "grey"
        grid_density = 1 / self.grid_size  # lines per meter
        for i in range(0, int(grid_density * self.width // (2 * self.scale)) + 1):
            self.canvas.create_line(self.width / 2 + i * self.scale / grid_density, 0,
                                    self.width / 2 + i * self.scale / grid_density, self.height, fill=color)
            self.canvas.create_line(self.width / 2 - i * self.scale / grid_density, 0,
                                    self.width / 2 - i * self.scale / grid_density, self.height, fill=color)
        for i in range(0, int(grid_density * self.height / (2 * self.scale)) + 1):
            self.canvas.create_line(0, self.height / 2 + i * self.scale / grid_density, self.width,
                                    self.height / 2 + i * self.scale / grid_density, fill=color)
            self.canvas.create_line(0, self.height / 2 - i * self.scale / grid_density, self.width,
                                    self.height / 2 - i * self.scale / grid_density, fill=color)

    def draw(self):
        self._draw_grid()
        for object in self.map.objects:
            self._draw_object(object)
        for line_segment in self.map.line_segments:
            self._draw_line_segment(line_segment)
        for point in self.map.points.values():
            self._draw_point(point)
        self._draw_robot(self.robot)

        self._window.mainloop()
        self._window.update()
