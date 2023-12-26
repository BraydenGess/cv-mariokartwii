from __init__ import *
from spotify_audio import *
import cv2 as cv

def main():
    spotify = setup_spotifyobject('credentials.txt')
    sp = SpotifyPlayer(spotify=spotify)
    search(sp, "YouMakeMyDreams")
    exit()
    root_model = initialize_rootmodel()
    coordinates = initialize_coordinates()
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        ret,frame = cap.read()
        run_audio(sp,frame,root_model,coordinates)

main()