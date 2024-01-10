import cv2 as cv
from __init__ import *
from spotify_audio import spotify_safetycheck,run_audio
from character_selection import character_select
from graphics.graphics import initialize_graphics
from nextgenstats.live import nextgenstats

def safe_pull(cap):
    ret,frame = cap.read()
    if not ret:
        print('No Input')
        sys.exit()
    return frame

def main():
    sp, coordinates = audio_setup(genre='Rock', credentials_file='credentials.txt')
    root_model,gp_info = initialize_rootmodel(),initialize_gpinfo()
    graphics = initialize_graphics(screen_setting='fullscreen')
    spotify_safetycheck(sp)
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        frame = safe_pull(cap)
        run_audio(sp,frame,root_model,coordinates,gp_info)
        character_select(frame,coordinates,root_model,gp_info)
        nextgenstats(frame, root_model, coordinates, gp_info,sp)
        graphics.run_graphics(gp_info, sp)

main()
