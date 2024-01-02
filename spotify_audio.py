import spotipy
from spotipy.oauth2 import SpotifyClientCredentials,SpotifyOAuth
from tools.utility import *
from tools.deep_learning import predict


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

def pause_toggle(sp,frame):
    return None

def get_course(frame,root_model,coordinates):
    index,confidence = predict(frame,coordinates.course_coordinates,root_model.coursedetect_model,'imgtobinary')
    if confidence >= 0.95:
        return index,confidence
    return 33,0

def course_tracker(sp,course_index):
    if course_index == 33:
        sp.course = course_index
        sp.course_count = 0
    if course_index == sp.course:
        sp.course_count += 1
    else:
        sp.course = course_index
        sp.course_count = 0

def play_music(sp,course_index):
    if sp.course_count == 2:
        if sp.course != sp.course_queued:
            sp.queue_newsong(course_index)

def run_audio(sp,frame,root_model,coordinates):
    pause_toggle(sp,frame)
    course_index,confidence = get_course(frame,root_model,coordinates)
    course_tracker(sp,course_index)
    play_music(sp,course_index)
    sp.auto_skip()






