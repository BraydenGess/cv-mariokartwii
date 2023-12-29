from __init__ import *
from spotify_audio import *
import cv2 as cv
import time

def main():
    spotify = setup_spotifyobject('credentials.txt')
    sp = SpotifyPlayer(spotify=spotify,course=33,course_count=0)
    root_model = initialize_rootmodel()
    coordinates = initialize_coordinates()
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame,root_model,coordinates)

def main2():
    sp,coordinates = audio_setup(genre='throwback-pop',credentials_file='credentials.txt')
    root_model = initialize_rootmodel()
    frame = cv.imread('/Users/bradygess/PycharmProjects/mariokartwii/audio/traincourserecognition/coursenametrainingimages/Opening1.png')
    t1 = time.time()
    while True:
        t2 = time.time()
        if t2-t1 > 10:
            frame = cv.imread(
                '/Users/bradygess/PycharmProjects/mariokartwii/audio/traincourserecognition/coursenametrainingimages/PeachBeach1.png')
        if t2-t1 > 25:
            frame = cv.imread(
                '/Users/bradygess/PycharmProjects/mariokartwii/audio/traincourserecognition/coursenametrainingimages/WariosGoldMine1.png')
        run_audio(sp,frame,root_model,coordinates)

main2()