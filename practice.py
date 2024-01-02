from spotify_audio import *
from __init__ import *
import time


sp, coordinates = audio_setup(genre='rock', credentials_file='credentials.txt')
t1 = time.time()
x = sp.spotify.current_playback()['item']['uri']
t2 = time.time()
t3 = time.time()
y = sp.spotify.queue()['currently_playing']['uri']
t4 = time.time()
print(t2-t1,t4-t3)
print(x,y)
exit()
