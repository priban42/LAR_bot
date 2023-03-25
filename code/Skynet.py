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

    def reset_map(self):
        self.map = Map()
        self.vizualize.set_map(self.map)

    def update_vision(self):
        """
        TODO: make it so that it gets the image from camera. preferably implemented in the vlass Computer_vision.
        """
        point_cloud = np.load("computer_vision/cloud2.npy", allow_pickle=True)
        color_picture = np.load("computer_vision/color2.npy", allow_pickle=True)
        #self.robot._turtle.wait_for_point_cloud()
        #point_cloud = self.robot._turtle.get_point_cloud()
        #self.robot._turtle.wait_for_rgb_image()
        #color_picture = self.robot._turtle.get_rgb_image()

        arnold.vision.update_image(color_picture, point_cloud)
        arnold.vision.display_contours("purple", "red", "green", "blue", "yellow")
        #arnold.vision.display_pc_img()

    def locate(self):
        self.update_vision()
        objects = self.vision.get_list_of_objects()
        print(objects)
        for object in objects:
            color = object[0]
            if color == "purple":
                print(object)
            relative_position = object[1]
            absolute_position = self.robot.relative_to_absolute_position(relative_position)
            if color == "purple":
                self.map.add_object(absolute_position[0], absolute_position[1], 0.1, color=color)
            else:
                #self.map.add_object(absolute_position[0], absolute_position[1], 0.2065, color=color)
                self.map.add_object(absolute_position[0], absolute_position[1], 0.25, color=color)
        point = self.map.add_point_from_position(self.robot.position)
        self.map.start_point = point

        self.map.add_points_from_objects()
        self.map.add_points_in_grid(self.robot.position)
        self.map.add_all_possible_line_segments()
        self.map.find_path()


    def follow_path(self, steps_to_follow):
        path = self.map.find_path()
        for p in path:
            print(p)
        self.robot.move_along_path(path[1:steps_to_follow + 1])

if __name__ == "__main__":
    arnold = Skynet()
    arnold.reset_map()
    arnold.locate()
    try:
        arnold.vizualize.draw(True)
    except:
        pass
    #arnold.follow_path(3)