from tools.deep_learning import predict

class GP_Info():
    def __init__(self,menu_screen=None):
        self.menu_screen = menu_screen
def player_count(frame,coordinates,root_model):
    return 42

def menu_control(frame,coordinates,root_model):
    index,confidence = predict(frame,coordinates.menu_coordinates,root_model.menudetect_model,'sharpimgtobinary')
    if ((index==2)and(confidence>0.95)):
        player_count(frame,coordinates,root_model)
    return 42

def character_select(frame,coordinates,root_model):
    menu_control(frame,coordinates,root_model)
    return 42