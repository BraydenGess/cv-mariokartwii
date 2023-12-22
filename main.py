from __init__ import *
from spotify_audio import *

def main():
    spotify = setup_spotifyobject('credentials.txt')
    sp = SpotifyPlayer(spotify=spotify)
    run_audio(sp)

main()