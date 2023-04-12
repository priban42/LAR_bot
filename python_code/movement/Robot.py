import numpy as np
from robolab_turtlebot import Turtlebot, Rate, get_time
import math
import time


class Robot:
    def __init__(self):
        self.turtle = Turtlebot()
        self.turtle = Turtlebot(rgb=True, pc=True)
        self._rate = Rate(10)
        self.position = np.array([0, 0])
        self.direction = np.array([0, -1]) #x, y [0, 1] is aiming up
        self._angular_velocity = 28.6  # in degrees/sec
        self._angular_acceleration = 28.6  # in degrees/sec
        self._linear_velocity = 0.3  # in meters/sec
        self._linear_acceleration = 0.3
        self.turtle.register_bumper_event_cb(self._bumper)
        self.turtle.register_button_event_cb(self._button)

        self.ACTIVE = False
        self.beyond_final = False

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
    def _button(self, msg):
        """
        This functions executes after any button is pressed. Used to start bot.
        :param msg: contains information about wich button has been pressed. (unused)
        """
        print("BUMPER PRESSED!")
        self.ACTIVE = True

    def rotate_bot_old(self, angle: float) -> None:  # deg
        """
        Physically rotates the turtle bot by an angle. Might not be very accurate.
        :param angle: in degrees
        """
        speed = (2*np.pi*self._angular_velocity)/360
        angle_rad = (2*np.pi*angle)/360
        t = abs(angle_rad) / speed
        t = t*1.3 + 4/self._angular_velocity
        #t = (t + 1.0828/(self._angular_velocity * (2 * np.pi / 360)))/0.4871
        start = get_time()
        speed = np.sign(angle_rad) * speed
        print("rotation:", t, speed)
        while get_time() - start < t and self.ACTIVE:
            self.turtle.cmd_velocity(angular=speed, linear=0)
            self._rate.sleep()
        if not self.ACTIVE:
            self.turtle.cmd_velocity(linear=0, angular=0)
        self.direction = self._rotate_vector(self.direction, angle)

    def rotate_bot(self, angle: float) -> None:
        """
        Physically moves the turtle bot a certain distance. Might not be very accurate.
        :param distance: in meters
        """
        #time.sleep(1)
        fixed_angle = angle + 3#rotational asymetry
        self.turtle.reset_odometry()
        time.sleep(0.5)
        angle_sign = np.sign(fixed_angle)
        abs_angle = abs(fixed_angle)

        if abs_angle > (self._angular_acceleration**2)/self._angular_velocity:
            abs_angle = abs_angle - 4*self._angular_velocity/28.6
        else:
            abs_angle = abs_angle# - 0.5*(np.sqrt(abs_angle*self._linear_acceleration))/(28.6)

        angle_rad = ((abs_angle - 4)/360)*2*np.pi
        #print(angle_sign, angle_rad)
        angular_acceleration_rad = (self._angular_acceleration/360)*2*np.pi
        angular_velocity_rad = (self._angular_velocity/360)*2*np.pi
        t_last = get_time()
        v = 0 #current velocity
        distance_travelled = 0
        while(distance_travelled < angle_rad/2):
            dt = get_time() - t_last
            dv = angular_acceleration_rad * dt
            if v < angular_velocity_rad:
                v += dv
            self.turtle.cmd_velocity(linear = 0, angular = v*angle_sign)
            t_last = get_time()
            self._rate.sleep()
            x, y, a = self.turtle.get_odometry()#a is from -pi to pi
            distance_travelled = abs(a)
            #print(distance_travelled)
            if not self.ACTIVE:
                self.turtle.cmd_velocity(linear=0, angular=0)
                break
        while(distance_travelled < angle_rad):
            self.turtle.cmd_velocity(linear=0, angular=v*angle_sign)
            self._rate.sleep()
            x, y, a = self.turtle.get_odometry()
            distance_travelled = abs(a)
            #print("2.2", distance_travelled)
            if not self.ACTIVE:
                self.turtle.cmd_velocity(linear=0, angular=0)
                break
        self.turtle.cmd_velocity(linear=0, angular=0)
        self.direction = self._rotate_vector(self.direction, angle)
        #self.position = self.position + self.direction*distance

    def move_bot_old(self, distance: float) -> None:
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
            self.turtle.cmd_velocity(linear=speed, angular=0)
            self._rate.sleep()
        if not self.ACTIVE:
            self.turtle.cmd_velocity(linear=0, angular=0)
        self.position = self.position + self.direction*distance

    def move_bot(self, dist: float) -> None:
        """
        Physically moves the turtle bot a certain distance. Might not be very accurate.
        :param distance: in meters
        """
        #time.sleep(1)
        self.turtle.reset_odometry()
        time.sleep(0.5)
        if dist > (self._linear_velocity**2)/self._linear_acceleration:
            distance = dist - 0.05*self._linear_velocity/0.3
        else:
            distance = dist - 0.045*(np.sqrt(dist*self._linear_acceleration))/(0.3)
        #print((self._linear_velocity**2)/self._linear_acceleration)
        #print(distance)
        t_last = get_time()
        v = 0 #current velocity
        distance_travelled = 0
        while(distance_travelled < distance/2):
            dt = get_time() - t_last
            dv = self._linear_acceleration * dt
            if v < self._linear_velocity:
                v += dv
            self.turtle.cmd_velocity(linear = v, angular = 0)
            t_last = get_time()
            self._rate.sleep()
            x, y, a = self.turtle.get_odometry()
            odometry_vector = np.array([x, y])
            distance_travelled = np.linalg.norm(odometry_vector)
            #print(distance_travelled)
            if not self.ACTIVE:
                self.turtle.cmd_velocity(linear=0, angular=0)
                break
        while(distance_travelled < distance):
            self.turtle.cmd_velocity(linear=v, angular=0)
            self._rate.sleep()
            x, y, a = self.turtle.get_odometry()
            odometry_vector = np.array([x, y])
            distance_travelled = np.linalg.norm(odometry_vector)
            #print("2.2", distance_travelled)
            if not self.ACTIVE:
                self.turtle.cmd_velocity(linear=0, angular=0)
                break
        self.turtle.cmd_velocity(linear=0, angular=0)
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

    def relative_to_absolute_position(self, relative_position: np.array([float, float])) -> np.array([float, float]):
        """
        Calculates coordinates according to robots position and angle.
        :param relative_position:
        :return:
        """
        base_vector = np.array([0, 1])
        angle = self._clockwise_angle_between_vectors(base_vector, self.direction)
        rotated_position = self._rotate_vector(relative_position, angle)
        absolute_position = rotated_position + self.position
        return absolute_position

    def align_with_vector(self, vect: np.ndarray) -> None:
        """
        rotates the robot so that it aims in the same direction as vector 'vect'.
        :param vect: any nonzero 2d vector.
        """
        angle = self._angle_between_vectors(self.direction, vect)
        self.rotate_bot(angle)
        self.direction = self._normalize_vector(vect)

    def look_at_position(self, position):
        """
        Rotates the robot so that it aims at the 'position'.
        :param position:
        """
        vector = position - self.position
        self.align_with_vector(vector)

    def move_to_position(self, position):
        """
        Rotates bot and moves it forward in order to arrive at point
        :param point:
        """
        vect = position - self.position
        distance = np.linalg.norm(vect)
        self.align_with_vector(vect)
        self.move_bot(distance)


    def move_along_path(self, path, max_distance = 1000):
        """
        Moves along path.
        :param path: a list of points to witch to travel.
        :param max_distance: Maximal distance the robot travels on single call of this function.
         if exceeded the robot stops moving.
        """
        distance_traveled = 0
        for point in path:
            distance = np.linalg.norm(self.position - point.position)
            if max_distance > distance_traveled + distance:
                self.move_to_position(point.position)
                if point.final and not self.beyond_final:
                    self.beyond_final = True
                    return True
            else:
                norm_vect = (point.position - self.position)/np.linalg.norm(point.position - self.position)
                new_position = self.position + (max_distance - distance_traveled) * norm_vect
                self.move_to_position(new_position)
        return False

    if __name__ == "__main__":
        pass
