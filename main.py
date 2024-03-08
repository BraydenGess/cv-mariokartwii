import cv2 as cv
import sys
from __init__ import *
from spotify_audio import spotify_safetycheck,run_audio
from character_selection import character_select
from graphics.graphics import initialize_graphics
from nextgenstats.live import nextgenstats

def final_graphics(graphics,sp):
    finished = False
    while not finished:
        finished = graphics.final_graphics(sp)

def main():
    sp, coordinates = audio_setup(genre='Rock', credentials_file='credentials.txt')
    root_model,gp_info = initialize_rootmodel(),initialize_gpinfo()
    graphics = initialize_graphics(screen_setting='fullscreen')
    spotify_safetycheck(sp)
    if False:
        final_graphics(graphics,sp)
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        if ret:
            run_audio(sp,frame,root_model,coordinates,gp_info)
            character_select(frame,coordinates,root_model,gp_info)
            nextgenstats(frame, root_model, coordinates, gp_info,sp)
        graphics.run_graphics(gp_info,sp,ret)

main()
