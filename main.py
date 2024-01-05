from __init__ import *
from spotify_audio import *
from graphics.championship_graphics import champ_graphics
import cv2 as cv
import time
from character_selection import character_select

def spotify_safetycheck(sp):
    warning = False
    safe = False
    while not safe:
        if sp.spotify.current_playback() != None:
            safe = True
            sp.support_volume = sp.spotify.current_playback()['device']['supports_volume']
        elif not warning:
            print('Activate Device')
            warning = True
    print('Ready')

def main():
    sp, coordinates = audio_setup(genre='Rock', credentials_file='credentials.txt')
    root_model = initialize_rootmodel()
    gp_info = None
    spotify_safetycheck(sp)
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame,root_model,coordinates)
        character_select(frame,coordinates,root_model,gp_info)

main()
