import numpy as np
import cv2
import time

color_img = np.load("color1.npy", allow_pickle=True)
hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)

import timeit
start = time.time()

b, g, r    = color_img[:, :, 0], color_img[:, :, 1], color_img[:, :, 2]
h, s, v    = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

green_rgb = np.array([71, 150, 92], np.uint8)



lower_blue = np.array([95,110,70])
upper_blue = np.array([102,255,255])

lower_green = np.array([48,95,70])
upper_green = np.array([75,255,255])

lower_yellow = np.array([22,110,70])
upper_yellow = np.array([32,255,255])

lower_purple = np.array([117,100,70])
upper_purple = np.array([132,255,255])

lower_red1 = np.array([180,105,70])
upper_red1 = np.array([180,255,255])

lower_red2 = np.array([0,110,70])
upper_red2 = np.array([10,255,255])

# Threshold the HSV image to get only blue colors
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_green = cv2.inRange(hsv, lower_green, upper_green)
mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask = mask_blue|mask_green|mask_red1|mask_red2|mask_yellow|mask_purple

masked_image = color_img
masked_image = cv2.bitwise_and(color_img, color_img, mask=mask )
end = time.time()
print(end - start)
cv2.imshow("bagr", masked_image)

def click_data(event, x, y, flags, param):
    print(hsv[y][x])
cv2.setMouseCallback('bagr',click_data);
cv2.waitKey()
