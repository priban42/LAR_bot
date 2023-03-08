import numpy as np
from robolab_turtlebot import Turtlebot, Rate, get_time
import math

class Robot:
    def __init__(self):
        self.turtle = Turtlebot()
        self.rate = Rate(10)
        self.position = [0, 0]
        self.direction = [0, 1]
        self.angular_velocity = 1.5# 1.5... *1.25
        self.linear_velocity = 0.3
        self.turtle.register_bumper_event_cb(self.bumper)
        self.ACTIVE = True
        print("robot initialized...")

    def bumper(self, msg):
        print("BUMPER PRESSED!")
        self.ACTIVE = False

    def rotate_bot(self, angle):#deg
        t = abs(angle)/self.angular_velocity*1.24*(2*np.pi/360)
        start = get_time()
        speed = np.sign(angle)*self.angular_velocity
        print(t, speed)
        while get_time() - start < t and self.ACTIVE:
            self.turtle.cmd_velocity(angular = speed, linear = 0)
            self.rate.sleep()

    def move_bot(self, distance):
        t = abs(distance)/self.linear_velocity
        start = get_time()
        speed = np.sign(distance)*self.linear_velocity
        print(t, speed)
        while get_time() - start < t and self.ACTIVE:
            self.turtle.cmd_velocity(linear = speed, angular = 0)
            self.rate.sleep()

    @staticmethod
    def angle_between_vectors(vect1, vect2):  # rad
        ang1 = np.arctan2(*vect1[::-1])
        ang2 = np.arctan2(*vect2[::-1])
        angle = np.rad2deg(ang1 - ang2) % (360)
        if angle > 180:
            angle -= 360
        return angle

    @staticmethod
    def normalize_vector(vect):
        norm = vect / np.linalg.norm(vect)
        return norm

    @staticmethod
    def rotate_vector(vect, angle):#angle in degrees, kladny uhel = proti smeru hod. rucicek
        theta = np.deg2rad(-angle)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        return(np.dot(rot, vect))

    def align_with_vector(self, vect):
        angle = self.angle_between_vectors(self.direction, vect)
        self.rotate_bot(angle)
        self.direction = self.normalize_vector(vect)

    def move_to_position(self, position):
        pass
