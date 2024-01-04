from tools.deep_learning import predict

def menu_control(frame,coordinates,root_model):
    index,confidence = predict(frame,coordinates.menu_coordinates,root_model.menudetect_model,'sharpimgtobinary')
    return 42


def character_select(frame,coordinates,root_model):
    menu_control(frame,coordinates,root_model)
    return 42