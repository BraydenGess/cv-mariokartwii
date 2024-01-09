def remove_newline(string):
    if string[-1] == "\n":
        string = string[:-1]
    return string

def remove_comma(string):
    new_string = ''
    for element in string:
        if element == ',':
            new_string += ' '
        else:
            new_string += element
    return new_string

def text_spaces(string):
    new_text = ''
    prev = True
    for char in string:
        if char.islower():
            new_text += char
            prev = False
        if char.isupper():
            if prev == False:
                new_text += ' '
                new_text += char
            else:
                new_text += char
    return new_text

def string_tocolor(color):
    color_dict = {'white':(255,255,255),'black':(0,0,0)}
    if color.lower() in color_dict:
        return color_dict[color.lower()]
    return color_dict['black']
