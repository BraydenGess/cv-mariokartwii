import os
import random
import sys
from keras.models import load_model
from tools.utility import remove_newline
from collections import deque
from spotify_audio import setup_spotifyobject
from urllib.request import urlopen
from tools.deep_learning import *

class SpotifyPlayer():
    def __init__(self,spotify,course_queued,playlist,songkey_dict,song_queued,is_paused,support_volume,img_str):
        self.spotify = spotify
        self.course_queued = course_queued
        self.song_queued = song_queued
        self.playlist = playlist
        self.songkey_dict = songkey_dict
        self.is_paused = is_paused
        self.support_volume = support_volume
        self.img_str = img_str
    def pause(self):
        if self.spotify.current_playback()['is_playing']:
            self.spotify.pause_playback(device_id=None)
            self.is_paused = True
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
    def seek_track(self,ms):
        self.spotify.seek_track(ms)
    def search(self,searchQuery):
        search_results = self.spotify.search(searchQuery, 1, 0, "track")
        tracks_items = search_results['tracks']['items']
        song_uri,song_name = tracks_items[0]['uri'],tracks_items[0]['name']
        image_url = tracks_items[0]['album']['images'][0]['url']
        search_song = Song(song_name=song_name,uri=song_uri,img=image_url)
        return search_song
    def get_song(self,song):
        if song in self.songkey_dict:
            return self.songkey_dict[song]
        return self.search(song)
    def skip_tosong(self,song_uri):
        self.min_volume()
        user_queue = self.spotify.queue()['queue']
        for element in user_queue:
            self.spotify.next_track()
            if song_uri == element['uri']:
                self.max_volume()
                break
    def queue_songs(self,songs):
        for song in songs:
            self.spotify.add_to_queue(uri=song.uri, device_id=None)
        self.skip_tosong(song_uri=songs[0].uri)
    def queue_newsong(self,course_index):
        song = self.playlist[course_index].song_queue.popleft()
        next_song = self.playlist[course_index].song_queue.popleft()
        song_queued = self.get_song(song)
        self.queue_songs(songs=[song_queued,self.get_song(next_song)])
        self.course_queued = course_index
        self.song_queued = song_queued
        self.img_str = urlopen(song_queued.img).read()
        self.playlist[self.course_queued].song_queue.append(song)
        self.playlist[self.course_queued].song_queue.appendleft(next_song)
    def queue_skip(self):
        next_song = self.playlist[self.course_queued].song_queue.popleft()
        if next_song == self.song_queued.song_name:
            song = self.playlist[self.course_queued].song_queue.popleft()
            song = self.get_song(song)
            self.spotify.add_to_queue(uri=song.uri, device_id=None)
            self.playlist[self.course_queued].song_queue.appendleft(song)
            self.playlist[self.course_queued].song_queue.append(next_song)
        else:
            self.playlist[self.course_queued].song_queue.appendleft(next_song)

    def auto_skip(self):
        current_playback = self.spotify.current_playback()['item']['uri']
        if ((self.course_queued != None) and (current_playback != self.song_queued.uri)):
            t = self.spotify.track(current_playback)
            current_playback = Song(song_name=t['name'],uri=current_playback,img=t['album']['images'][0]['url'])
            self.song_queued = current_playback
            self.img_str = urlopen(self.song_queued.img).read()
            self.queue_skip()

class RootModel:
    def __init__(self,coursedetect_model=None,homedetect_model=None,menudetect_model=None,playercountdetect_model=None,
                 char2detect_model=None,char4detect_model=None,vehicle2detect_model=None,vehicle4detect_model=None,
                 godetect_model=None,scoringdetect_model=None,plusdetect_model=None):
        self.coursedetect_model = coursedetect_model
        self.homedetect_model = homedetect_model
        self.menudetect_model = menudetect_model
        self.playercountdetect_model = playercountdetect_model
        self.char2detect_model = char2detect_model
        self.char4detect_model = char4detect_model
        self.vehicle2detect_model = vehicle2detect_model
        self.vehicle4detect_model = vehicle4detect_model
        self.godetect_model = godetect_model
        self.scoringdetect_model = scoringdetect_model
        self.plusdetect_model = plusdetect_model

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
        self.go2_coordinates = [740,1140,200,360]
        self.go4_coordinates = [294, 694, 200, 360]
        self.scoring_coordinates = []
        self.plus_coordinates = []
    def set_scoringcoordinates(self):
        [x0, x1, y0, y1] = [610, 1090, 73, 149]
        boxheight = y1 - y0
        for i in range(12):
            y2 = y0 + (boxheight * i)
            y3 = y2 + boxheight
            self.scoring_coordinates.append([x0, x1, y2, y3])
    def set_pluscoordinates(self):
        [x0, x1, x2, x3] = [1210, 1255, 1255, 1300]
        [y0, y1] = [73, 149]
        for i in range(12):
            xc1 = x0
            xc2 = x1
            if i >= 3:
                xc1 = x2
                xc2 = x3
            y2 = y0 + ((y1 - y0) * i)
            y3 = y2 + (y1 - y0)
            self.plus_coordinates.append([xc1, xc2, y2, y3])

