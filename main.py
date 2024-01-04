from __init__ import *
from spotify_audio import *
from graphics.championship_graphics import champ_graphics
import cv2 as cv
import time
from character_selection import character_select

def main():
    sp, coordinates = audio_setup(genre='rock', credentials_file='credentials.txt')
    root_model = initialize_rootmodel()
    cap = cv.VideoCapture(0)
    print('Ready')
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame,root_model,coordinates)
        #character_select(frame,coordinates,root_model)
main()