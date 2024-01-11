from tools.deep_learning import predict
from tools.imagemanipulation import imgtobinary
import random
import cv2 as cv
import numpy as np
import time

def countdown(frame,root_model,coordinates,gp_info,sp):
    new_coordinates = coordinates.go4_coordinates
    if gp_info.player_count == 2:
        new_coordinates = coordinates.go2_coordinates
    index,confidence = predict(frame,new_coordinates,root_model.godetect_model,'superlightimgtobinary')
    if (confidence>0.99):
        if index == 0:
            gp_info.started = True
            gp_info.time = time.time()
        ### Jump Around - Moonview Case
        if index == 3:
            if sp.song_queued.song_name == 'Jump Around':
                sp.seek_track(ms=5500)

def nextgenstats(frame,root_model,coordinates,gp_info,sp):
    if ((gp_info.racing) and (not gp_info.started)):
        countdown(frame,root_model,coordinates,gp_info,sp)
    return 42