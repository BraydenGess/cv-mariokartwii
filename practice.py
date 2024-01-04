#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os

cap = cv.VideoCapture(0)
ret,frame = cap.read()
print(frame)
cv.imwrite('train_models/training_images/home_trainingimages/Home#14.png', imgtobinary(frame))



