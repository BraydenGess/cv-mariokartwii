from tools.deep_learning import predict

def get_playercount(frame,coordinates,root_model,gp_info):
    index,confidence = predict(frame,coordinates.playercount_coordinates,
                               root_model.playercountdetect_model,'sharpimgtobinary')
    if ((index)>=1 and (confidence>0.99)):
        gp_info.player_count = index+1
    return gp_info

def add_objectolist(gp_info,frame,coordinates,model,filter,alpha):
    objects = []
    for i in range(gp_info.player_count):
        index, conf = predict(frame, coordinates[i], model, filter)
        if ((conf > alpha) and (index!=0)):
            objects.append(index)
    return objects
def get_objects(frame,coordinates2,coordinates4,model2,model4,gp_info,alpha,filter):
    if gp_info.player_count == 2:
        coordinates = coordinates2
        model = model2
    if gp_info.player_count >= 3:
        coordinates = coordinates4
        model = model4
    objects = add_objectolist(gp_info, frame, coordinates, model, filter, alpha)
    if len(objects) == gp_info.player_count:
        return True,objects
    return False,None

def get_characters(frame,coordinates,root_model,gp_info):
    valid,characters = get_objects(frame,coordinates.char2_coordinates,coordinates.char4_coordinates,
                                   root_model.char2detect_model,root_model.char4detect_model,gp_info,alpha=0.7,
                                   filter='lightimgtobinary')
    if valid:
        for i in range(len(characters)):
            gp_info.players[gp_info.colors[i]].character = characters[i]
    return gp_info

def get_vehicles(frame,coordinates,root_model,gp_info):
    valid, vehicles = get_objects(frame, coordinates.vehicle2_coordinates, coordinates.vehicle4_coordinates,
                                    root_model.vehicle2detect_model, root_model.vehicle4detect_model,gp_info,alpha= 0.7,
                                  filter='sharpimgtobinary')
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