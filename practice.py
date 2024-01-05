#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os
path = 'train_models/training_images/menu_trainingimages/Multiplayer#K.png'
new_path = 'train_models/training_images/playercount_trainingimages/players4#B.png'
cv.imwrite(new_path,cv.imread(path))


