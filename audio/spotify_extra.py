from spotify_audio import setup_spotifyobject
from __init__ import make_songkeydict
import sys
import random
import os

def check_playlistexists(playlists,target_playlist):
    for i, playlist in enumerate(playlists['items']):
        if target_playlist == playlist['name']:
            return True,playlist
    print('Playlist Not Found')
    print("Hint: Make sure playlist is public and added to username's profile")
    sys.exit()

def check_length(playlist):
    min_length = 66
    playlist_length = playlist['tracks']['total']
    if playlist_length < min_length:
        print(f'WARNING -- Playlist too short')
        print(f'Number of tracks must exceed {min_length} to avoid duplicates')
    return playlist_length

def get_tracksfromplaylist(sp,playlist):
    tracks = []
    raw_tracks = sp.playlist_tracks(playlist_id=playlist['uri'])
    for track in raw_tracks['items']:
        name = track['track']['name']
        uri = track['track']['uri']
        duration = track['track']['duration_ms']
        tracks.append([name,uri,duration])
    return tracks

def get_courses(file):
    f = open(file,'r')
    courses = []
    datalines = f.readlines()
    for i in range(1,len(datalines)):
        data = datalines[i].split(',')
        course_name = data[0]
        length_rank = int(data[2])
        courses.append([course_name,length_rank,i])
    return courses

def make_playlist(tracks,courses,playlist_length):
    tracks.sort(key=lambda x:x[2])
    courses.sort(key=lambda x:x[1])
    courses = courses[:15] + [["Opening",0,0]] + courses[15:]
    songs_per = max(playlist_length//len(courses),2)
    for i in range(len(courses)):
        for j in range(songs_per):
            iter = ((len(tracks)-1)-j-(i*songs_per))
            rand = random.randint(0,len(courses))
            index = iter
            if index < 0:
                index = rand
            courses[i].append(tracks[index])
    return courses,tracks

def playlist_input(file_name):
    raw_input = input('Playlist already exists. (r) rename/(o) overwrite/(q) quit\n')
    if raw_input == 'r':
        new_input = input('Enter the new playlist name\n')
        file_name = new_input + '.csv'
    elif raw_input == 'o':
        return file_name,True
    else:
        print('Quit')
        sys.exit()
    return file_name,False

def write_newplaylist(courses,target_playlist):
    file_name = target_playlist + '.csv'
    playlist_folder = 'audio/playlists/'
    while file_name in os.listdir(playlist_folder):
        file_name,overwrite = playlist_input(file_name)
        if overwrite:
            break
    file_path = playlist_folder + file_name
    uris = []
    f = open(file_path,'w')
    courses.sort(key=lambda x:x[2])
    f.write('CourseNames,Songs\n')
    for course in courses:
        course_name = course[0]
        f.write(course_name)
        f.write(',')
        for i in range(3,len(course)):
            song_name = course[i][0]
            uri = course[i][1]
            uris.append([song_name,uri])
            f.write(song_name)
            if i != len(course)-1:
                f.write(',')
        f.write('\n')
    f.close()
    uri_path = 'audio/song_uri.csv'
    songkey_dict = make_songkeydict(uri_path)
    f = open(uri_path,'a')
    for element in uris:
        song_name = element[0]
        if song_name not in songkey_dict:
            f.write('\n')
            f.write(element[0])
            f.write(',')
            f.write(element[1])
            songkey_dict[element[0]] = element[1]

def make_newplaylist(sp,username,target_playlist):
    playlists = sp.user_playlists(username)
    found,playlist = check_playlistexists(playlists,target_playlist)
    playlist_length = check_length(playlist)
    if found:
        tracks = get_tracksfromplaylist(sp,playlist)
        courses = get_courses(file='nextgenstats/information/coursedata.csv')
        courses,tracks = make_playlist(tracks, courses,playlist_length)
        write_newplaylist(courses,target_playlist)

def get_arguements(argv,sp):
    command = argv[1]
    if command == 'newplaylist':
        target_playlist = argv[2]
        username = sp.current_user()['id']
        if len(command) >= 4:
            username = argv[3]
    return command,username,target_playlist

def main():
    sp = setup_spotifyobject(file='credentials.txt')
    command,username,target_playlist = get_arguements(sys.argv,sp)
    if command == 'newplaylist':
        make_newplaylist(sp,username,target_playlist)

main()