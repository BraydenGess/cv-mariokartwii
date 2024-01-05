from tools.imagemanipulation import *
from sklearn.model_selection import train_test_split
from keras.layers import Dense
from keras.models import Sequential
import numpy as np
import tensorflow as tf
from keras.models import load_model
from __init__ import *
from spotify_audio import *
from graphics.championship_graphics import champ_graphics
import cv2 as cv
import time
from character_selection import character_select
from graphics.graphics import initialize_graphics

def graphics_quit():
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()

def main():
    graphics = initialize_graphics()
    gp_info = initialize_gpinfo()
    while True:
        graphics.run_graphics(gp_info)

main()
