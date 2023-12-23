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
    index,confidence = predict(frame,coordinates.course_coordinates,root_model,'imgtobinary')
    return index,confidence

def run_audio(sp,frame,root_model,coordinates):
    pause_toggle(sp,frame)
    course_name,confidence = get_course(frame,root_model,coordinates)

def search(sp):
    searchQuery = "Bad Moon Rising"
    # Search for the Song.
    searchResults = sp.spotify.search(searchQuery, 1, 0, "track")
    # Get required data from JSON response.
    tracks_dict = searchResults['tracks']
    tracks_items = tracks_dict['items']
    song = tracks_items[0]['external_urls']['spotify']
    # Open the Song in Web Browser
    song = 'spotify:track:18AXbzPzBS8Y3AkgSxzJPb'
    sp.queue_song(song)




