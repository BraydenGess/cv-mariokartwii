from tools.deep_learning import predict

class GP_Info():
    def __init__(self,menu_screen=None,player_count=None):
        self.menu_screen = menu_screen
        self.player_count = player_count
def player_count(frame,coordinates,root_model,gp_info):
    index,confidence = predict(frame,coordinates.playercount_coordinates,
                               root_model.playercountdetect_model,'sharpimgtobinary')
    if (index)>=1 and (confidence>0.8):
        gp_info.player_count = index+1
    return gp_info

def menu_control(frame,coordinates,root_model,gp_info):
    index,confidence = predict(frame,coordinates.menu_coordinates,root_model.menudetect_model,'sharpimgtobinary')
    if confidence>0.95:
        if index != 0:
            gp_info.menu_screen = index
        if gp_info.menu_screen==2:
            gp_info.player_count(frame,coordinates,root_model)
    return 42

def character_select(frame,coordinates,root_model,gp_info):
    menu_control(frame,coordinates,root_model,gp_info)
    return 42