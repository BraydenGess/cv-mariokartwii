#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os
img_path = 'train_models/training_images/menu_trainingimages/Start#A.png'
dup_path = 'train_models/training_images/menu_trainingimages/Start#C.png'
img = cv.imread(img_path)
cv.imwrite(dup_path,img)





