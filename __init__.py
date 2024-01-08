import random
from keras.models import load_model
from tools.utility import remove_newline
from collections import deque
from spotify_audio import setup_spotifyobject
import os
import sys

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
            self.is_pause = True
    def resume(self):
        if not self.spotify.current_playback()['is_playing']:
            self.spotify.start_playback(device_id=None)
            self.is_paused = False
    def min_volume(self):
        if self.support_volume:
            self.spotify.volume(volume_percent=0,device_id=None)
    def max_volume(self):
        if self.support_volume:
            self.spotify.volume(volume_percent=100,device_id=None)
    def search(self,searchQuery):
        search_results = self.spotify.search(searchQuery, 1, 0, "track")
        tracks_items = search_results['tracks']['items']
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
    def __init__(self,coursedetect_model=None,homedetect_model=None,menudetect_model=None,playercountdetect_model=None,
                 char2detect_model=None,char4detect_model=None,vehicle2detect_model=None,vehicle4detect_model=None):
        self.coursedetect_model = coursedetect_model
        self.homedetect_model = homedetect_model
        self.menudetect_model = menudetect_model
        self.playercountdetect_model = playercountdetect_model
        self.char2detect_model = char2detect_model
        self.char4detect_model = char4detect_model
        self.vehicle2detect_model = vehicle2detect_model
        self.vehicle4detect_model = vehicle4detect_model

class Coordinates:
    def __init__(self):
        self.course_coordinates = [1020,1770,894,978]
        self.home_coordinates = [135,490,80,180]
        self.menu_coordinates = [120,675,80,140]
        self.playercount_coordinates = [555, 640, 80, 140]
        self.char2_coordinates = [[150,580,435,480],[150,580,781,826]]
        self.char4_coordinates = [[155,445,452,480],[1455,1745,452,480],[155,445,834,862],[1455,1745,834,862]]
        self.vehicle2_coordinates = [[450, 925, 420, 500],[450, 925, 790, 870]]
        self.vehicle4_coordinates = [[350,855,450,500],[1053,1558,450,500],[350,855,798,848],[1053,1558,798,848]]

class Course:
    def __init__(self,course_name=None,song_queue=None,fast_staff=None,length_rank=None,AP=None,img=None):
        self.course_name = course_name
        self.song_queue = song_queue
        self.fast_staff = fast_staff
        self.length_rank = length_rank
        self.AP = AP
        self.img = img

class GP_Info():
    def __init__(self,menu_screen=None,player_count=None,players=None,colors=None,read_menu=None,racing=None,
                 rgb_colors=None,character_stats=None,vehicle_stats=None):
        self.menu_screen = menu_screen
        self.player_count = player_count
        self.players = players
        self.colors = colors
        self.read_menu = read_menu
        self.racing = racing
        self.rgb_colors = rgb_colors
        self.character_stats = character_stats
        self.vehicle_stats = vehicle_stats
    def model_switching(self,course_index):
        if course_index == 0:
            self.read_menu = True
            self.racing = False
        else:
            self.read_menu = False
            self.racing = True

class Player():
    def __init__(self,name=None,color=None,character=None,vehicle=None,score=None,place=None):
        self.name = name
        self.color = color
        self.character = character
        self.vehicle = vehicle
        self.score = score
        self.place = place

class Stat_Asset():
    def __init__(self,name=None,sp=None,wt=None,ac=None,hn=None,dr=None,off=None,mt=None,sigma=None,size=None):
        self.name = name
        self.sp = sp
        self.wt = wt
        self.ac = ac
        self.hn = hn
        self.dr = dr
        self.off = off
        self.mt = mt
        self.sigma = sigma
        self.size = size

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
    root_model.char2detect_model = load_model('models/char2detectionmodel')
    root_model.char4detect_model = load_model('models/char4detectionmodel')
    root_model.vehicle2detect_model = load_model('models/vehicle2detectionmodel')
    root_model.vehicle4detect_model = load_model('models/vehicle4detectionmodel')
    return root_model

def initialize_coordinates():
    coordinates = Coordinates()
    return coordinates

def check_imageexists(courseimage_directory,image_path):
    img_path = courseimage_directory + image_path
    if not os.path.isfile(img_path):
        print(f'Image {img_path} does not exit')
        sys.exit()
    return img_path

def add_coursedata(course_dict,file_name):
    course_infofile = 'nextgenstats/information/coursedata.csv'
    courseimage_directory = 'graphics/coursepictures/'
    f = open(course_infofile, 'r')
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        course_name = data[0]
        if course_name == course_dict[i].course_name:
            course_dict[i].fast_staff = data[1]
            course_dict[i].length_rank = data[2]
            course_dict[i].AP = data[3]
            course_dict[i].img = check_imageexists(courseimage_directory,remove_newline(data[4]))
        else:
            print(f"Races out of order or misspelled in {file_name} or {course_infofile}")
            sys.exit()
    f.close()
    return course_dict

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
    course_dict = add_coursedata(course_dict,file_name)
    return course_dict

def comma_innamecase(data):
    song_name = ''
    for i in range(len(data)-1):
        song_name += data[i]
        if i != len(data) - 2:
            song_name += ','
    return song_name

def make_songkeydict(file):
    songkey_dict = dict()
    f = open(file, 'r')
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        song_name = comma_innamecase(data)
        song_uri = remove_newline(data[-1])
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

def get_attributes(file):
    f = open(file,'r')
    datalines = f.readlines()
    asset_stats = dict()
    for i in range(1,len(datalines)):
        data = datalines[i].split(',')
        c = Stat_Asset(name=data[0],sp=data[1],wt=data[2],ac=data[3],hn=data[4],dr=data[5],off=data[6],mt=data[7],
                      sigma=data[8],size=remove_newline(data[9]))
        asset_stats[i] = c
    return asset_stats

def create_playerdict(gp_info):
    player_dict = dict()
    for i in range(len(gp_info.colors)):
        player_dict[gp_info.colors[i]] = Player(color=gp_info.colors[i])
    return player_dict

def initialize_gpinfo():
    gp_info = GP_Info(menu_screen=0,player_count=0,colors=["Orange","Blue","Red","Green"],read_menu=False,
                      rgb_colors=[(255,165,0),(0,128,255),(255,100,50),(50,255,50)],racing=False)
    gp_info.character_stats = get_attributes(file='nextgenstats/information/characterstats.csv')
    gp_info.vehicle_stats = get_attributes(file='nextgenstats/information/vehiclestats.csv')
    gp_info.player_dict = create_playerdict(gp_info)
    return gp_info



