import numpy as np
from Entity import Entity
import math


class Object(Entity):
    def __init__(self, position=np.array([-100, -100]), radius=10):
        Entity.__init__(self, position)
        self.radius = radius
        self.color = "orange"

    def __eq__(self, other: 'Object') -> bool:
        comparison = self.position == other.position
        return comparison.all() and self.radius == other.radius

    def __hash__(self):
        return int(self.position[0] + 2*(10 ** 10) * self.position[1] + (10 ** 5)*self.radius)

    def set_radius(self, r):
        self.radius = r

    import math

    def get_adjecent_points(self, object: 'Object') -> tuple:
        """
        generates 2 coordinates for points laying in between 2 objects.
         the points lay on lines tanget to the obejct circle and have the same distance from both centres.
        :param object:
        :return:tuple of 2 positions
        """
        vect = (object.position - self.position)/2
        radius = (self.radius + object.radius)/2
        ortogonal_vect = np.array([-vect[1], vect[0]])
        ortogonal_vect = (radius * ortogonal_vect)/np.linalg.norm(ortogonal_vect)
        return self.position + vect + ortogonal_vect, self.position + vect - ortogonal_vect


    def line_segment_intersects_circle(self, line_segment):
        """
        Calculates weather any point of line_segment lays in the object circle.
        :param line_segment:
        :return:
        """
        #
        x1 = line_segment.A.position[0]
        y1 = line_segment.A.position[1]
        x2 = line_segment.B.position[0]
        y2 = line_segment.B.position[1]
        cx = self.position[0]
        cy = self.position[1]
        r = self.radius
        if (cx - x1) ** 2 + (cy - y1) ** 2 < r ** 2:
            return True

        if (cx - x2) ** 2 + (cy - y2) ** 2 < r ** 2:
            return True

        dx = x2 - x1
        dy = y2 - y1
        a = dx ** 2 + dy ** 2
        b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
        c = cx ** 2 + cy ** 2 + x1 ** 2 + y1 ** 2 - 2 * (cx * x1 + cy * y1) - r ** 2
        discriminant = b ** 2 - 4 * a * c

        # If the discriminant is negative, the line segment and circle do not intersect
        if discriminant < 0:
            return False

        # Calculate the points of intersection between the line and the circle
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        intersection_points = [(x1 + t1 * dx, y1 + t1 * dy), (x1 + t2 * dx, y1 + t2 * dy)]

        # Check whether the intersection points lie on the line segment
        for point in intersection_points:
            if (min(x1, x2) <= point[0] <= max(x1, x2)) and (min(y1, y2) <= point[1] <= max(y1, y2)):
                return True

        # If none of the intersection points lie on the line segment, the line segment and circle do not intersect
        return False
