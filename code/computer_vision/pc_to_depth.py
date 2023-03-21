import numpy as np
import cv2
import time


cloud = np.load("cloud2.npy", allow_pickle=True)
color_img = np.load("color2.npy", allow_pickle=True)
print(cloud.dtype, color_img.dtype)

color_img = color_img.astype('float64')
print(cloud.dtype, color_img.dtype)
color_img = color_img/255
print(color_img)
print(cloud)

cloud[:, :, 0] = 0
cloud[:, :, 1] = 0
img = (color_img+cloud)/2
#print(color_img)

#print(cloud)
cv2.imshow("bagr", img)

cv2.waitKey()