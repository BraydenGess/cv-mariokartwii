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