import numpy as np
import cv2
import time
import os

def display_color_image(path, name):
    img = np.load(path + name, allow_pickle=True)
    img = img/255
    cv2.imshow(name, img)
    cv2.waitKey()

def display_depth_image(path, name):
    img = np.load(path + name, allow_pickle=True)
    grayscale = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    grayscale[:, :, 0] = img*5
    grayscale[:, :, 1] = img*5
    grayscale[:, :, 2] = img*5
    #print(grayscale)
    cv2.imshow(name, grayscale)
    cv2.waitKey()

path = "/home.nfs/pribavoj/PycharmProjects/LAR_bot/code/fotoaparat/color_pictures/"
path = "color_pictures/"
path = "depth_pictures/"
#name = "23_60_17_58_19.npy"

#print(os.listdir(path))
for name in os.listdir(path):
    #display_color_image(path, name)
    display_depth_image(path, name)

