from spotify_audio import *
from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary

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
        if count == 15:
            exit()

main()





