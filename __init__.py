import queue
import random
from keras.models import load_model
from tools.utility import remove_newline

class SpotifyPlayer():
    def __init__(self,spotify,course,course_count,course_queued,playlist,songkey_dict,song_queued):
        self.spotify = spotify
        self.course = course
        self.course_count = course_count
        self.course_queued = course_queued
        self.song_queued = song_queued
        self.playlist = playlist
        self.songkey_dict = songkey_dict
    def queue_song(self,song):
        self.spotify.add_to_queue(uri=song,device_id=None)
        self.spotify.next_track()
    def pause(self):
        if self.spotify.current_playback()['is_playing']:
            self.spotify.pause_playback(device_id=None)
    def resume(self):
        if not self.spotify.current_playback()['is_playing']:
            self.spotify.start_playback(device_id=None)
    def search(self,song_name):
        searchQuery = song_name
        searchResults = self.spotify.search(searchQuery, 1, 0, "track")
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song_uri = tracks_items[0]['external_urls']['spotify']
        return song_uri
    def queue_newsong(self,course_index):
        song = self.playlist[course_index].song_queue.get()
        song_uri = None
        if song in self.songkey_dict:
            song_uri = self.songkey_dict[song]
        else:
            song_uri = self.search(song)
        self.queue_song(song_uri)
        self.course_queued = course_index
        self.song_queued = song_uri
        self.playlist[course_index].song_queue.put(song)
    def auto_skip(self):
        if self.spotify.current_playback()['item']['uri'] != self.song_queued:
            if self.course_queued != None:
                self.queue_newsong(self.course_queued)

class RootModel:
    def __init__(self,coursedetect_model=None):
        self.coursedetect_model = coursedetect_model


class Coordinates:
    def __init__(self,course_coordinates=None):
        self.course_coordinates = [1020,1770,894,978]

class Course:
    def __init__(self,course_name=None,song_queue=None):
        self.course_name = course_name
        self.song_queue = song_queue

### SET UP ###
def initialize_rootmodel():
    root_model = RootModel()
    root_model.coursedetect_model = load_model('models/coursedetectionmodel')
    return root_model

def initialize_coordinates():
    coordinates = Coordinates()
    return coordinates

def initialize_playlist(playlist_name):
    course_dict = dict()
    file = 'audio/playlists/'+playlist_name+'.csv'
    f = open(file,'r')
    datalines = f.readlines()
    for i in range(1,len(datalines)):
        data = datalines[i].split(',')
        course_name = data[0]
        data[-1] = remove_newline(data[-1])
        course_songs = data[1:]
        random.shuffle(course_songs)
        q = queue.Queue()
        for j in range(len(course_songs)):
            q.put(course_songs[j])
        course_dict[i-1] = Course(course_name=course_name,song_queue=q)
    f.close()
    songkey_dict = dict()
    f = open('audio/song_uri.csv','r')
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        song_name = data[0]
        song_uri = remove_newline(data[1])
        songkey_dict[song_name] = song_uri
    return course_dict,songkey_dict


