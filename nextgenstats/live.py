from tools.deep_learning import predict
from tools.imagemanipulation import imgtobinary
import random
import cv2 as cv
import numpy as np
import time

#Bad Moon Rising
def countdown(frame,root_model,coordinates,gp_info,sp):
    if gp_info.player_count == 2:
        coordinates = coordinates.go2_coordinates
    else:
        coordinates = coordinates.go4_coordinates
    index,confidence = predict(frame,coordinates,root_model.godetect_model,'superlightimgtobinary')
    print(index,confidence,gp_info.started)
    if (confidence>0.99):
        if index == 0:
            gp_info.started = True
            gp_info.time = time.time()
        ### Jump Around - Moonview Case
        if index == 3:
            if sp.song_queued == 'spotify:track:6JymsaWDHk2Yj4e0yNBIFH':
                sp.seek_track(ms=5500)

def nextgenstats(frame,root_model,coordinates,gp_info,sp):
    if ((gp_info.racing) and (not gp_info.started)):
        countdown(frame,root_model,coordinates,gp_info,sp)
    return 42