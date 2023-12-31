import queue
import random
from keras.models import load_model
from tools.utility import remove_newline
from collections import deque
import time
from spotify_audio import setup_spotifyobject


class SpotifyPlayer():
    def __init__(self,spotify,course,course_count,course_queued,playlist,songkey_dict,song_queued):
        self.spotify = spotify
        self.course = course
        self.course_count = course_count
        self.course_queued = course_queued
        self.song_queued = song_queued
        self.playlist = playlist
        self.songkey_dict = songkey_dict
    def pause(self):
        if self.spotify.current_playback()['is_playing']:
            self.spotify.pause_playback(device_id=None)
    def resume(self):
        if not self.spotify.current_playback()['is_playing']:
            self.spotify.start_playback(device_id=None)
    def search(self,searchQuery):
        searchResults = self.spotify.search(searchQuery, 1, 0, "track")
        tracks_items = searchResults['tracks']['items']
        song_uri = tracks_items[0]['external_urls']['spotify']
        return song_uri
    def get_uri(self,song):
        if song in self.songkey_dict:
            song_uri = self.songkey_dict[song]
        else:
            song_uri = self.search(song)
        return song_uri
    def queue_song(self,songs):
        for song in songs:
            self.spotify.add_to_queue(uri=self.get_uri(song), device_id=None)
        for element in self.spotify.queue()['queue']:
            self.spotify.next_track()
            if songs[0] == element['uri']:
                break
    def queue_newsong(self,course_index):
        song = self.playlist[course_index].song_queue.popleft()
        next_song = self.playlist[course_index].song_queue.popleft()
        self.queue_song(songs=[song,next_song])
        self.course_queued = course_index
        self.song_queued = self.get_uri(song)
        self.playlist[self.course_queued].song_queue.append(song)
        self.playlist[self.course_queued].song_queue.appendleft(next_song)
    def queue_skip(self):
        next_song = self.playlist[self.course_queued].song_queue.popleft()
        if self.get_uri(next_song) == self.song_queued:
            song = self.playlist[self.course_queued].song_queue.popleft()
            song_uri = self.get_uri(song)
            self.spotify.add_to_queue(uri=song_uri, device_id=None)
            self.playlist[self.course_queued].song_queue.appendleft(song)
            self.playlist[self.course_queued].song_queue.append(next_song)
        else:
            self.playlist[self.course_queued].song_queue.appendleft(next_song)
    def auto_skip(self):
        current_playback = self.spotify.queue()['currently_playing']['uri']
        if ((current_playback != self.song_queued) and (self.course_queued != None)):
            self.song_queued = current_playback
            self.queue_skip()

class RootModel:
    def __init__(self,coursedetect_model=None):
        self.coursedetect_model = coursedetect_model

class Coordinates:
    def __init__(self):
        self.course_coordinates = [1020,1770,894,978]

class Course:
    def __init__(self,course_name=None,song_queue=None):
        self.course_name = course_name
        self.song_queue = song_queue

### SET UP ###
def audio_setup(genre,credentials_file):
    spotify = setup_spotifyobject(credentials_file)
    coordinates = initialize_coordinates()
    course_dict, songkey_dict = initialize_playlist(genre)
    sp = SpotifyPlayer(spotify=spotify, course=33, course_count=0, course_queued=None,
                       song_queued=None, playlist=course_dict, songkey_dict=songkey_dict)
    return sp,coordinates

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
        q = deque()
        for j in range(len(course_songs)):
            q.append(course_songs[j])
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


