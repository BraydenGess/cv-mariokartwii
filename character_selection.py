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
            if conf > 0.9:
                characters.append(index)
    if gp_info.player_count >= 3:
        for i in range(gp_info.player_count):
            index,conf = predict(frame,coordinates.char4_coordinates[i],root_model.char4detect_model,'lightimgtobinary')
            print(index,conf)
            if conf > 0.9:
                characters.append(index)
    ### Set Characters ###
    if len(characters) == gp_info.player_count:
        for i in range(len(characters)):
            gp_info.players[gp_info.colors[i]].character = characters[i]
    return 42

def get_vehicles(frame,coordinates,root_model,gp_info):
    vehicles = []
    if gp_info.player_count == 2:
        for i in range(2):
            index, conf = predict(frame, coordinates.vehicle2_coordinates[i], root_model.vehicle2detect_model,
                                  'sharpimgtobinary')
            if conf > 0.9:
                vehicles.append(index)
    if gp_info.player_count >= 3:
        for i in range(gp_info.player_count):
            index, conf = predict(frame, coordinates.vehicle4_coordinates[i], root_model.vehicle4detect_model,
                                  'sharpimgtobinary')
            if conf > 0.9:
                vehicles.append(index)
    ### Set Characters ###
    if len(vehicles) == gp_info.player_count:
        for i in range(len(vehicles)):
            gp_info.players[gp_info.colors[i]].vehicle = vehicles[i]
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
        if gp_info.menu_screen == 4:
            get_vehicles(frame,coordinates,root_model,gp_info)
        if gp_info.menu_screen == 6:
            gp_info.read_menu = False

def character_select(frame,coordinates,root_model,gp_info):
    menu_control(frame,coordinates,root_model,gp_info)
    return 42