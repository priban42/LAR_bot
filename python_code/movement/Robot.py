import numpy as np
from robolab_turtlebot import Turtlebot, Rate, get_time
import math


class Robot:
    def __init__(self):
        self._turtle = Turtlebot()
        self._turtle = Turtlebot(rgb=True, pc=True)
        self._rate = Rate(10)
        self.position = np.array([0, 0])
        self.direction = np.array([0, -1]) #x, y [0, 1] is aiming up
        self._angular_velocity = 28.6  # 1.5... *1.25
        self._linear_velocity = 0.3
        self._turtle.register_bumper_event_cb(self._bumper)
        self.ACTIVE = True
        print("robot initialized...")

    def __str__(self):
        return "position:" + str(self.position) + "direction:" + str(self.direction) + "ACTIVE:" + str(self.ACTIVE)

    def _bumper(self, msg):
        """
        This functions executes after a bumper is pressed. Used to stop any movement.
        :param msg: contains information about wich button has been pressed. (unused)
        """
        print("BUMPER PRESSED!")
        self.ACTIVE = False

    def rotate_bot(self, angle: float) -> None:  # deg
        """
        Physically rotates the turtle bot by an angle. Might not be very accurate.
        :param angle: in degrees
        """
        speed = (2*np.pi*self._angular_velocity)/360
        angle_rad = (2*np.pi*angle)/360
        t = abs(angle_rad) / speed
        t = t*1.25 + 8/self._angular_velocity
        #t = (t + 1.0828/(self._angular_velocity * (2 * np.pi / 360)))/0.4871
        start = get_time()
        speed = np.sign(angle_rad) * speed
        print("rotation:", t, speed)
        while get_time() - start < t and self.ACTIVE:
            self._turtle.cmd_velocity(angular=speed, linear=0)
            self._rate.sleep()
        if not self.ACTIVE:
            self._turtle.cmd_velocity(linear=0, angular=0)
        self.direction = self._rotate_vector(self.direction, angle)

    def move_bot(self, distance: float) -> None:
        """
        Physically moves the turtle bot a certain distance. Might not be very accurate.
        :param distance: in meters
        """
        t = abs(distance) / self._linear_velocity
        #t = (t - 0.4603/self._linear_velocity)/0.9208
        t = t*1.13 - self._linear_velocity*0.1
        start = get_time()
        speed = np.sign(distance) * self._linear_velocity
        print("linear movement:", t, speed)
        while get_time() - start < t and self.ACTIVE:
            self._turtle.cmd_velocity(linear=speed, angular=0)
            self._rate.sleep()
        if not self.ACTIVE:
            self._turtle.cmd_velocity(linear=0, angular=0)
        self.position = self.position + self.direction*distance

    @staticmethod
    def _angle_between_vectors(vect1: np.ndarray, vect2: np.ndarray) -> float:  # in degrees
        """
        :param vect1: main vector. (use Robot.direction here)
        :param vect2: secondary vector
        :return: angle between 180° and -180°
        """
        ang1 = np.arctan2(*vect1[::-1])
        ang2 = np.arctan2(*vect2[::-1])
        angle = np.rad2deg(ang1 - ang2) % (360)
        if angle > 180:
            angle -= 360
        return angle

    @staticmethod
    def _clockwise_angle_between_vectors(vect1: np.ndarray, vect2: np.ndarray) -> float:
        """
        :param vect1: main vector. (use Robot.direction here)
        :param vect2: secondary vector
        :return: angle between 0° and 360° in clockwise direction
        """
        ang1 = np.arctan2(*vect1[::-1])
        ang2 = np.arctan2(*vect2[::-1])
        angle = np.rad2deg(ang1 - ang2) % 360
        return angle

    @staticmethod
    def _normalize_vector(vect: np.ndarray) -> np.ndarray:
        """
        normalizes a vector. for example: (100, 0) -> (1, 0)
        :param vect: any nonzero 2d vector
        :return: normalized vector
        """
        norm = vect / np.linalg.norm(vect)
        return norm

    @staticmethod
    def _rotate_vector(vect: np.ndarray,
                       angle: float) -> np.ndarray:  # angle in degrees, kladny uhel = proti smeru hod. rucicek
        """
        Takes a vector and rotates it by angle.
        :param vect: any nonzero 2d vector
        :param angle: in degrees preferably between 180° and -180°
        :return: rotated vector
        """
        theta = np.deg2rad(-angle)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        return (np.dot(rot, vect))

    def relative_to_absolute_position(self, relative_position):
        base_vector = np.array([0, 1])
        angle = self._clockwise_angle_between_vectors(base_vector, self.direction)
        rotated_position = self._rotate_vector(relative_position, angle)
        absolute_position = rotated_position + self.position
        return absolute_position

    def align_with_vector(self, vect: np.ndarray) -> None:
        """
        rotates the robot so that it aims in the same direction as vector 'vect'
        :param vect: any nonzero 2d vector
        """
        angle = self._angle_between_vectors(self.direction, vect)
        self.rotate_bot(angle)
        self.direction = self._normalize_vector(vect)


    def move_to_position(self, point):
        vect = point.position - self.position
        distance = np.linalg.norm(vect)
        self.align_with_vector(vect)
        self.move_bot(distance)

    def move_along_path(self, path):
        for position in path:
            self.move_to_position(position)

    if __name__ == "__main__":
        pass
