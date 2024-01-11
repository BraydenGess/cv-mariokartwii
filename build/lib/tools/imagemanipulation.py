import cv2

def imgtobinary(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU)[1]
    return out_binary

def sharpimgtobinary(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out_binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)[1]
    return out_binary

def lightimgtobinary(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out_binary = cv2.threshold(image,140,255,cv2.THRESH_BINARY)[1]
    return out_binary

def superlightimgtobinary(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out_binary = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY)[1]
    return out_binary

def darkbinary(image,thresh):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out_binary = cv2.threshold(image,thresh, 255, cv2.THRESH_BINARY)[1]
    return out_binary

def lightbinary(image,thresh):
    image = (255-image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out_binary = cv2.threshold(image,thresh,255, cv2.THRESH_BINARY)[1]
    return out_binary

def extreme_values(image):
    dark = darkbinary(image,225)
    light = lightbinary(image,225)
    new = (dark+light)
    return new

def extreme_values2(image):
    dark = darkbinary(image,165)
    light = lightbinary(image,165)
    new = (dark+light)
    return new
