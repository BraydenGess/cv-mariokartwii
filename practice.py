#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os

path = '/Users/bradygess/PycharmProjects/mariokartwii/characterselection/characters/fourpcharacterimages/'
for image in os.listdir(path):
    image_path = path+image
    frame = cv.imread(image_path)
    new_path = 'train_models/training_images/character_trainingimages4/'+image
    cv.imwrite(new_path,frame)





