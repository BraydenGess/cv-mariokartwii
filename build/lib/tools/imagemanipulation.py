import cv2
import numpy as np

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

def supersharpimgtobinary(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    out_binary = cv2.threshold(image, 235, 255, cv2.THRESH_BINARY)[1]
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
    new = edge(new)
    return new

def edge(frame):
    new_frame = frame.copy()
    for row in range(5, len(frame) - 4):
        for col in range(5, len(frame[row]) - 4):
            window = frame[row - 4:row + 4, col - 4:col + 4]
            filter = np.ones([8, 8], dtype=int)
            x = np.sum(np.multiply(window, filter))
            if x >= (255 * 54):
                new_frame[row][col] = 0
    return new_frame

def switch(frame):
    dark = supersharpimgtobinary(frame)
    light = supersharpimgtobinary(255-frame)
    new = (dark + light)
    return new