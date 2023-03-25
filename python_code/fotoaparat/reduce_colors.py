import numpy as np
import PIL
import time
import scipy.misc
#from scipy.misc import toimage
import cv2

# Define color codes for each color
WHITE = np.array([255, 255, 255])
PURPLE = np.array([128, 0, 128])
YELLOW_RGB = np.array([255, 255, 0])
YELLOW = np.array([0, 255, 255])
BLUE_RGB = np.array([15, 60, 255])
BLUE = np.array([255, 60, 15])
RED_RGB = np.array([255, 0, 0])
RED = np.array([0, 0, 255])
GREY = np.array([128, 128, 128])
GREEN = np.array([0, 128, 0])
BLACK = np.array([0, 0, 0])







blue_hsv = 98
red_hue0_hsv = 0
red_hue179_hsv = 179
green_hsv = 60
purple_hsv = 125
yellow_hsv = 30

find_color = {
    30 : 0,
    60 : 30,
    98 : 60,
    125 : 98,
    179 : 125
}


colors = [red_hue0_hsv, yellow_hsv, green_hsv, blue_hsv, purple_hsv, red_hue179_hsv]

# Define function to reduce color of each pixel to one of the predefined colors
def reduce_color(pixel_original, white_values):

    pixel = pixel_original
    #když je barva dostatečně saturovaná hledá barvy
    if pixel[1] > 160:
        previous = pixel[0]
        for col in colors:
            #print(col)
            #prochází barvy postupně dokavad nenajde horší, následně vezme předchozí
            new = abs(pixel[0] - col)
            if new > previous:
                #print(find_color[col])
                out = find_color[col]
                return np.array([out, 255, 255])
            previous = new
        return np.array([0, 255, 255])
    else:
        #rozlišení černé, bílé, šedé
        v = pixel[2]
        a = pixel[2] * (255. / white_values[2])
        pixel[2] = min(a, 255)
        # if a < v:
        #    print(pixel[2], v)
        if pixel[2] < 80:
            return np.array([0, 0, 0])
        elif pixel[2] > 160:
            return np.array([0, 0, 255])
        else:
            return np.array([0, 0, 127])


# Define function to apply reduce_color to each pixel in the image
def reduce_colors(image):
    #zavolá pro každý pixel fci reduce color
    white_values = [220, 220, 220]
    return np.apply_along_axis(reduce_color, 2, image, white_values)

# Example usage
"""image = np.array([
    [[255, 255, 255], [128, 0, 128], [255, 255, 0]],
    [[0, 0, 255], [255, 0, 0], [128, 128, 128]],
    [[0, 128, 0], [255, 255, 255], [128, 0, 128]]
])"""


#import image in np form
np_img_input = np.load("color_pictures_old/" + "23_60_17_58_14.npy", allow_pickle=True)

#convert brg to hsv
image_hsv = cv2.cvtColor(np_img_input, cv2.COLOR_BGR2HSV)
#now hsv is saturated
cv2.imshow("name1", cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)/255)
cv2.waitKey()
reduced_image_hsv = np.array(image_hsv)

#image_hsv = cv2.convertScaleAbs(image_hsv, alpha=6, beta=1)

image_hsv[...,1] = image_hsv[...,1]*60
image_hsv = image_hsv.clip(0, 255)

cv2.imshow("name2", cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)/255)
cv2.waitKey()


reduced_image_hsv = reduce_colors(image_hsv)
cv2.imshow("name", reduced_image_hsv/255)
cv2.waitKey()

print(reduced_image_hsv.shape)
reduced_image_hsv = np.uint8(reduced_image_hsv)

#print(reduced_image_hsv)
reduced_image_rgb = cv2.cvtColor(reduced_image_hsv, cv2.COLOR_HSV2BGR)

cv2.imshow("name", reduced_image_rgb/255)
cv2.waitKey()
#imshow(reduced_image)
#img = Image.fromarray(reduced_image, 'RGB')
#img.show()
#print(reduced_image)
