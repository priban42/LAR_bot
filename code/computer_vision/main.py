import numpy as np
import cv2

color_img = np.load("color1.npy", allow_pickle=True)
hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)

b, g, r    = color_img[:, :, 0], color_img[:, :, 1], color_img[:, :, 2]
h, s, v    = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

green_rgb = np.array([71, 150, 92], np.uint8)
green_hsv = cv2.cvtColor(green_rgb, cv2.COLOR_RGB2HSV)

print(green_rgb, green_hsv)
hsv_ref_green = np.array([96, 36, 59], np.uint8)
h_treshold = 30
h_mask_1 = np.where((h - hsv_ref_green[0]) < h_treshold, True, False)
h_mask_2 = np.where((hsv_ref_green[0] - h) < h_treshold, True, False)
h_mask = h_mask_1 | h_mask_2
#h_mask_1.astype(int)
#color_img*h_mask
#s_mask = (s > hsv_ref_green[0]).astype(int)
idx = (h_mask == False)
color_img[idx] = 0
cv2.imshow("bagr", color_img)
cv2.waitKey()