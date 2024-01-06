from spotify_audio import setup_spotifyobject
import sys

def check_playlistexists(playlists,target_playlist):
    for i, playlist in enumerate(playlists['items']):
        if target_playlist == playlist['name']:
            return True,playlist
    print('Playlist Not Found')
    print("Hint: Make sure playlist is public and added to username's profile")
    sys.exit()

def check_length(playlist):
    playlist_length = playlist['tracks']['total']
    if playlist_length < 66:
        print('Playlist too short. Number of tracks must exceed 66')
        sys.exit()
def make_newplaylist(sp,username,target_playlist):
    playlists = sp.user_playlists(username)
    found,playlist = check_playlistexists(playlists,target_playlist)
    check_length(playlist)
    if found:
        tracks = sp.playlist_tracks(playlist_id=playlist['uri'])
        for track in tracks['items']:
            name = track['track']['name']
            uri = track['track']['uri']
            print(name,uri)
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