#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary,sharpimgtobinary
import numpy as np
import os
from spotify_audio import *
x = [120,675,80,140]
#img = cv.imread('train_models/training_images/playercount_trainingimages/players2#A.png')
#img2 = cv.imread('train_models/training_images/playercount_trainingimages/players2#B.png')
#img3 = cv.subtract(img2,img)
#cv.imwrite('cack.png',img3)


cap = cv.VideoCapture(0)
count = 0
while cap.isOpened():
    ret,frame = cap.read()
    file_name = 'cack' + str(count) + '.png'
    count += 1
    cv.imwrite(file_name,sharpimgtobinary(frame))
    if count == 5:
        break




