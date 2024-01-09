def remove_newline(string):
    if string[-1] == "\n":
        string = string[:-1]
    return string

def remove_comma(string):
    new_string = ''
    for element in string:
        if element != ',':
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

def get_scoringdict():
    scoring_dict = {'1':15,'2':12,'3':10,'4':8,'5':7,'6':6,'7':5,'8':4,'9':3,'10':2,'11':1,'12':0}
    return scoring_dict