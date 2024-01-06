from spotify_audio import setup_spotifyobject
import sys

def main():
    command = sys.argv
    sp = setup_spotifyobject(file='credentials.txt')
    username = sp.current_user()['id']
    playlists = sp.user_playlists(username)
    for i, playlist in enumerate(playlists['items']):
        print(playlist['name'])
        #playlist_name = playlist['items']['name']
        #print(playlist_name)





main()