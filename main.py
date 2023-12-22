from __init__ import *
from spotify_audio import *
import cv2 as cv

def main():
    spotify = setup_spotifyobject('credentials.txt')
    sp = SpotifyPlayer(spotify=spotify)
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame)

main()