from spotify_audio import setup_spotifyobject
import sys

def check_playlistexists(playlists,target_playlist):
    for i, playlist in enumerate(playlists['items']):
        if target_playlist == playlist['name']:
            return True,playlist
    print('Playlist Not Found')
    print("Hint: Make sure playlist is public and added to username's profile")
    sys.exit()
    return False,None
def make_newplaylist(sp,username,target_playlist):
    playlists = sp.user_playlists(username)
    found,playlist = check_playlistexists(playlists,target_playlist)
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
    print(command,username,target_playlist)
    if command == 'newplaylist':
        make_newplaylist(sp,username,target_playlist)






main()