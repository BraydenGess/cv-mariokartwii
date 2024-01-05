from tools.deep_learning import predict

def get_playercount(frame,coordinates,root_model,gp_info):
    index,confidence = predict(frame,coordinates.playercount_coordinates,
                               root_model.playercountdetect_model,'sharpimgtobinary')
    if ((index)>=1 and (confidence>0.99)):
        gp_info.player_count = index+1
    return gp_info

def get_objects(frame,coordinates2,coordinates4,model2,model4,gp_info,alpha,filter):
    objects = []
    if gp_info.player_count == 2:
        for i in range(2):
            index,conf = predict(frame,coordinates2[i],model2,filter)
            if conf > alpha:
                objects.append(index)
    if gp_info.player_count >= 3:
        for i in range(gp_info.player_count):
            index,conf = predict(frame,coordinates4[i],model4,filter)
            if conf > 0.9:
                objects.append(index)
    if len(objects) == gp_info.player_count:
        return True,objects
    return False,None

def get_characters(frame,coordinates,root_model,gp_info):
    valid,characters = get_objects(frame,coordinates.char2_coordinates,coordinates.char4_coordinates,
                                   root_model.char2detect_model,root_model.char4detect_model,0.9,'lightimgtobinary')
    if valid:
        for i in range(len(characters)):
            gp_info.players[gp_info.colors[i]].character = characters[i]
    return gp_info

def get_vehicles(frame,coordinates,root_model,gp_info):
    valid, vehicles = get_objects(frame, coordinates.vehicle2_coordinates, coordinates.vehicle4_coordinates,
                                    root_model.vehicle2detect_model, root_model.vehicle4detect_model, 0.9,
                                  'sharpimgtobinary')
    if valid:
        for i in range(len(vehicles)):
            gp_info.players[gp_info.colors[i]].vehicle = vehicles[i]
    return gp_info

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