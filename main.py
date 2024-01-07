from __init__ import *
from spotify_audio import spotify_safetycheck,setup_spotifyobject,run_audio
import cv2 as cv
import time
from character_selection import character_select
from graphics.graphics import initialize_graphics

def main():
    sp, coordinates = audio_setup(genre='ChillRap', credentials_file='credentials.txt')
    root_model = initialize_rootmodel()
    gp_info = initialize_gpinfo()
    spotify_safetycheck(sp)
    graphics = initialize_graphics()
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame,root_model,coordinates,gp_info)
        if gp_info.read_menu:
            character_select(frame,coordinates,root_model,gp_info)
        graphics.run_graphics(gp_info)

main()
