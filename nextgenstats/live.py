from tools.deep_learning import predict


def countdown(frame,root_model,coordinates,gp_info):
    if gp_info.player_count == 2:
        coordinates = coordinates.go2_coordinates
    else:
        coordinates = coordinates.go4_coordinates
    index,confidence = predict(frame,coordinates,root_model.godetect_model,'superlightimgtobinary')
    if (confidence>0.95):
        if index == 1:
            gp_info.started = True

def nextgenstats(frame,root_model,coordinates,gp_info):
    if (gp_info.racing and not gp_info.started):
        countdown(frame,root_model,coordinates,gp_info)
    return 42