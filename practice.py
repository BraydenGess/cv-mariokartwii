#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os

def get_newimagename(image_name):
    new_name = ''
    for i in range(len(image_name)):
        char = image_name[i]
        if char == 'X':
            new_name += '#'
        elif char == '.':
            new_name += '#'
            new_name += '.'
        else:
            new_name += char
    return 'train_models/training_images/char_trainingimages4/'+new_name


path = 'train_models/training_images/character_trainingimages4/'
for image in os.listdir(path):
    if not 'DS' in image:
        image_path = path+image
        frame = cv.imread(image_path)
        new_name = get_newimagename(image)
        cv.imwrite(new_name,frame)





