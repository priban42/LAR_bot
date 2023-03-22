import numpy as np
import cv2
import time
import os

def display_color_image(path, name):
    img = np.load(path + name, allow_pickle=True)
    img = img/255
    cv2.imshow(name, img)
    cv2.waitKey()

def save_color_image(path_to_open, path_to_save, name):
    img = np.load(path_to_open + name, allow_pickle=True)
    #img = img/255
    #print(img)
    #cv2.imshow(name, img)
    #cv2.waitKey()
    cv2.imwrite(path_to_save + name + ".jpg", img)

def display_depth_image(path, name):
    img = np.load(path + name, allow_pickle=True)
    grayscale = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    grayscale[:, :, 0] = img*5
    grayscale[:, :, 1] = img*5
    grayscale[:, :, 2] = img*5
    #print(grayscale)
    #cv2.imshow(name, grayscale)
    #cv2.waitKey()
    cv2.imwrite(name + ".jpg", grayscale)
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

path = "/code/fotoaparat/color_pictures/"
path = "color_pictures/"
path2 = "color_pictures_jpg/"
#path = "depth_pictures_old/"
#name = "23_60_17_58_19.npy"

#display_color_image(path, "23_67_16_38_57.npy")
#save_depth_image(path, "23_67_16_39_35.npy")
#display_depth_image(path, "23_67_16_39_35.npy")
print(os.listdir(path))
for name in os.listdir(path):
    #display_color_image(path, name)
    #display_depth_image(path, name)
    try:
        save_color_image(path, path2, name)
    except:
        pass
    pass

