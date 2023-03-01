import numpy as np
import cv2
import time
name = "23_60_17_58_19.npy"
path = "/home.nfs/pribavoj/PycharmProjects/LAR_bot/code/fotoaparat/color_pictures/"

img = np.load(path + name, allow_pickle=True)
#print(img)
#print(img.shape)
img = img/255
cv2.imshow("image", img)
cv2.waitKey()
imga = np.zeros([5,5,3])

imga[:,:,0] = np.ones([5,5])*64/255.0
imga[:,:,1] = np.ones([5,5])*128/255.0
imga[:,:,2] = np.ones([5,5])*192/255.0
print(imga.shape)
print(imga)
cv2.imwrite('color_img.jpg', imga)
cv2.imshow("image", imga)
cv2.waitKey()
