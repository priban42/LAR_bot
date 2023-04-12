import time

from computer_vision.Computer_vision import Computer_vision
from movement.Test_Robot import Robot# Change before runnign on turtle bot!!!!!!!!!
#from movement.Robot import Robot# to this
from map.Vizualize import Vizualize
from map import Map
import os
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
        self.beyond_final_point = False

    def reset_map(self):
        self.map = Map()
        self.vizualize.set_map(self.map)

    def update_vision(self):
        point_cloud = np.load("computer_vision/cloud1.npy", allow_pickle=True)
        color_picture = np.load("computer_vision/color1.npy", allow_pickle=True)
        #self.robot.turtle.wait_for_point_cloud()
        #point_cloud = self.robot.turtle.get_point_cloud()
        #self.robot.turtle.wait_for_rgb_image()
        #color_picture = self.robot.turtle.get_rgb_image()

        self.vision.update_image(color_picture, point_cloud)
        self.vision.display_contours("purple", "red", "green", "blue", "yellow", "grey")
        #self.vision.display_contours("grey")
        #arnold.vision.display_pc_img()

    def locate(self):
        self.update_vision()
        objects = self.vision.get_list_of_objects()
        for object in objects:
            color = object[0]
            relative_position = object[1]
            absolute_position = self.robot.relative_to_absolute_position(relative_position)
            if color == "purple":
                self.map.add_object_from_position(absolute_position[0], absolute_position[1], 0.2, color=color)
            elif color == "yellow":
                self.map.add_object_from_position(absolute_position[0], absolute_position[1], 0.15, color=color)
            elif color == "grey":
                self.map.add_object_from_position(absolute_position[0], absolute_position[1], 0.25, color=color)
            else:
                self.map.add_object_from_position(absolute_position[0], absolute_position[1], 0.35, color=color)
        point = self.map.add_point_from_position(self.robot.position)
        self.map.start_point = point

        self.map.add_points_from_objects()
        self.map.add_points_in_grid(self.robot.position)
        self.map.add_all_possible_line_segments()
        self.map.find_path()
        self.map.find_point_of_interest()


    def follow_path(self, steps_to_follow, max_distance, ending = False):
        path = self.map.find_path()
        print(min(steps_to_follow + 1, len(path)))
        if ending:
            self.beyond_final_point = self.robot.move_along_path(path[2:3], max_distance)
        else:
            self.beyond_final_point = self.robot.move_along_path(path[1:min(steps_to_follow + 1, len(path))], max_distance)

    def wait_to_start(self):
        while self.robot.ACTIVE == False:
            time.sleep(0.1)

def main():
    arnold = Skynet()
    arnold.wait_to_start()
    for a in range(10):
        arnold.reset_map()
        arnold.locate()
        try:
            arnold.vizualize.draw(False)
        except:
            pass
        if arnold.beyond_final_point:
            print("FINAL PART")
            print(arnold.map.find_path())
            arnold.follow_path(5, 10, True)
            return
        else:
            arnold.follow_path(1, 0.5)
            arnold.robot.look_at_position(arnold.map.point_of_interest.position)

if __name__ == "__main__":
    main()
