from computer_vision.Computer_vision import Computer_vision
from movement.Test_Robot import Robot# Change before runnign on turtle bot!!!!!!!!!
#from movement.Robot import Robot# to this
from map.Vizualize import Vizualize
from map import Map
import numpy as np
import cv2

class Skynet:
    def __init__(self):
        self.robot = Robot()
        self.map = Map()
        self.vision = Computer_vision()
        self.vizualize = Vizualize()
        self.vizualize.set_map(self.map)
        self.vizualize.set_robot(self.robot)


    def update_vision(self):
        """
        TODO: make it so that it gets the image from camera. preferably implemented in the vlass Computer_vision.
        """
        cloud = np.load("computer_vision/cloud2.npy", allow_pickle=True)
        color_img = np.load("computer_vision/color2.npy", allow_pickle=True)
        arnold.vision.update_image(color_img, cloud)
    def locate(self):
        self.update_vision()
        objects = self.vision.get_list_of_objects()
        for object in objects:
            color = object[0]
            relative_position = object[1]
            absolute_position = self.robot.relative_to_absolute_position(relative_position)
            self.map.add_object(absolute_position[0], absolute_position[1], 0.1, color=color)


if __name__ == "__main__":
    arnold = Skynet()
    arnold.update_vision()
    arnold.locate()
    arnold.vizualize.draw()
    pass