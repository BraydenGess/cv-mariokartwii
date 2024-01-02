#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np

def main():
    cap = cv.VideoCapture(0)
    count = 0
    while cap.isOpened():
        ret,frame = cap.read()
        file_name = 'img' + str(count) + '.png'
        cv.imwrite(file_name,imgtobinary(frame))
        count += 1
        print(count)
        time.sleep(0.1)
        if count == 5:
            exit()

def main2():
    array = np.array([1,2,3],dtype=int)
    array2 = np.array([1, 2, 3], dtype=int)
    confidence = np.argmax(array)
    confidence2 = np.argmax(array2)
    if confidence == confidence2 != 2:
        print('True')

main2()





