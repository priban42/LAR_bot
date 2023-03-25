import numpy as np
import cv2
import sys
import time


class Computer_vision:
    COLORS = ["blue", "green", "yellow", "purple", "red"]
    COLOR_BOUNDS = {
        "blue": [np.array([95, 110, 70]), np.array([102, 255, 255])],
        "green": [np.array([42, 70, 70]), np.array([75, 255, 255])],
        "yellow": [np.array([22, 135, 70]), np.array([32, 255, 255])],
        "purple": [np.array([113, 50, 70]), np.array([146, 255, 255])],
        "red":[np.array([180, 105, 122]), np.array([180, 255, 255]), np.array([0, 110, 120]), np.array([10, 255, 255])]
    }
    def __init__(self):
        self.bgr_image = None
        self.hsv_image = None
        self.point_cloud = None
        self.max_u = 640
        self.max_v = 480
        self.max_object_size = 100000
        self.min_object_size = 500
        self.color_masks = {"blue": None, "green": None, "yellow": None, "purple": None, "red":None}
        self.connected_components = {"blue": None, "green": None, "yellow": None, "purple": None, "red":None}
        self.contours = {"blue": None, "green": None, "yellow": None, "purple": None, "red":None}

    def _click_data(self, event, x, y, flags, param):
        """
        upon calling cv2.setMouseCallback('NAME OF WINDOW', self._click_data); this function is set to be called upon sensing an event.
         This function than checks weather the event is left mouse button click and prints useful information about the clicked pixel.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            print("[U, V]:",[x, y],"HSV:", self.hsv_image[y, x], "BGR:", self.bgr_image[y, x], "PC:", self.point_cloud[y, x], "distance:", np.linalg.norm(self.point_cloud[y, x]))
    def update_image(self, bgr_image, point_cloud):
        """
        Updates color image and point cloud. Also calculates coresponding hsv image. Call everytime new images are meant to be analyzed.
        :param bgr_image:
        :param point_cloud:
        """
        self.bgr_image = bgr_image
        self.point_cloud = point_cloud
        self.hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
        self.update_color_masks()
        self.update_contours()

    def display_bgr_image(self):
        """
        Displays color image.
        """
        cv2.imshow("BGR", self.bgr_image)
        cv2.setMouseCallback('BGR', self._click_data)
        cv2.waitKey()

    def display_hsv_img(self):
        """
        Displays hsv image as bgr. (in the wierd way).
        """
        cv2.imshow("HSV", self.hsv_image)
        cv2.setMouseCallback('HSV', self._click_data)
        cv2.waitKey()
    def display_pc_img(self):
        """
        takes the Z coordinate and displays it as grayscale. (Not much is visible here).
        """
        x_range = (-0.3, 0.3)
        z_range = (0.3, 3.0)
        depth_img = self.point_cloud
        # mask out floor points
        mask = self.point_cloud[:, :, 1] > x_range[0]

        # mask point too far and close
        mask = np.logical_and(mask, self.point_cloud[:, :, 2] > z_range[0])
        mask = np.logical_and(mask, self.point_cloud[:, :, 2] < z_range[1])
        image = np.zeros(mask.shape)

        # assign depth i.e. distance to image
        image[mask] = np.int8(self.point_cloud[:, :, 2][mask] / 3.0 * 255)
        im_color = cv2.applyColorMap(255 - image.astype(np.uint8),
                                     cv2.COLORMAP_JET)
        cv2.imshow("Point cloud", im_color)
        cv2.setMouseCallback('Point cloud', self._click_data)
        cv2.waitKey()

    def display_color_masks(self, *colors):
        """
        Combines colormasks into one and displays it.
        :param colors: A list of colors, where colors are sring names. for example:  "red", "blue", ....
        """
        final_mask = self.color_masks[colors[0]]
        if len(colors) > 1:
            for color in colors[1:]:
                final_mask = final_mask | self.color_masks[color]
        print(type(final_mask), final_mask.dtype)
        print(type(self.bgr_image), self.bgr_image.dtype)
        masked_image = cv2.bitwise_and(self.bgr_image, self.bgr_image, mask=final_mask)
        cv2.imshow("Masked BGR", masked_image)
        cv2.setMouseCallback('Masked BGR', self._click_data)
        cv2.waitKey()


    def get_color_mask(self, color):
        """
        :param color: string name of desired color. For example: "red". color must be included in self.COLORS.
        :return: A 2d uint8 numpy array where 1 corresponds to color present on pixe and 0 means otherwise.
        """
        if color == "red":
            mask1 = cv2.inRange(self.hsv_image, self.COLOR_BOUNDS[color][0], self.COLOR_BOUNDS[color][1])
            mask2 = cv2.inRange(self.hsv_image, self.COLOR_BOUNDS[color][2], self.COLOR_BOUNDS[color][3])
            mask = mask1 | mask2
        else:
            mask = cv2.inRange(self.hsv_image, self.COLOR_BOUNDS[color][0], self.COLOR_BOUNDS[color][1])
        return mask

    def update_color_masks(self):
        """
        Creates a new mask for each color in self.COLORS.
        """
        for color in self.COLORS:
            self.color_masks[color] = self.get_color_mask(color)

    def update_connected_components(self):
        """
        Updates the dictionary of connected components for each color.
        """
        for color in self.COLORS:
            mask = self.color_masks[color]
            components = cv2.connectedComponentsWithStats(mask)
            filtered_components = []
            for component in components:
                if self.min_object_size < component[2][4] < self.max_object_size:
                    filtered_components.append(component)
            self.connected_components[color] = filtered_components

    def display_connected_components(self, *colors): #deprecated
        """
        Combines connected components into one and displays it.
        :param colors: A list of colors, where colors are sring names. for example:  "red", "blue", ....
        """
        final_mask = self.connected_components[colors[0]][1].astype("uint8")
        if len(colors) > 1:
            for color in colors[1:]:
                final_mask = final_mask | self.connected_components[color][1].astype("uint8")
        masked_image = cv2.bitwise_and(self.bgr_image, self.bgr_image, mask=final_mask)
        cv2.imshow("BGR masked by Connected compoments", masked_image)
        cv2.setMouseCallback('BGR masked by Connected compoments', self._click_data)
        cv2.waitKey()

    def update_contours(self):
        """
        Generates countours and filters them by size.
        Desirable contours are then placed in self.contours according to their color.
        """
        for color in self.COLORS:
            filtered_contours = []
            contours, hierarchy = cv2.findContours(self.color_masks[color], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if self.min_object_size < cv2.contourArea(contour) < self.max_object_size:
                    filtered_contours.append(contour)
            self.contours[color] = filtered_contours

    def display_contours(self, *colors):
        """
        Displays contours according to selected colors.
        :param colors: A list of colors, where colors are sring names. for example:  "red", "blue", ....
        """
        img = self.bgr_image
        for color in colors:
            cv2.drawContours(img, self.contours[color], -1, (0, 255, 0), 1)
        cv2.imshow("Contours on BGR", img)
        cv2.setMouseCallback('Contours on BGR', self._click_data)
        cv2.waitKey()

    def get_position_from_contour(self, contour, index):
        shape = list(self.bgr_image.shape)[:2]
        mask = np.zeros(shape, np.float64)
        cv2.drawContours(mask, contour, index, 1, -1)
        indeces = np.nonzero(mask)
        #print(self.point_cloud[indeces])
        points = np.delete(self.point_cloud[indeces], 1, 1)#remove Y coordinate (irelevant)
        points = points * np.array([-1, 1]) #fliping x coordinate
        #print(points)
        median = np.nanmedian(points, axis=(0))
        quantile = np.nanquantile(points, 0.3, axis=(0))
        #mean = np.nanmean(points, axis=(0))
        return quantile
    def get_color_center_position(self, color):#deprecated
        #mask = self.get_color_mask(color)
        mask = self.color_masks[color]
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

    def get_point_cloud_avg_xyz_on_uv(self, uv, sizeU = 4, sizeV = 8):#deprecated
        u = uv[0]
        v = uv[1]
        area_of_interest = self.point_cloud[max(v-sizeV//2, 0):min(v+sizeV//2, self.max_v), max(u-sizeU//2, 0):min(u+sizeU//2, self.max_u)]

        avg = np.nanmedian(area_of_interest, axis=(0, 1))
        return avg

    def get_list_of_objects_old(self):#deprecated
        objects = []
        self.update_color_masks()
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

    def get_list_of_objects(self):
        objects = []
        self.update_color_masks()
        for color in self.COLORS:
            color_contours = self.contours[color]
            if color_contours != None:
                for index in range(len(color_contours)):
                    position = self.get_position_from_contour(color_contours, index)
                    objects.append([color, position])
        return objects

if __name__ == "__main__":
    #np.set_printoptions(threshold=sys.maxsize)
    computer_vision = Computer_vision()
    cloud = np.load("cloud1.npy", allow_pickle=True)
    bgr_image = np.load("color1.npy", allow_pickle=True)
    computer_vision.update_image(bgr_image, cloud)
    computer_vision.update_color_masks()
    #computer_vision.display_pc_img()
    computer_vision.update_contours()
    #computer_vision.get_position_from_contour(computer_vision.contours["purple"], 0)
    print(computer_vision.get_list_of_objects_old())
    print(computer_vision.get_list_of_objects())

    computer_vision.display_contours("purple", "red", "green", "blue", "yellow")
    #computer_vision.update_connected_components()
    #computer_vision.display_color_masks("purple", "green", "red", "yellow", "blue")


    #computer_vision.display_connected_components("purple", "green", "red", "yellow", "blue")

    #copmputer_vision.display_pc_img()
    #objects = copmputer_vision.get_list_of_objects()
    #print(objects)