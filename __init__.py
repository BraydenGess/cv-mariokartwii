from keras.models import load_model

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

class RootModel:
    def __init__(self,coursedetect_model=None):
        self.coursedetect_model = coursedetect_model


class Coordinates:
    def __init__(self,course_coordinates=None):
        self.course_coordinates = [1020,1770,894,978]

### SET UP ###
def initialize_rootmodel():
    root_model = RootModel()
    root_model.coursedetect_model = load_model('models/coursedetectionmodel')
    return root_model

def initialize_coordinates():
    coordinates = Coordinates()
    return coordinates