class Course:
    def __init__(self,course_name=None,song_queue=None,fast_staff=None,length_rank=None,AP=None,CPI=None,
                 img=None,txtcolor=None,regular=None,elixir=None):
        self.course_name = course_name
        self.song_queue = song_queue
        self.fast_staff = fast_staff
        self.length_rank = length_rank
        self.AP = AP
        self.CPI = CPI
        self.regular = regular
        self.elixir = elixir
        self.img = img
        self.txtcolor = txtcolor

class GP_Info():
    def __init__(self,menu_screen=None,player_count=None,players=None,colors=None,read_menu=None,racing=None,
                 rgb_colors=None,character_stats=None,vehicle_stats=None,started=None,time=None,
                 score_read=None,score_scan=None,scoreboard=None,temp_scoreboard=None,gp_courses=None):
        self.menu_screen = menu_screen
        self.player_count = player_count
        self.players = players
        self.colors = colors
        self.read_menu = read_menu
        self.racing = racing
        self.started = started
        self.rgb_colors = rgb_colors
        self.character_stats = character_stats
        self.vehicle_stats = vehicle_stats
        self.time = time
        ### Scoreboard Assets
        self.score_scan = score_scan
        self.score_read = score_read
        self.scoreboard = scoreboard
        self.temp_scoreboard = temp_scoreboard
        self.score_dict = {1: 15, 2: 12, 3: 10, 4: 8, 5: 7, 6: 6, 7: 5, 8: 4, 9: 3, 10: 2, 11: 1, 12: 0}
        self.gp_courses = gp_courses
    def model_switching(self,course_index):
        if course_index == 0:
            self.racing = False
            self.started = False
            self.read_menu = True
            self.menu_screen = 0
            for color in self.colors:
                self.players[color].vehicle = None
            self.gp_courses = []
        else:
            self.read_menu = False
            self.started = False
            self.racing = True
            self.score_scan = True
            self.gp_courses.append(course_index)
    def get_pluscount(self,frame,root_model,coordinates):
        plus_count = 0
        for i in range(12):
            index, confidence = predict(frame, coordinates.plus_coordinates[i], root_model.plusdetect_model,
                                      'sharpimgtobinary')
            if ((index==1)and(confidence>0.9)):
                plus_count += 1
        return plus_count
    def control_scan(self,frame,root_model,coordinates):
        plus_count = self.get_pluscount(frame,root_model,coordinates)
        if not self.score_read:
            if plus_count >= 3:
                self.score_read = True
                self.temp_scoreboard = []
                for i in range(12):
                    self.temp_scoreboard.append([25, -1])
        else:
            if plus_count <= 3:
                self.score_read = False
                self.score_scan = False
                return True
        return False
    def read_scoreboard(self,frame,root_model,coordinates):
        for i in range(len(coordinates.scoring_coordinates)):
            prediction = full_predict(frame, coordinates.scoring_coordinates[i], root_model.scoringdetect_model,
                                          'switch')
            index = np.argmax(prediction[0][:-1])
            confidence = prediction[0][index]
            if confidence >= self.temp_scoreboard[i][1]:
                self.temp_scoreboard[i][0] = index
                self.temp_scoreboard[i][1] = confidence
    def update_scoreboard(self):
        if self.scoreboard[0][1] != 0:
            for i in range(len(self.temp_scoreboard)):
                index = self.temp_scoreboard[i][0]
                for j in range(len(self.scoreboard)):
                    character = self.scoreboard[j][0]
                    if index == character:
                        self.scoreboard[j][1] += self.score_dict[i+1]
        else:
            for i in range(len(self.temp_scoreboard)):
                index = self.temp_scoreboard[i][0]
                self.scoreboard[i][0] = index
                if index == 25:
                    self.scoreboard[i][0] = random.randint(0,24)
                self.scoreboard[i][1] += self.score_dict[i+1]
        self.scoreboard.sort(key=lambda x:x[1],reverse=True)
    def initialize_scoreboard(self):
        cpu_scoreboard = []
        player_scoreboard = []
        available_players = []
        for i in range(24):
            available_players.append(i)
        for i in range(self.player_count-1,-1,-1):
            p = self.players[self.colors[i]]
            character_index = self.character_stats[p.character].index
            player_scoreboard.append([character_index,0])
            if character_index in available_players:
                available_players.remove(character_index)
        random.shuffle(available_players)
        for i in range(12-self.player_count):
            cpu_scoreboard.append([available_players[i],0])
        self.scoreboard = cpu_scoreboard+player_scoreboard
