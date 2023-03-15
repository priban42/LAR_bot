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

def save_depth_image(path, name):
    img = np.load(path + name, allow_pickle=True)
    img = img.clip(256, 512)

    print(np.max(img))
    print(np.shape(img))

    img = (img - np.ones((480, 848))*256)*2

    grayscale = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    grayscale[:, :, 0] = img
    grayscale[:, :, 1] = img
    grayscale[:, :, 2] = img

    print(img)
    print (np.max(img))
    #print(grayscale)
    cv2.imwrite(name + ".jpg", grayscale)
    #cv2.imshow(name, grayscale)
    #cv2.waitKey()

path = "/home.nfs/pribavoj/PycharmProjects/LAR_bot/code/fotoaparat/color_pictures/"
#path = "color_pictures/"
path = "depth_pictures/"
#name = "23_60_17_58_19.npy"

#display_color_image(path, "23_67_16_38_57.npy")
save_depth_image(path, "23_67_16_39_35.npy")
#display_depth_image(path, "23_67_16_39_35.npy")
#print(os.listdir(path))
for name in os.listdir(path):
    #display_color_image(path, name)
    #display_depth_image(path, name)
    #save_depth_image(path, name)
    pass

