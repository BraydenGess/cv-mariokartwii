#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os
from spotify_audio import *
x = [120,675,80,140]
img = cv.imread('train_models/training_images/playercount_trainingimages/players2#A.png')
frame = img[80:140,555:640]
cv.imwrite('cack.png',frame)

sp = setup_spotifyobject(file='credentials.txt')
print(sp.current_playback()['item']['uri'])