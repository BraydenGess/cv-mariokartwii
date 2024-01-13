import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
from tools.utility import *
from tools.deep_learning import predict
import cv2 as cv

def spotify_safetycheck(sp):
    warning = False
    safe = False
    while not safe:
        if sp.spotify.current_playback() != None:
            safe = True
            sp.support_volume = sp.spotify.current_playback()['device']['supports_volume']
            print('Supports Volume')
        elif not warning:
            print('Activate Device')
            warning = True
    print('Ready')

def setup_spotifyobject(file):
    f = open(file,'r')
    cred_dict = {'username':'None','client_id':'None','client_secret':'None','redirect_uri':'None'}
    for cred in f.readlines():
        [label,key] = cred.split(' ')
        if label in cred_dict:
            cred_dict[label] = remove_newline(key)
    scope = 'user-modify-playback-state user-read-playback-state'
    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id=cred_dict['client_id'],
                                    client_secret=cred_dict['client_secret'],redirect_uri = cred_dict['redirect_uri'],
                                    username=cred_dict['username']))
    return spotify

def pause_toggle(sp,frame,root_model,coordinates):
    index,confidence = predict(frame,coordinates.home_coordinates,root_model.homedetect_model,'imgtobinary')
    if confidence >= 0.8:
        if index == 0:
            if sp.is_paused:
                sp.resume()
        else:
            if not sp.is_paused:
                sp.pause()

def double_verifycourse(coordinates,root_model,index,alpha):
    cap = cv.VideoCapture(0)
    ret, next_frame = cap.read()
    if not ret:
        return False
    index2, confidence2 = predict(next_frame, coordinates.course_coordinates, root_model.coursedetect_model,
                                  'imgtobinary')
    if ((index2==index)and(confidence2>alpha)):
         return True
    return False

def get_course(frame,root_model,coordinates):
    index,confidence = predict(frame,coordinates.course_coordinates,root_model.coursedetect_model,'imgtobinary')
    if ((index == 0) and (confidence > 0.87)):
        if double_verifycourse(coordinates,root_model,index,alpha=0.87):
            return index,confidence
    if ((index!=33)and(confidence>0.95)):
        if double_verifycourse(coordinates,root_model,index,alpha=0.95):
            return index,confidence
    return 33,0

def play_music(frame,root_model,coordinates,sp,gp_info):
    course_index,confidence = get_course(frame,root_model,coordinates)
    if ((course_index != 33)and(course_index != sp.course_queued)):
        sp.queue_newsong(course_index)
        gp_info.model_switching(course_index,gp_info)

def run_audio(sp,frame,root_model,coordinates,gp_info):
    pause_toggle(sp,frame,root_model,coordinates)
    if (not gp_info.read_menu):
        play_music(frame,root_model,coordinates,sp,gp_info)
    #sp.auto_skip() - needs some fixing