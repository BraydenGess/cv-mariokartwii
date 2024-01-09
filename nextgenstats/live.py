from tools.deep_learning import predict


def countdown(frame,root_model,coordinates,gp_info):
    if gp_info.player_count == 2:
        coordinates = coordinates.go2_coordinates
    index,confidence = predict(frame,coordinates,root_model.godetect_model,'suplerlightimgtobinary')
    print(index,confidence)



def nextgenstats(frame,root_model,coordinates,gp_info):
    print(gp_info.racing)
    if (gp_info.racing and not gp_info.started):
        countdown(frame,root_model,coordinates,gp_info)
    return 42