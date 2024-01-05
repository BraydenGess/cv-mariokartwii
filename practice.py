#from spotify_audio import *
#from __init__ import *
import time
import cv2 as cv
from tools.imagemanipulation import imgtobinary
import numpy as np
import os
from spotify_audio import *


sp = setup_spotifyobject(file='credentials.txt')
print(sp.current_playback()['item']['uri'])