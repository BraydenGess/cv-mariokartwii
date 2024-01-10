import cv2 as cv
import os
from tools.imagemanipulation import *



new_directory = 'train_models/training_images/scoring_trainingimages/'
for image_name in os.listdir(new_directory):
    new_path = new_directory+image_name
    img = cv.imread(new_path)
    cv.imwrite(new_path,imgtobinary(img))



