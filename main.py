from __init__ import *
from spotify_audio import spotify_safetycheck,setup_spotifyobject,run_audio
import cv2 as cv
import time
from character_selection import character_select

def main():
    sp, coordinates = audio_setup(genre='Rock', credentials_file='credentials.txt')
    root_model = initialize_rootmodel()
    gp_info = initialize_gpinfo()
    spotify_safetycheck(sp)
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame,root_model,coordinates,gp_info)
        if gp_info.read_menu:
            character_select(frame,coordinates,root_model,gp_info)

main()
