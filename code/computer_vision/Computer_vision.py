import numpy as np
import cv2
import time


class Computer_vision:
    COLORS = ["blue", "green", "yellow", "purple", "red"]
    COLOR_BOUNDS = {
        "blue": [np.array([95, 110, 70]), np.array([102, 255, 255])],
        "green": [np.array([48, 95, 70]), np.array([75, 255, 255])],
        "yellow": [np.array([22, 110, 70]), np.array([32, 255, 255])],
        "purple": [np.array([113, 70, 70]), np.array([138, 255, 255])],
        "red":[np.array([180, 105, 120]), np.array([180, 255, 255]), np.array([0, 110, 120]), np.array([10, 255, 255])]
    }
    def __init__(self):
        self.bgr_image = None
        self.hsv_image = None
        self.point_cloud = None
        self.max_u = 640
        self.max_v = 480
        self.max_object_size = 50000
        self.min_object_size = 500

    def update_image(self, color_img, point_cloud):
        self.color_image = color_img
        self.point_cloud = point_cloud
        self.hsv_image = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)

    def get_color_mask(self, color):
        if color == "red":
            mask1 = cv2.inRange(self.hsv_image, self.COLOR_BOUNDS[color][0], self.COLOR_BOUNDS[color][1])
            mask2 = cv2.inRange(self.hsv_image, self.COLOR_BOUNDS[color][2], self.COLOR_BOUNDS[color][3])
            mask = mask1 | mask2
        else:
            mask = cv2.inRange(self.hsv_image, self.COLOR_BOUNDS[color][0], self.COLOR_BOUNDS[color][1])
        return mask

    def get_color_center_position(self, color):
        mask = self.get_color_mask(color)
        out = cv2.connectedComponentsWithStats(mask)

        positions = []
        #if color == "purple":
        #    print("out", out[2], out[3])
        for a in range(len(out[3])):
            if self.min_object_size < out[2][a][4] < self.max_object_size:
                positions.append(out[3][a])
            else:
                pass
        #print("positions:", positions)
        return np.asarray(positions, dtype=np.int16)

    def get_point_cloud_avg_xyz_on_uv(self, uv, sizeU = 4, sizeV = 8):
        u = uv[0]
        v = uv[1]
        area_of_interest = self.point_cloud[max(v-sizeV//2, 0):min(v+sizeV//2, self.max_v), max(u-sizeU//2, 0):min(u+sizeU//2, self.max_u)]

        avg = np.nanmedian(area_of_interest, axis=(0, 1))
        return avg

    def get_list_of_objects(self):
        objects = []
        for color in self.COLORS:
            uvs = self.get_color_center_position(color)
            #print(color, uvs)
            for uv in uvs:
                position = self.get_point_cloud_avg_xyz_on_uv(uv)
                position = np.delete(position, 1) * np.array([-1, 1]) #excluding y coordinate and fliping x coordinate

                #print(color, position)
                if (not np.isnan(position).any()):
                    objects.append([color, position])
        return objects

if __name__ == "__main__":
    copmputer_vision = Computer_vision()
    cloud = np.load("cloud2.npy", allow_pickle=True)
    color_img = np.load("color2.npy", allow_pickle=True)
    copmputer_vision.update_image(color_img, cloud)
    objects = copmputer_vision.get_list_of_objects()
    print(objects)