class Player():
    def __init__(self,name=None,color=None,character=None,vehicle=None,score=None,place=None):
        self.name = name
        self.color = color
        self.character = character
        self.vehicle = vehicle
        self.score = score
        self.place = place

class Stat_Asset():
    def __init__(self,name=None,index = None,sp=None,wt=None,ac=None,hn=None,dr=None,off=None,mt=None,sigma=None,size=None):
        self.name = name
        self.index = index
        self.sp = sp
        self.wt = wt
        self.ac = ac
        self.hn = hn
        self.dr = dr
        self.off = off
        self.mt = mt
        self.sigma = sigma
        self.size = size

class Song():
    def __init__(self,song_name=None,uri=None,img=None):
        self.song_name = song_name
        self.uri = uri
        self.img = img

### SET UP ###
def audio_setup(genre,credentials_file):
    spotify = setup_spotifyobject(credentials_file)
    coordinates = initialize_coordinates()
    course_dict, songkey_dict = initialize_playlist(genre)
    sp = SpotifyPlayer(spotify=spotify, course_queued=None, song_queued=None, playlist=course_dict,
                       songkey_dict=songkey_dict, is_paused=False, support_volume=False,img_str=None)
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
    root_model.godetect_model = load_model('models/godetectionmodel')
    root_model.scoringdetect_model = load_model('models/scoringdetectionmodel2')
    root_model.plusdetect_model = load_model('models/plusdetectionmodel')
    return root_model

def initialize_coordinates():
    coordinates = Coordinates()
    coordinates.set_scoringcoordinates()
    coordinates.set_pluscoordinates()
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
            course_dict[i].CPI = data[4]
            course_dict[i].img = check_imageexists(courseimage_directory,data[5])
            course_dict[i].txtcolor = remove_newline(data[6])
        else:
            print(f"Races out of order or misspelled in {file_name} or {course_infofile}")
            sys.exit()
    f.close()
    return course_dict

def make_coursedict(file_name):
    course_dict = dict()
    course_indexlookup = dict()
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
        course_dict[i - 1] = Course(course_name=course_name, song_queue=q,elixir=[],regular=[])
        course_indexlookup[course_name] = i-1
    f.close()
    course_dict = add_coursedata(course_dict,file_name)
    return course_dict,course_indexlookup

def make_songkeydict(file):
    songkey_dict = dict()
    f = open(file, 'r')
    datalines = f.readlines()
    for i in range(1, len(datalines)):
        data = datalines[i].split(',')
        song_name = data[0]
        song_uri = remove_newline(data[1])
        song_img = remove_newline(data[2])
        song = Song(song_name=song_name,uri=song_uri,img=song_img)
        songkey_dict[song_name] = song
    f.close()
    return songkey_dict

def initialize_playlist(playlist_name):
    songkey_dict = make_songkeydict(file = 'audio/song_uri.csv')
    course_playlists = os.listdir('audio/playlists/')
    file_name = playlist_name+'.csv'
    if file_name not in course_playlists:
        raise Exception("Not Valid Playlist")
    course_dict,null = make_coursedict(file_name)
    return course_dict,songkey_dict

def get_attributes(file):
    f = open(file,'r')
    datalines = f.readlines()
    asset_stats = dict()
    for i in range(1,len(datalines)):
        data = datalines[i].split(',')
        c = Stat_Asset(name=data[0],index=i-1,sp=data[1],wt=data[2],ac=data[3],hn=data[4],dr=data[5],off=data[6],mt=data[7],
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
                      rgb_colors=[(255,165,0),(0,128,255),(255,100,50),(50,255,50)],racing=False,started=False,time=0)
    gp_info.character_stats = get_attributes(file='nextgenstats/information/characterstats.csv')
    gp_info.vehicle_stats = get_attributes(file='nextgenstats/information/vehiclestats.csv')
    gp_info.players = create_playerdict(gp_info)
    gp_info.score_read = False
    gp_info.score_scan = False
    return gp_info



