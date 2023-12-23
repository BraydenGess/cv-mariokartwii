class SpotifyPlayer():
    def __init__(self,spotify):
        self.spotify = spotify
    def queue_song(self,song):
        self.spotify.add_to_queue(uri=song,device_id=None)
        self.spotify.next_track()
    def pause(self):
        if self.spotify.current_playback()['is_playing']:
            self.spotify.pause_playback(device_id=None)
    def resume(self):
        if not self.spotify.current_playback()['is_playing']:
            self.spotify.start_playback(device_id=None)


