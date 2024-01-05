from tools.deep_learning import predict

def get_playercount(frame,coordinates,root_model,gp_info):
    index,confidence = predict(frame,coordinates.playercount_coordinates,
                               root_model.playercountdetect_model,'sharpimgtobinary')
    if ((index)>=1 and (confidence>0.99)):
        gp_info.player_count = index+1
    return gp_info

def get_characters(frame,coordinates,root_model,gp_info):
    characters = []
    if gp_info.player_count == 2:
        for i in range(2):
            index,conf = predict(frame,coordinates.char2_coordinates[i],root_model.char2detect_model,'lightimgtobinary')
            characters.append(index)
    if gp_info.player_count >= 3:
        for i in range(gp_info.player_count):
            index,conf = predict(frame,coordinates.char4_coordinates[i],root_model.char4detect_model,'lightimgtobinary')
            characters.append(index)
    print(characters)
    return 42

def menu_control(frame,coordinates,root_model,gp_info):
    index,confidence = predict(frame,coordinates.menu_coordinates,root_model.menudetect_model,'sharpimgtobinary')
    if confidence>0.95:
        if index != 0:
            gp_info.menu_screen = index
        if gp_info.menu_screen == 2:
            gp_info = get_playercount(frame,coordinates,root_model,gp_info)
        if gp_info.menu_screen == 3:
            get_characters(frame, coordinates, root_model, gp_info)
    return 42

def character_select(frame,coordinates,root_model,gp_info):
    menu_control(frame,coordinates,root_model,gp_info)
    return 42