

def menu_control(root_model):
    index,confidence = predict(frame,coordinates.course_coordinates,root_model.coursedetect_model,'sharpimgtobinary')
    return 42


def character_select(root_model):
    menu_control(root_model)
    return 42