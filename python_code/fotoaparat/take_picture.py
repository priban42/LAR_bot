from __future__ import print_function

import time
import cv2

import numpy as np

from robolab_turtlebot import Turtlebot, Rate

import random

import os

bumper_names = ['LEFT', 'CENTER', 'RIGHT']
state_names = ['RELEASED', 'PRESSED']



def take_pictures(msg):
    time.sleep(0.5)
    loc_time = time.localtime()
    year = loc_time.tm_year - 2000
    im_id = str(year) + "_" + str(loc_time.tm_yday) + "_" + str(loc_time.tm_hour) + "_" + str(
        loc_time.tm_min) + "_" + str(loc_time.tm_sec)

    rand = im_id
    turtle.wait_for_point_cloud()
    point_cloud = turtle.get_point_cloud()

    turtle.wait_for_rgb_image()
    color_picture = turtle.get_rgb_image()

    turtle.wait_for_depth_image()
    depth_picture = turtle.get_depth_image()
    #print(color_picture)
    np.save("/home.nfs/pribavoj/PycharmProjects/LAR_bot/python_code/fotoaparat/point_cloud_pictures/" + str(rand), point_cloud, allow_pickle=True)
    np.save("/home.nfs/pribavoj/PycharmProjects/LAR_bot/python_code/fotoaparat/color_pictures/" + str(rand), color_picture, allow_pickle=True)
    np.save("/home.nfs/pribavoj/PycharmProjects/LAR_bot/python_code/fotoaparat/depth_pictures/" + str(rand), depth_picture, allow_pickle=True)
    print("picture taken")

def bumper_cb(msg):
    #bumper = bumper_names[msg.bumper]
    #state = state_names[msg.state]
    #print(msg.bumper, type(msg.bumper))
    #print(msg.state, type(msg.state))
    if msg.bumper == 1 and msg.state == 1:
        print("condition met")
        take_pictures(msg)

def main():
    #/home.nfs/pribavoj/PycharmProjects/LAR_bot/python_code/fotoaparat/take_picture.py
    global turtle
    turtle = Turtlebot(rgb=True, depth=True, pc=True)
    rate = Rate(1)
    turtle.register_bumper_event_cb(bumper_cb)
    while not turtle.is_shutting_down():
        rate.sleep()


if __name__ == '__main__':
    main()
