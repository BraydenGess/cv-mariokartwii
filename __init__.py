import queue
import random
from keras.models import load_model
from tools.utility import remove_newline
from collections import deque
import time
from spotify_audio import setup_spotifyobject
import pygame
import os

class SpotifyPlayer():
    def __init__(self,spotify,course_queued,playlist,songkey_dict,song_queued,is_paused,support_volume):
        self.spotify = spotify
        self.course_queued = course_queued
        self.song_queued = song_queued
        self.playlist = playlist
        self.songkey_dict = songkey_dict
        self.is_paused = is_paused
        self.support_volume = support_volume
    def pause(self):
        if self.spotify.current_playback()['is_playing']:
            self.spotify.pause_playback(device_id=None)
    def resume(self):
        if not self.spotify.current_playback()['is_playing']:
            self.spotify.start_playback(device_id=None)
    def min_volume(self):
        if self.support_volume:
            self.spotify.volume(volume_percent=0,device_id=None)
    def max_volume(self):
        if self.support_volume:
            self.spotify.volume(volume_percent=100,device_id=None)
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
            self.spotify.add_to_queue(uri=song, device_id=None)
        self.min_volume()
        for element in self.spotify.queue()['queue']:
            self.spotify.next_track()
            if songs[0] == element['uri']:
                self.max_volume()
                break
    def queue_newsong(self,course_index):
        song = self.playlist[course_index].song_queue.popleft()
        next_song = self.playlist[course_index].song_queue.popleft()
        self.queue_song(songs=[self.get_uri(song),self.get_uri(next_song)])
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
        current_playback = self.spotify.current_playback()['item']['uri']
        if ((current_playback != self.song_queued) and (self.course_queued != None)):
            self.song_queued = current_playback
            self.queue_skip()

class RootModel:
    def __init__(self,coursedetect_model=None,homedetect_model=None,menudetect_model=None,playercountdetect_model=None):
        self.coursedetect_model = coursedetect_model
        self.homedetect_model = homedetect_model
        self.menudetect_model = menudetect_model
        self.playercountdetect_model = playercountdetect_model

class Coordinates:
    def __init__(self):
        self.course_coordinates = [1020,1770,894,978]
        self.home_coordinates = [135,490,80,180]
        self.menu_coordinates = [120,675,80,140]
        self.playercount_coordinates = [120,675,80,140]

class Course:
    def __init__(self,course_name=None,song_queue=None):
        self.course_name = course_name
        self.song_queue = song_queue

class GP_Info():
    def __init__(self,menu_screen=None,player_count=None):
        self.menu_screen = menu_screen
        self.player_count = player_count


### SET UP ###
def audio_setup(genre,credentials_file):
    spotify = setup_spotifyobject(credentials_file)
    coordinates = initialize_coordinates()
    course_dict, songkey_dict = initialize_playlist(genre)
    sp = SpotifyPlayer(spotify=spotify, course_queued=None, song_queued=None, playlist=course_dict,
                       songkey_dict=songkey_dict, is_paused=False, support_volume=False)
    return sp,coordinates

def initialize_rootmodel():
    root_model = RootModel()
    root_model.coursedetect_model = load_model('models/coursedetectionmodel')
    root_model.homedetect_model = load_model('models/homedetectionmodel')
    root_model.menudetect_model = load_model('models/menudetectionmodel')
    root_model.playercountdetect_model = load_model('models/playercountdetectionmodel')
    return root_model

def initialize_coordinates():
    coordinates = Coordinates()
    return coordinates

def make_coursedict(file_name):
    course_dict = dict()
    file = 'audio/playlists/' + file_name
    f = open(file, 'r')
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        course_name = data[0]
        data[-1] = remove_newline(data[-1])
        course_songs = data[1:]
        random.shuffle(course_songs)
        q = deque()
        for j in range(len(course_songs)):
            q.append(course_songs[j])
        course_dict[i - 1] = Course(course_name=course_name, song_queue=q)
    f.close()
    return course_dict

def make_songkeydict(file):
    songkey_dict = dict()
    f = open(file, 'r')
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        song_name = data[0]
        song_uri = remove_newline(data[1])
        songkey_dict[song_name] = song_uri
    f.close()
    return songkey_dict

def initialize_playlist(playlist_name):
    songkey_dict = make_songkeydict(file = 'audio/song_uri.csv')
    course_playlists = os.listdir('audio/playlists/')
    file_name = playlist_name+'.csv'
    if file_name in course_playlists:
        course_dict = make_coursedict(file_name)
    else:
        raise Exception("Not Valid Playlist")
    return course_dict,songkey_dict

def initialize_gpinfo():
    gp_info = GP_Info(menu_screen=0,player_count=0)
    return gp_info

def initialize_graphics():
    pygame.init()
    screen = pygame.display.set_mode()
    x,y = screen.get_size()
    display_surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Beerio")
    return display_surface,x,y


